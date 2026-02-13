#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.deps import check_dependencies, print_dependency_report
from core.engine import RunOptions, run

BANNER = r"""
██╗     ███████╗██╗  ██╗
██║     ██╔════╝╚██╗██╔╝
██║     █████╗   ╚███╔╝ 
██║     ██╔══╝   ██╔██╗ 
███████╗███████╗██╔╝ ██╗
╚══════╝╚══════╝╚═╝  ╚═╝

        LexRecon v5
"""

def _read_domains(path: str) -> list[str]:
    doms = []
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        d = line.strip()
        if not d or d.startswith("#"):
            continue
        doms.append(d)
    # dedup preserve order
    seen=set()
    out=[]
    for d in doms:
        if d not in seen:
            seen.add(d); out.append(d)
    return out

def main(argv=None) -> int:
    print(BANNER)
    p = argparse.ArgumentParser(description="LexRecon v5 - scope-first recon framework (authorized use only)")

    tgt = p.add_mutually_exclusive_group(required=True)
    tgt.add_argument("-d", "--domain", help="Single target domain (in-scope)")
    tgt.add_argument("-i", "--input", help="File with in-scope domains (one per line). No discovery performed.")

    p.add_argument("--mode", choices=["fast","smart","deep"], default="smart", help="Run mode")
    p.add_argument("-o", "--out", default="results", help="Output base directory")
    p.add_argument("--max-workers", type=int, default=1, help="Parallelism across targets (default: 1)")
    p.add_argument("--timeout", type=int, default=900, help="Per-module command timeout seconds")
    p.add_argument("--httpx-timeout", type=int, default=10, help="httpx request timeout seconds")
    p.add_argument("--httpx-threads", type=int, default=50, help="httpx threads (per target)")
    p.add_argument("--rate-limit", type=int, default=0, help="httpx rate limit (-rl). 0 disables.")
    p.add_argument("--no-cache", action="store_true", help="Disable caching")
    p.add_argument("--cache-dir", default=".lexrecon_cache", help="Cache directory")
    p.add_argument("--jsonl-log", default="", help="Write a JSONL event log to this path (default: per-run folder)")
    p.add_argument("--check", action="store_true", help="Check dependencies and exit")
    p.add_argument("--strict", action="store_true", help="With --check: exit non-zero if required deps missing")

    args = p.parse_args(argv)

    if args.check:
        rep = check_dependencies()
        print_dependency_report(rep)
        if args.strict and rep.missing_required:
            return 2
        return 0

    domains = [args.domain] if args.domain else _read_domains(args.input)
    if not domains:
        print("[!] No domains provided.")
        return 2

    opt = RunOptions(
        out_base=args.out,
        mode=args.mode,
        max_workers=max(1, args.max_workers),
        timeout_s=args.timeout,
        httpx_timeout_s=args.httpx_timeout,
        httpx_threads=max(1, args.httpx_threads),
        httpx_rate_limit=max(0, args.rate_limit),
        cache=not args.no_cache,
        cache_dir=args.cache_dir,
        jsonl_log=args.jsonl_log or None,
    )

    run(domains, opt)
    print("\n[✓] Done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
