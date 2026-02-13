import os
from core.exec_utils import run_cmd

def run(
    domain,
    passive=True,
    brute=False,
    live=True,
    wordlist="wordlists/dns-Jhaddix.txt",
    out_base="results",
    run_id=None,
    timeout_s=600,
    httpx_timeout_s=10,
    httpx_threads=50,
    httpx_rate_limit=0,
):
    """
    Scope-first subdomain recon:
    - Passive: subfinder + assetfinder
    - Optional brute: ffuf (opt-in)
    - Cleaning
    - Live web check: httpx
    """
    run_tag = run_id or "default"
    outdir = f"{out_base}/{domain}/{run_tag}/subs"
    os.makedirs(outdir, exist_ok=True)

    all_subs = f"{outdir}/all_subdomains.txt"
    clean_subs = f"{outdir}/clean_subdomains.txt"
    brute_subs = f"{outdir}/brute_subdomains.csv"
    live_subs = f"{outdir}/live_subdomains.txt"

    if passive:
        cmd = (
            f"subfinder -d {domain} -silent; "
            f"assetfinder --subs-only {domain}"
        )
        run_cmd(f"{cmd} | sort -u > {all_subs}", shell=True, timeout_s=timeout_s, quiet=True)

    if brute:
        ffuf_cmd = (
            f"ffuf -u https://FUZZ.{domain} "
            f"-w {wordlist} "
            f"-mc 200 "
            f"-t 50 "
            f"-of csv -o {brute_subs}"
        )
        run_cmd(ffuf_cmd, shell=True, timeout_s=timeout_s, quiet=True)
        run_cmd(
            f"cut -d',' -f1 {brute_subs} | sort -u >> {all_subs}",
            shell=True, timeout_s=timeout_s, quiet=True
        )
        run_cmd(f"sort -u {all_subs} -o {all_subs}", shell=True, timeout_s=timeout_s, quiet=True)

    run_cmd(
        f"grep -E '^[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$' {all_subs} | "
        f"grep -v '@' | grep -v '\\*' | sort -u > {clean_subs}",
        shell=True, timeout_s=timeout_s, quiet=True
    )

    if live:
        rl = f" -rl {httpx_rate_limit} " if httpx_rate_limit and httpx_rate_limit > 0 else " "
        run_cmd(
            f"cat {clean_subs} | httpx -silent -https -follow-redirects -threads {httpx_threads} -timeout {httpx_timeout_s}{rl}> {live_subs}",
            shell=True,
            timeout_s=timeout_s,
            quiet=True
        )

    return {"all": all_subs, "clean": clean_subs, "live": live_subs, "outdir": outdir}
