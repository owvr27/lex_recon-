import os, subprocess

def run(domain):
    outdir = f"results/{domain}/js"
    os.makedirs(outdir, exist_ok=True)

    js_files = f"{outdir}/js_files.txt"
    endpoints = f"{outdir}/js_endpoints.txt"

    subprocess.call(
        f"grep '.js' results/{domain}/urls/urls.txt | sort -u > {js_files}",
        shell=True
    )

    subprocess.call(
        f"python3 tools/LinkFinder/linkfinder.py -i {js_files} -o cli > {endpoints}",
        shell=True
    )

    return endpoints
