import customtkinter as ctk
import subprocess, os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

APP_NAME = "LΞX Recon v2"
AUTHOR = "Made by Omar Abdelsalam"

def run(cmd):
    return subprocess.getoutput(cmd)

def ensure(domain):
    path = f"results/{domain}"
    os.makedirs(path, exist_ok=True)
    return path

def log(msg):
    output.insert("end", msg + "\n")
    output.see("end")
    app.update()

def recon_all():
    domain = entry.get().strip()
    if not domain:
        log("[!] Enter a domain")
        return

    path = ensure(domain)

    log("[+] Finding subdomains")
    run(f"subfinder -d {domain} -silent | amass enum -passive -d {domain} > {path}/subs.txt")

    log("[+] Checking live hosts")
    run(f"cat {path}/subs.txt | httpx -silent > {path}/live.txt")

    log("[+] Collecting URLs")
    run(f"cat {path}/live.txt | gau > {path}/urls.txt")
    run(f"cat {path}/live.txt | waybackurls >> {path}/urls.txt")

    log("[+] Extracting JS files")
    run(f"grep '.js' {path}/urls.txt | sort -u > {path}/js.txt")

    log("[+] Extracting JS endpoints")
    run(f"python3 tools/LinkFinder/linkfinder.py -i {path}/js.txt -o cli > {path}/js_endpoints.txt")

    log("[+] Finding parameters")
    run(f"python3 tools/ParamSpider/paramspider.py -d {domain} -o {path}/params.txt")

    log("[+] Detecting tech stack")
    run(f"whatweb {domain} > {path}/tech.txt")

    log("[✓] Recon completed successfully")

# ---------------- UI ----------------
app = ctk.CTk()
app.title(APP_NAME)
app.geometry("1000x650")

title = ctk.CTkLabel(app, text=APP_NAME, font=("Hack", 28))
title.pack(pady=10)

subtitle = ctk.CTkLabel(app, text=AUTHOR)
subtitle.pack()

entry = ctk.CTkEntry(app, width=400, placeholder_text="example.com")
entry.pack(pady=15)

btn = ctk.CTkButton(app, text="🚀 RUN FULL RECON", command=recon_all)
btn.pack(pady=10)

output = ctk.CTkTextbox(app, width=900, height=400)
output.pack(pady=10)

app.mainloop()
