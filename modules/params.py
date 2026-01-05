import os, subprocess

def run(domain):
    outdir = f"results/{domain}/params"
    os.makedirs(outdir, exist_ok=True)

    params = f"{outdir}/parameters.txt"
    idor = f"{outdir}/idor_candidates.txt"

    subprocess.call(
        f"arjun -u https://{domain} -oT {params}",
        shell=True
    )

    subprocess.call(
        f"grep -Ei 'id|user|account|uuid' {params} > {idor}",
        shell=True
    )

    return params
