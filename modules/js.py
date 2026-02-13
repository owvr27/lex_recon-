import os
from core.exec_utils import run_cmd

def run(domain, out_base="results", run_id=None, timeout_s=900):
    run_tag = run_id or "default"
    outdir = f"{out_base}/{domain}/{run_tag}/js"
    os.makedirs(outdir, exist_ok=True)

    js_files = f"{outdir}/js_files.txt"
    endpoints = f"{outdir}/js_endpoints.txt"

    urls_file = f"{out_base}/{domain}/{run_tag}/urls/urls.txt"
    if os.path.exists(urls_file):
        run_cmd(f"grep -i '\\.js\b' {urls_file} | sort -u > {js_files}", shell=True, timeout_s=timeout_s, quiet=True)
    else:
        open(js_files, "w").close()

    # If LinkFinder is present, use it. Otherwise leave endpoints empty.
    linkfinder = "tools/LinkFinder/linkfinder.py"
    if os.path.exists(linkfinder):
        run_cmd(f"python3 {linkfinder} -i {js_files} -o cli > {endpoints}", shell=True, timeout_s=timeout_s, quiet=True)
    else:
        open(endpoints, "w").close()

    return {"all": endpoints, "js_files": js_files, "outdir": outdir}
