from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.cache import SimpleCache
from core.logging_utils import EventLogger
from core.url_prioritize import scope_filter_urls, probe_with_httpx, prioritize

from modules import subdomains, urls, js, params

@dataclass
class RunOptions:
    out_base: str = "results"
    mode: str = "smart"  # fast|smart|deep
    # safety / performance
    max_workers: int = 1
    timeout_s: int = 900
    httpx_timeout_s: int = 10
    httpx_threads: int = 50
    httpx_rate_limit: int = 0
    # caching
    cache: bool = True
    cache_dir: str = ".lexrecon_cache"
    # logging
    jsonl_log: str | None = None

def _run_single(domain: str, opt: RunOptions) -> dict:
    run_id = time.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    base_dir = Path(opt.out_base) / domain / run_id
    base_dir.mkdir(parents=True, exist_ok=True)

    logger = EventLogger(opt.jsonl_log or str(base_dir / "events.jsonl"))
    cache = SimpleCache(opt.cache_dir)

    logger.log("run_start", {"domain": domain, "mode": opt.mode, "run_id": run_id})

    results: dict = {"domain": domain, "run_id": run_id, "paths": {}}

    # --- Subdomains ---
    brute = (opt.mode == "deep")
    logger.log("subdomains_start", {"passive": True, "brute": brute})
    subs = subdomains.run(
        domain,
        passive=True,
        brute=brute,
        live=True,
        out_base=opt.out_base,
        run_id=run_id,
        timeout_s=opt.timeout_s,
        httpx_timeout_s=opt.httpx_timeout_s,
        httpx_threads=min(opt.httpx_threads, 100),
        httpx_rate_limit=opt.httpx_rate_limit,
    )
    results["paths"]["subs"] = subs

    # Smart escalation: if few lines in all_subdomains, enable brute (still opt.mode smart only)
    if opt.mode == "smart":
        try:
            n = sum(1 for _ in open(subs["all"], "r", encoding="utf-8", errors="ignore"))
        except Exception:
            n = 0
        if n < 50:
            logger.log("smart_escalate_bruteforce", {"reason": "low_subdomain_count", "count": n})
            subs = subdomains.run(
                domain,
                passive=True,
                brute=True,
                live=True,
                out_base=opt.out_base,
                run_id=run_id,
                timeout_s=opt.timeout_s,
                httpx_timeout_s=opt.httpx_timeout_s,
                httpx_threads=min(opt.httpx_threads, 100),
                httpx_rate_limit=opt.httpx_rate_limit,
            )
            results["paths"]["subs"] = subs

    # --- URL collection (from archives / optional crawler if installed) ---
    logger.log("urls_start", {})
    u = urls.run(domain, archive_only=False, out_base=opt.out_base, run_id=run_id, timeout_s=opt.timeout_s)
    results["paths"]["urls"] = u

    # --- JS analysis (if tool exists) ---
    logger.log("js_start", {})
    j = js.run(domain, out_base=opt.out_base, run_id=run_id, timeout_s=opt.timeout_s)
    results["paths"]["js"] = j

    # --- Params ---
    logger.log("params_start", {})
    p = params.run(domain, out_base=opt.out_base, run_id=run_id)
    results["paths"]["params"] = p

    # --- URL prioritization (scope-filtered, then live probe, then score) ---
    urls_dir = Path(u["outdir"])
    scoped = str(urls_dir / "scoped_urls.txt")
    live_jsonl = str(urls_dir / "live_urls.jsonl")
    live_txt = str(urls_dir / "live_urls.txt")
    prioritized_txt = str(urls_dir / "prioritized_urls.txt")
    prioritized_jsonl = str(urls_dir / "prioritized_urls.jsonl")
    high_value = str(urls_dir / "high_value_urls.txt")

    logger.log("url_scope_filter_start", {})
    kept = scope_filter_urls(u["all"], domain, scoped)
    logger.log("url_scope_filter_done", {"kept": kept, "out": scoped})

    # Cache key for httpx probe: depends on scoped file content hash + opts
    cache_key = cache.make_key("httpx_probe", {
        "domain": domain,
        "scoped_path": scoped,
        "threads": opt.httpx_threads,
        "timeout": opt.httpx_timeout_s,
        "rate_limit": opt.httpx_rate_limit,
    })

    do_probe = True
    if opt.cache:
        cached = cache.get(cache_key)
        if cached and os.path.exists(live_jsonl):
            do_probe = False
            logger.log("httpx_probe_cache_hit", {"cache_key": cache_key})

    if do_probe:
        logger.log("httpx_probe_start", {})
        rc = probe_with_httpx(
            scoped,
            live_jsonl,
            timeout_s=opt.httpx_timeout_s,
            threads=opt.httpx_threads,
            rate_limit=opt.httpx_rate_limit,
        )
        logger.log("httpx_probe_done", {"returncode": rc, "out": live_jsonl})
        if opt.cache and rc == 0:
            cache.set(cache_key, {"ok": True, "ts": time.time(), "live_jsonl": live_jsonl})

    logger.log("url_prioritize_start", {})
    pri_stats = prioritize(live_jsonl, prioritized_txt, prioritized_jsonl, high_value, live_txt)
    logger.log("url_prioritize_done", pri_stats)

    results["paths"]["urls"].update({
        "scoped": scoped,
        "live_jsonl": live_jsonl,
        "live": live_txt,
        "prioritized_txt": prioritized_txt,
        "prioritized_jsonl": prioritized_jsonl,
        "high_value": high_value,
    })
    results["stats"] = pri_stats

    # Final report
    report_path = base_dir / "report.json"
    import json
    report_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    logger.log("run_done", {"report": str(report_path)})

    return results

def run(domains: list[str], opt: RunOptions) -> list[dict]:
    """Run against an explicit list of in-scope domains (no discovery)."""
    if opt.max_workers < 1:
        opt.max_workers = 1
    results: list[dict] = []
    if opt.max_workers == 1 or len(domains) == 1:
        for d in domains:
            results.append(_run_single(d, opt))
        return results

    with ThreadPoolExecutor(max_workers=opt.max_workers) as ex:
        futs = {ex.submit(_run_single, d, opt): d for d in domains}
        for fut in as_completed(futs):
            results.append(fut.result())
    return results
