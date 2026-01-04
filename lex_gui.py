#!/usr/bin/env python3
import os, subprocess
import customtkinter as ctk

# ---------------- CONFIG ----------------
APP_NAME = "LΞX Recon v2.5"
AUTHOR = "Made by Omar Abdelsalam"
RESULTS = "results"
TOOLS = "tools"

LINKFINDER = "https://github.com/GerbenJavado/LinkFinder"
PARAMSPIDER = "https://github.com/devanshbatham/ParamSpider"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ---------------- HELPERS ----------------
def cmd(c): subprocess.call(c, shell=True)
def log(m): output.insert("end", m+"\n"); output.see("end"); app.update()

def ensure_tools():
    os.makedirs(TOOLS, exist_ok=True)
    if not os.path.exists(f"{TOOLS}/LinkFinder"):
        log("[+] Downloading LinkFinder")
        cmd(f"git clone {LINKFINDER} {TOOLS}/LinkFinder")
    if not os.path.exists(f"{TOOLS}/ParamSpider"):
        log("[+] Downloading ParamSpider")
        cmd(f"git clone {PARAMSPIDER} {TOOLS}/ParamSpider")

def tdir(d):
    p=f"{RESULTS}/{d}"
    os.makedirs(p, exist_ok=True)
    return p

# ---------------- RECON ----------------
def run_recon(mode):
    domain = entry.get().strip()
    if not domain:
        log("[!] Enter a domain"); return

    ensure_tools()
    p = tdir(domain)

    log(f"[+] Recon mode: {mode.upper()} | Target: {domain}")

    log("[1] Subdomains")
    cmd(f"subfinder -d {domain} -silent | amass enum -passive -d {domain} > {p}/subs.txt")

    log("[2] Live hosts")
    cmd(f"cat {p}/subs.txt | httpx -silent > {p}/live.txt")

    log("[3] URLs")
    cmd(f"cat {p}/live.txt | gau > {p}/urls.txt")
    cmd(f"cat {p}/live.txt | waybackurls >> {p}/urls.txt")
    cmd(f"sort -u {p}/urls.txt -o {p}/urls.txt")

    if mode == "fast":
        log("[✓] FAST recon completed"); return

    log("[4] JS files")
    cmd(f"grep '\\.js' {p}/urls.txt | sort -u > {p}/js.txt")

    log("[5] JS endpoints")
    cmd(f"python3 {TOOLS}/LinkFinder/linkfinder.py -i {p}/js.txt -o cli > {p}/js_endpoints.txt")

    log("[6] Parameters")
    cmd(f"python3 {TOOLS}/ParamSpider/paramspider.py -d {domain} -o {p}/params.txt")

    log("[7] API recon")
    cmd(f"grep -Ei '/api|/v1|/v2|graphql|swagger|openapi' {p}/urls.txt > {p}/api_endpoints.txt")
    cmd(f"grep -Ei '/api|/v1|/v2|graphql' {p}/js_endpoints.txt >> {p}/api_endpoints.txt")
    cmd(f"sort -u {p}/api_endpoints.txt -o {p}/api_endpoints.txt")

    log("[8] Tech stack")
    cmd(f"whatweb {domain} > {p}/tech.txt")

    log("[✓] DEEP recon completed")

# ---------------- UI ----------------
app = ctk.CTk()
app.title(APP_NAME)
app.geometry("1050x700")

ctk.CTkLabel(app, text=APP_NAME, font=("Hack",28,"bold")).pack(pady=10)
ctk.CTkLabel(app, text=AUTHOR).pack()

entry = ctk.CTkEntry(app, width=420, placeholder_text="example.com")
entry.pack(pady=10)

frame = ctk.CTkFrame(app)
frame.pack(pady=5)

ctk.CTkButton(frame, text="⚡ FAST RECON", width=180,
              command=lambda: run_recon("fast")).pack(side="left", padx=10)

ctk.CTkButton(frame, text="🧠 DEEP RECON", width=180,
              command=lambda: run_recon("deep")).pack(side="left", padx=10)

output = ctk.CTkTextbox(app, width=980, height=420)
output.pack(pady=15)

app.mainloop()
