#!/usr/bin/env python3
import subprocess
import os
import argparse

BANNER = r"""
██╗     ███████╗██╗  ██╗
██║     ██╔════╝╚██╗██╔╝
██║     █████╗   ╚███╔╝ 
██║     ██╔══╝   ██╔██╗ 
███████╗███████╗██╔╝ ██╗
╚══════╝╚══════╝╚═╝  ╚═╝

        LΞX Recon Tool
   Made by Omar Abdelsalam
"""

def run(cmd, stdin=None):
    return subprocess.Popen(
        cmd,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

def subdomains(domain):
    os.makedirs(f"results/{domain}", exist_ok=True)
    outfile = f"results/{domain}/live_subdomains.txt"

    print("[+] Running subfinder + amass")
    sub = run(["subfinder", "-d", domain, "-silent"])
    amass = run(["amass", "enum", "-passive", "-d", domain], stdin=sub.stdout)

    print("[+] Probing live hosts")
    httpx = run(["httpx", "-silent"], stdin=amass.stdout)
    output = httpx.communicate()[0]

    with open(outfile, "w") as f:
        f.write(output)

    print(f"[✓] Saved → {outfile}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description="LΞX Recon Tool")
    parser.add_argument("-d", "--domain", help="Target domain")
    parser.add_argument("--subdomains", action="store_true", help="Run subdomain recon")

    args = parser.parse_args()

    if args.domain and args.subdomains:
        subdomains(args.domain)
    else:
        parser.print_help()
