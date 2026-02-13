import os
from core.exec_utils import run_cmd

def run(domain, archive_only=False, out_base="results", run_id=None, timeout_s=900):
    run_tag = run_id or "default"
    outdir = f"{out_base}/{domain}/{run_tag}/urls"
    os.makedirs(outdir, exist_ok=True)

    urls = f"{outdir}/urls.txt"
    # Archive sources
    run_cmd(f"gau {domain} > {urls}", shell=True, timeout_s=timeout_s, quiet=True)
    run_cmd(f"waybackurls {domain} >> {urls}", shell=True, timeout_s=timeout_s, quiet=True)

    # Optional crawler if installed (katana). Keep safe depth.
    if not archive_only:
        run_cmd(f"katana -u https://{domain} -d 2 -silent >> {urls}", shell=True, timeout_s=timeout_s, quiet=True)

    run_cmd(f"sort -u {urls} -o {urls}", shell=True, timeout_s=timeout_s, quiet=True)
    run_cmd(f"grep '\\?' {urls} > {outdir}/urls_with_params.txt", shell=True, timeout_s=timeout_s, quiet=True)

    return {"all": urls, "with_params": f"{outdir}/urls_with_params.txt", "outdir": outdir}
