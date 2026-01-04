#!/usr/bin/env python3
import os
import subprocess
import customtkinter as ctk

# ================== CONFIG ==================
APP_NAME = "LΞX Recon v2"
AUTHOR = "Made by Omar Abdelsalam"

RESULTS_DIR = "results"
TOOLS_DIR = "tools"

LINKFINDER_REPO = "https://github.com/GerbenJavado/LinkFinder"
PARAMSPIDER_REPO = "https://github.com/devanshbatham/ParamSpider"

# ================== UI SETUP ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ================== HELPERS ==================
def run_cmd(cmd):
    subprocess.call(cmd, shell=True)

def log(msg):
    output_box.insert("end", msg + "\n")
    output_box.see("end")
    app.update()

def ensure_tools():
    os.makedirs(TOOLS_DIR, exist_ok=True)

    if not os.path.exists(f"{TOOLS_DIR}/LinkFinder"):
        log("[+] Downloading LinkFinder...")
        run_cmd(f"git clone {LINKFINDER_REPO} {TOOLS_DIR}/LinkFinder")

    if not os.path.exists(f"{TOOLS_DIR}/ParamSpider"):
        log("[+] Downloading ParamSpider...")
        run_cmd(f"git clone {PARAMSPIDER_REPO} {TOOLS_DIR}/ParamSpider")

def ensure_target_dir(domain):
    path = f"{RESULTS_DIR}/{domain}"
    os.makedirs(path, exist_ok=True)
    return path

# ================== RECON LOGIC ==================
def run_full_recon():
    domain = domain_entry.get().strip()

    if not domain:
        log("[!] Please enter a domain")
        return

    ensure_tools()
    target_dir = ensure_target_dir(domain)

    log(f"[+] Starting FULL recon for {domain}")
    log("=" * 50)

    # Subdomains
    log("[1/7] Finding subdomains (subfinder + amass)")
    run_cmd(
        f"subfinder -d {domain} -silent | "
        f"amass enum -passive -d {domain} > {target_dir}/subdomains.txt"
    )

    # Live hosts
    log("[2/7] Checking live hosts (httpx)")
    run_cmd(
        f"cat {target_dir}/subdomains.txt | "
        f"httpx -silent > {target_dir}/live_hosts.txt"
    )

    # URLs
    log("[3/7] Collecting URLs (gau + wayback)")
    run_cmd(
        f"cat {target_dir}/live_hosts.txt | gau > {target_dir}/urls.txt"
    )
    run_cmd(
        f"cat {target_dir}/live_hosts.txt | waybackurls >> {target_dir}/urls.txt"
    )
    run_cmd(
        f"sort -u {target_dir}/urls.txt -o {target_dir}/urls.txt"
    )

    # JS files
    log("[4/7] Extracting JavaScript files")
    run_cmd(
        f"grep '\\.js' {target_dir}/urls.txt | sort -u > {target_dir}/js_files.txt"
    )

    # JS endpoints
    log("[5/7] Extracting JS endpoints (LinkFinder)")
    run_cmd(
        f"python3 {TOOLS_DIR}/LinkFinder/linkfinder.py "
        f"-i {target_dir}/js_files.txt -o cli > {target_dir}/js_endpoints.txt"
    )

    # Parameters
    log("[6/7] Discovering parameters (ParamSpider)")
    run_cmd(
        f"python3 {TOOLS_DIR}/ParamSpider/paramspider.py "
        f"-d {domain} -o {target_dir}/parameters.txt"
    )

    # Tech stack
    log("[7/7] Detecting technology stack (WhatWeb)")
    run_cmd(
        f"whatweb {domain} > {target_dir}/tech.txt"
    )

    log("=" * 50)
    log("[✓] FULL recon completed successfully")
    log(f"[✓] Results saved in: {target_dir}")

# ================== UI ==================
app = ctk.CTk()
app.title(APP_NAME)
app.geometry("1000x650")

title_label = ctk.CTkLabel(
    app, text=APP_NAME, font=("Hack", 28, "bold")
)
title_label.pack(pady=(15, 5))

author_label = ctk.CTkLabel(app, text=AUTHOR)
author_label.pack(pady=(0, 15))

domain_entry = ctk.CTkEntry(
    app,
    width=420,
    placeholder_text="example.com"
)
domain_entry.pack(pady=10)

run_button = ctk.CTkButton(
    app,
    text="🚀 RUN FULL RECON",
    width=250,
    height=40,
    command=run_full_recon
)
run_button.pack(pady=10)

output_box = ctk.CTkTextbox(
    app,
    width=920,
    height=400
)
output_box.pack(pady=15)

app.mainloop()
