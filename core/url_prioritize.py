from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

from core.exec_utils import run_cmd
from core.normalize import normalize_url

KEYWORDS = [
    "admin","login","signin","sign-in","auth","oauth","sso","reset","password",
    "api","graphql","swagger","openapi","docs","doc","v1","v2",
    "upload","import","export","download","backup","debug","console",
    "config","settings","manage","panel","dashboard",
    "callback","redirect","return","next=",
    ".php",".aspx",".jsp",".action",".do",".json",".xml"
]
HIGH_VALUE_REGEX = re.compile(r"(admin|login|signin|auth|oauth|sso|graphql|swagger|openapi|upload|import|export|reset|callback)", re.I)

def _status_score(code: int) -> int:
    if code == 200: return 40
    if code in (201,202,204): return 30
    if code in (301,302,303,307,308): return 25
    if code in (401,403): return 22
    if 200 <= code < 300: return 28
    if 300 <= code < 400: return 18
    if 400 <= code < 500: return 6
    if 500 <= code < 600: return 4
    return 0

def score_url(url: str, status_code: int | None = None, title: str | None = None, content_type: str | None = None) -> int:
    s = 0
    u = url.lower()
    if status_code is not None:
        s += _status_score(status_code)
    # parameters
    try:
        parts = urlsplit(url)
        q = parse_qs(parts.query)
        if q:
            s += 10
            s += min(10, len(q))  # more params => slightly higher
    except Exception:
        pass
    # keywords in url
    for k in KEYWORDS:
        if k in u:
            s += 3
    # title/content-type signals
    if title:
        t = title.lower()
        if any(x in t for x in ("admin","login","dashboard","api","graphql","swagger")):
            s += 8
    if content_type:
        ct = content_type.lower()
        if "json" in ct or "xml" in ct:
            s += 5
    return s

def scope_filter_urls(input_urls_path: str, domain: str, out_path: str) -> int:
    dom = domain.lower().strip()
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    kept = 0
    with open(input_urls_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            u = line.strip()
            if not u:
                continue
            nu = normalize_url(u)
            if not nu:
                continue
            host = urlsplit(nu).hostname or ""
            host = host.lower()
            if host == dom or host.endswith("." + dom):
                if nu not in seen:
                    seen.add(nu)
                    kept += 1
    out.write_text("\n".join(sorted(seen)) + ("\n" if seen else ""), encoding="utf-8")
    return kept

def probe_with_httpx(scoped_urls_path: str, jsonl_out: str, *,
                     timeout_s: int = 10,
                     threads: int = 50,
                     rate_limit: int = 0,
                     filter_codes: str = "200,301,302,303,307,308,401,403") -> int:
    """Runs httpx in a scope-first way. Requires input list."""
    Path(jsonl_out).parent.mkdir(parents=True, exist_ok=True)
    rl_flag = f" -rl {rate_limit} " if rate_limit and rate_limit > 0 else " "
    cmd = (
        f"cat {scoped_urls_path} | "
        f"httpx -silent -json -title -status-code -content-type -follow-redirects "
        f"-threads {threads} -timeout {timeout_s}{rl_flag}"
        f"-mc {filter_codes} > {jsonl_out}"
    )
    res = run_cmd(cmd, shell=True, timeout_s=max(60, timeout_s * 10), quiet=True)
    return 0 if res.returncode == 0 else res.returncode

def prioritize(jsonl_in: str, txt_out: str, jsonl_out: str, high_value_out: str, live_out: str) -> dict:
    p_in = Path(jsonl_in)
    if not p_in.exists():
        return {"error":"missing httpx output"}
    scored = []
    live_urls = set()
    with p_in.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line=line.strip()
            if not line: 
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            url = rec.get("url") or rec.get("input") or ""
            if not url:
                continue
            url = normalize_url(url)
            code = rec.get("status_code")
            title = rec.get("title")
            ctype = rec.get("content_type")
            live_urls.add(url)
            s = score_url(url, code, title, ctype)
            rec2 = {
                "score": s,
                "url": url,
                "status_code": code,
                "title": title,
                "content_type": ctype,
            }
            scored.append(rec2)

    scored.sort(key=lambda r: (r["score"], r.get("status_code") or 0), reverse=True)

    Path(txt_out).parent.mkdir(parents=True, exist_ok=True)
    Path(jsonl_out).parent.mkdir(parents=True, exist_ok=True)
    Path(high_value_out).parent.mkdir(parents=True, exist_ok=True)
    Path(live_out).parent.mkdir(parents=True, exist_ok=True)

    with open(txt_out, "w", encoding="utf-8") as ftxt, open(jsonl_out, "w", encoding="utf-8") as fj:
        for r in scored:
            ftxt.write(f"{r['score']}\t{r.get('status_code','')}\t{r['url']}\n")
            fj.write(json.dumps(r, ensure_ascii=False) + "\n")

    # high value subset
    hv = []
    for r in scored:
        if r["score"] >= 55 or HIGH_VALUE_REGEX.search(r["url"]):
            hv.append(r["url"])
    Path(high_value_out).write_text("\n".join(hv) + ("\n" if hv else ""), encoding="utf-8")

    Path(live_out).write_text("\n".join(sorted(live_urls)) + ("\n" if live_urls else ""), encoding="utf-8")

    return {
        "live_count": len(live_urls),
        "prioritized_count": len(scored),
        "high_value_count": len(hv),
    }
