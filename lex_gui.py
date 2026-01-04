import tkinter as tk
from tkinter import messagebox
import subprocess
import os

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

def ensure_dir(domain):
    path = f"results/{domain}"
    os.makedirs(path, exist_ok=True)
    return path

def status(msg):
    status_label.config(text=msg)
    root.update()

def show(text):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, text)

def subdomain_recon():
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showerror("Error", "Enter a domain")
        return

    path = ensure_dir(domain)
    outfile = f"{path}/live_subdomains.txt"

    status("Running subfinder + amass...")
    sub = run(["subfinder", "-d", domain, "-silent"])
    amass = run(["amass", "enum", "-passive", "-d", domain], stdin=sub.stdout)

    status("Checking live hosts...")
    httpx = run(["httpx", "-silent"], stdin=amass.stdout)
    result = httpx.communicate()[0]

    with open(outfile, "w") as f:
        f.write(result)

    show(result)
    status(f"Saved → {outfile}")

# ---------- UI ----------
root = tk.Tk()
root.title("LΞX Recon Tool")
root.geometry("950x650")

banner_box = tk.Text(root, height=10, bg="black", fg="green", font=("Courier", 10))
banner_box.pack(fill=tk.X)
banner_box.insert(tk.END, BANNER)
banner_box.config(state=tk.DISABLED)

tk.Label(root, text="Target Domain", font=("Arial", 14)).pack(pady=5)
domain_entry = tk.Entry(root, width=40, font=("Arial", 14))
domain_entry.pack()

tk.Button(
    root,
    text="Find Subdomains",
    font=("Arial", 12),
    width=20,
    command=subdomain_recon
).pack(pady=10)

status_label = tk.Label(root, text="Idle", fg="cyan")
status_label.pack()

output_box = tk.Text(root, height=25, width=115)
output_box.pack(pady=10)

tk.Label(
    root,
    text="Made by Omar Abdelsalam",
    fg="gray"
).pack(side=tk.BOTTOM, pady=5)

root.mainloop()
