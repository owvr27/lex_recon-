import shutil

REQUIRED_TOOLS = [
    "subfinder",
    "assetfinder",
    "httpx",
    "gau",
    "waybackurls"
]

OPTIONAL_TOOLS = [
    "ffuf"
]

def check_dependencies():
    print("\n[+] Checking dependencies...\n")

    for tool in REQUIRED_TOOLS:
        if shutil.which(tool):
            print(f"[✓] {tool}")
        else:
            print(f"[✗] {tool} (MISSING)")

    print("\nOptional tools:")
    for tool in OPTIONAL_TOOLS:
        if shutil.which(tool):
            print(f"[✓] {tool}")
        else:
            print(f"[!] {tool} not installed (optional)")
