import os, subprocess

def run(domain, archive_only=False):
    outdir = f"results/{domain}/urls"
    os.makedirs(outdir, exist_ok=True)

    urls = f"{outdir}/urls.txt"
    subprocess.call(f"gau {domain} > {urls}", shell=True)
    subprocess.call(f"waybackurls {domain} >> {urls}", shell=True)

    if not archive_only:
        subprocess.call(f"katana -u {domain} -d 3 >> {urls}", shell=True)

    subprocess.call(f"sort -u {urls} -o {urls}", shell=True)
    subprocess.call(
        f"grep '?' {urls} > {outdir}/urls_with_params.txt",
        shell=True
    )

    return urls

def has_js(domain):
    return True

def has_params(domain):
    return True
