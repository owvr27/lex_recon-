import os
import subprocess

def run(
    domain,
    passive=True,
    brute=False,
    live=True,
    wordlist="wordlists/dns-Jhaddix.txt"
):
    """
    Best-practice subdomain recon:
    - Passive: subfinder + assetfinder
    - Optional brute-force: ffuf
    - Resolve live hosts: httpx
    """

    outdir = f"results/{domain}/subs"
    os.makedirs(outdir, exist_ok=True)

    all_subs = f"{outdir}/all_subdomains.txt"
    brute_subs = f"{outdir}/brute_subdomains.txt"
    live_subs = f"{outdir}/live_subdomains.txt"

    # ----------------------------
    # 1) Passive enumeration
    # ----------------------------
    if passive:
        cmd = (
            f"subfinder -d {domain} -silent && "
            f"assetfinder --subs-only {domain}"
        )

        subprocess.call(
            f"{cmd} | sort -u > {all_subs}",
            shell=True,
            stderr=subprocess.DEVNULL
        )

    # ----------------------------
    # 2) Active brute-force (OPT-IN)
    # ----------------------------
    if brute:
        ffuf_cmd = (
            f"ffuf -u https://FUZZ.{domain} "
            f"-w {wordlist} "
            f"-mc 200 "
            f"-t 100 "
            f"-of csv -o {brute_subs}"
        )

        subprocess.call(
            ffuf_cmd,
            shell=True,
            stderr=subprocess.DEVNULL
        )

        # Extract valid subs from ffuf output
        subprocess.call(
            f"cut -d',' -f1 {brute_subs} | sort -u >> {all_subs}",
            shell=True
        )

        subprocess.call(
            f"sort -u {all_subs} -o {all_subs}",
            shell=True
        )

    # ----------------------------
    # 3) Resolve live hosts
    # ----------------------------
    if live:
        subprocess.call(
            f"cat {all_subs} | httpx -silent > {live_subs}",
            shell=True,
            stderr=subprocess.DEVNULL
        )

    return {
        "all": all_subs,
        "live": live_subs
    }
