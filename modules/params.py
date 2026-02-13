import os
from urllib.parse import urlsplit, parse_qsl
from core.normalize import normalize_url

def run(domain, out_base="results", run_id=None):
    run_tag = run_id or "default"
    outdir = f"{out_base}/{domain}/{run_tag}/params"
    os.makedirs(outdir, exist_ok=True)

    urls_file = f"{out_base}/{domain}/{run_tag}/urls/urls.txt"
    out_params = f"{outdir}/params.txt"

    params = set()
    if os.path.exists(urls_file):
        with open(urls_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                u = normalize_url(line.strip())
                if not u:
                    continue
                try:
                    q = parse_qsl(urlsplit(u).query, keep_blank_values=True)
                except Exception:
                    continue
                for k, _ in q:
                    if k:
                        params.add(k)

    with open(out_params, "w", encoding="utf-8") as f:
        for p in sorted(params):
            f.write(p + "\n")

    return {"all": out_params, "outdir": outdir}
