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
    Best-practice subdomain reconnaissance (2025):

    - Passive: subfinder + assetfinder
    - Optional brute-force: ffuf (opt-in)
    - Cleaning: remove wildcards, emails, junk
    - Live resolution: httpx (HTTPS + redirects)

    Outputs only REAL attack surface.
    """

    outdir = f"results/{domain}/subs"
    os.makedirs(outdir, exist_ok=True)

    all_subs = f"{outdir}/all_subdomains.txt"
    clean_subs = f"{outdir}/clean_subdomains.txt"
    brute_subs = f"{outdir}/brute_subdomains.txt"
    live_subs = f"{outdir}/live_subdomains.txt"

    # -------------------------------------------------
    # 1) Passive subdomain enumeration (BEST PRACTICE)
    # -------------------------------------------------
    if passive:
        cmd = (
            f"subfinder -d {domain} -silent; "
            f"assetfinder --subs-only {domain}"
        )

        subprocess.call(
            f"{cmd} | sort -u > {all_subs}",
            shell=True,
            stderr=subprocess.DEVNULL
        )

    # -------------------------------------------------
    # 2) Active brute-force (OPTIONAL, OPT-IN)
    # -------------------------------------------------
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

        # Extract discovered subdomains from ffuf output
        subprocess.call(
            f"cut -d',' -f1 {brute_subs} | sort -u >> {all_subs}",
            shell=True,
            stderr=subprocess.DEVNULL
        )

        subprocess.call(
            f"sort -u {all_subs} -o {all_subs}",
            shell=True,
            stderr=subprocess.DEVNULL
        )

    # -------------------------------------------------
    # 3) Clean subdomains BEFORE resolving (CRITICAL)
    # -------------------------------------------------
    subprocess.call(
        f"grep -E '^[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$' {all_subs} | "
        f"grep -v '@' | grep -v '\\*' | sort -u > {clean_subs}",
        shell=True,
        stderr=subprocess.DEVNULL
    )

    # -------------------------------------------------
    # 4) Resolve LIVE web hosts (PROPERLY)
    # -------------------------------------------------
    if live:
        subprocess.call(
            f"cat {clean_subs} | "
            f"httpx -silent -https -follow-redirects > {live_subs}",
            shell=True,
            stderr=subprocess.DEVNULL
        )

    return {
        "all": all_subs,
        "clean": clean_subs,
        "live": live_subs
    }
