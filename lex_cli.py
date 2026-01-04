#!/usr/bin/env python3
import os
import argparse
import subprocess

# ================== LΞX LOGO ==================
BANNER = r"""
██╗     ███████╗██╗  ██╗
██║     ██╔════╝╚██╗██╔╝
██║     █████╗   ╚███╔╝ 
██║     ██╔══╝   ██╔██╗ 
███████╗███████╗██╔╝ ██╗
╚══════╝╚══════╝╚═╝  ╚═╝

        LΞX Recon v2.5
   Made by Omar Abdelsalam
"""

print(BANNER)

# ================== CONFIG ==================
TOOLS = "tools"
RESULTS = "results"

LINKFINDER_REPO = "https://github.com/GerbenJavado/LinkFinder"
PARAMSPIDER_REPO = "https://github.com/devanshbatham/ParamSpider"

# ================== HELPERS ==================
def cmd(c):
    subprocess.call(c, shell=True)

def ensure_tools():
    os.makedirs(TOOLS, exist_ok=True)

    if not os.path.exists(f"{TOOLS}/LinkFinder"):
        print("[+] Downloading LinkFinder...")
        cmd(f"git clone {LINKFINDER_REPO} {TOOLS}/LinkFinder")

    if not os.path.exists(f"{TOOLS}/ParamSpider"):
        print("[+] Downloading ParamSpider...")
        cmd(f"git clone {PARAMSPIDER_REPO} {TOOLS}/ParamSpider")

# ================== RECON ==================
def recon(domain, mode):
    ensure_tools()

    target_dir = f"{RESULTS}/{domain}"
    os.makedirs(target_dir, exist_ok=True)

    print(f"[+] Target: {domain}")
    print(f"[+] Mode: {mode.upper()}")
    print("-" * 50)

    print("[1/8] Subdomains")
    cmd(f"subfinder -d {domain} -silent | amass enum -passive -d {domain} > {target_dir}/subs.txt")

    print("[2/8] Live hosts")
    cmd(f"cat {target_dir}/subs.txt | httpx -silent > {target_dir}/live.txt")

    print("[3/8] URLs")
    cmd(f"cat {target_dir}/live.txt | gau > {target_dir}/urls.txt")
    cmd(f"cat {target_dir}/live.txt | waybackurls >> {target_dir}/urls.txt")
    cmd(f"sort -u {target_dir}/urls.txt -o {target_dir}/urls.txt")

    if mode == "fast":
        print("[✓] FAST recon completed")
        print(f"[✓] Results saved in {target_dir}")
        return

    print("[4/8] JavaScript files")
    cmd(f"grep '\\.js' {target_dir}/urls.txt | sort -u > {target_dir}/js.txt")

    print("[5/8] JS endpoints")
    cmd(f"python3 {TOOLS}/LinkFinder/linkfinder.py -i {target_dir}/js.txt -o cli > {target_dir}/js_endpoints.txt")

    print("[6/8] Parameters")
    cmd(f"python3 {TOOLS}/ParamSpider/paramspider.py -d {domain} -o {target_dir}/params.txt")

    print("[7/8] API recon")
    cmd(f"grep -Ei '/api|/v1|/v2|graphql|swagger|openapi' {target_dir}/urls.txt > {target_dir}/api_endpoints.txt")
    cmd(f"grep -Ei '/api|/v1|/v2|graphql' {target_dir}/js_endpoints.txt >> {target_dir}/api_endpoints.txt")
    cmd(f"sort -u {target_dir}/api_endpoints.txt -o {target_dir}/api_endpoints.txt")

    print("[8/8] Tech stack")
    cmd(f"whatweb {domain} > {target_dir}/tech.txt")

    print("-" * 50)
    print("[✓] DEEP recon completed successfully")
    print(f"[✓] Results saved in {target_dir}")

# ================== MAIN ==================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LΞX Recon CLI v2.5")
    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    parser.add_argument("--fast", action="store_true", help="Run fast recon")
    parser.add_argument("--deep", action="store_true", help="Run deep recon")

    args = parser.parse_args()

    mode = "fast" if args.fast else "deep"
    recon(args.domain, mode)
