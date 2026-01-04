#!/usr/bin/env python3
import os, argparse, subprocess

TOOLS="tools"; RESULTS="results"

def cmd(c): subprocess.call(c, shell=True)

def ensure():
    os.makedirs(TOOLS, exist_ok=True)
    if not os.path.exists(f"{TOOLS}/LinkFinder"):
        cmd("git clone https://github.com/GerbenJavado/LinkFinder tools/LinkFinder")
    if not os.path.exists(f"{TOOLS}/ParamSpider"):
        cmd("git clone https://github.com/devanshbatham/ParamSpider tools/ParamSpider")

def recon(domain, mode):
    ensure()
    p=f"{RESULTS}/{domain}"
    os.makedirs(p, exist_ok=True)

    print(f"[+] Mode: {mode.upper()} | Target: {domain}")

    cmd(f"subfinder -d {domain} -silent | amass enum -passive -d {domain} > {p}/subs.txt")
    cmd(f"cat {p}/subs.txt | httpx -silent > {p}/live.txt")
    cmd(f"cat {p}/live.txt | gau > {p}/urls.txt")
    cmd(f"cat {p}/live.txt | waybackurls >> {p}/urls.txt")
    cmd(f"sort -u {p}/urls.txt -o {p}/urls.txt")

    if mode == "fast":
        return

    cmd(f"grep '\\.js' {p}/urls.txt | sort -u > {p}/js.txt")
    cmd(f"python3 {TOOLS}/LinkFinder/linkfinder.py -i {p}/js.txt -o cli > {p}/js_endpoints.txt")
    cmd(f"python3 {TOOLS}/ParamSpider/paramspider.py -d {domain} -o {p}/params.txt")
    cmd(f"grep -Ei '/api|/v1|/v2|graphql|swagger|openapi' {p}/urls.txt > {p}/api_endpoints.txt")
    cmd(f"grep -Ei '/api|/v1|/v2|graphql' {p}/js_endpoints.txt >> {p}/api_endpoints.txt")
    cmd(f"sort -u {p}/api_endpoints.txt -o {p}/api_endpoints.txt")
    cmd(f"whatweb {domain} > {p}/tech.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LΞX Recon v2 CLI")
    parser.add_argument("-d","--domain",required=True)
    parser.add_argument("--fast",action="store_true")
    parser.add_argument("--deep",action="store_true")
    args = parser.parse_args()

    recon(args.domain, "fast" if args.fast else "deep")
