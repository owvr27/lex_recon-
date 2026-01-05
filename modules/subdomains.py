import os, subprocess

def run(domain, passive=True, live=False):
    outdir = f"results/{domain}/subs"
    os.makedirs(outdir, exist_ok=True)

    outfile = f"{outdir}/all_subdomains.txt"

    cmd = f"subfinder -d {domain} -silent"
    cmd += f" | assetfinder"
    cmd += f" | amass enum -passive -d {domain} -norecursive -noalts"

    subprocess.call(f"{cmd} > {outfile}", shell=True)

    if live:
        subprocess.call(
            f"cat {outfile} | httpx -silent > {outdir}/live_subdomains.txt",
            shell=True
        )

    return outfile
