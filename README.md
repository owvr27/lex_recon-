        LΞX Recon
   Made by Omar Abdelsalam

# LΞX Recon

**LΞX Recon** is a **professional web reconnaissance framework** built for **real bug bounty hunters and web penetration testers**.

It focuses on **high-signal attack surface discovery** using **modern, proven recon methodologies**, avoiding noisy scans and misleading output.

> Recon should be **signal, not noise**.

---

## ✨ Key Features

- **Best-practice subdomain discovery (2025)**
  - Passive: `subfinder` + `assetfinder`
  - Optional active brute-force (opt-in): `ffuf`
- **Accurate live host detection**
  - Clean input filtering
  - HTTPS + redirect-aware probing with `httpx`
- URL collection from archives
  - `gau` + `waybackurls`
- JavaScript analysis
  - Hidden endpoint extraction
  - API route discovery
- Parameter discovery
  - GET / POST parameters
  - IDOR-style candidate detection
- **API recon**
  - REST
  - GraphQL
  - Swagger / OpenAPI endpoints
- Modular architecture
- Powerful **CLI + modern dark GUI**
- Clean, organized, human-readable output

---

## ⚡ Recon Modes

### ⚡ FAST
Designed for quick triage.

Includes:
- Passive subdomains
- Cleaned & resolved live hosts
- Archived URLs

Use this mode when testing many targets quickly.

---

### 🧠 DEEP
Designed for active bug hunting.

Includes:
- FAST recon +
- JavaScript file analysis
- Endpoint extraction
- Parameter discovery
- API endpoint mapping
- Technology fingerprinting

---

### 🤖 SMART (Recommended)
Adaptive mode.

LexRecon decides what to run based on early results:
- JS-heavy apps → deeper JS analysis
- API-heavy apps → API-focused recon
- Small surface → optional brute-force

This mode mimics how experienced bug bounty hunters think.

---

## 🖥 Usage

### GUI
```bash
python3 lexrecon_gui.py

CLI

python3 lexrecon_cli.py -d example.com --deep

Other modes:

python3 lexrecon_cli.py -d example.com --fast
python3 lexrecon_cli.py -d example.com --smart

📁 Output Structure

results/example.com/
├── subs/
│   ├── all_subdomains.txt
│   ├── clean_subdomains.txt
│   └── live_subdomains.txt
├── urls/
├── js/
├── params/
└── report/

    Only live_subdomains.txt represents the real attack surface.

🔧 Dependencies

External tools required (must be in $PATH):

    subfinder

    assetfinder

    httpx

    gau

    waybackurls

    ffuf (optional, for brute-force)

Wordlists:

wordlists/dns-Jhaddix.txt

Some helper tools are automatically handled by LexRecon when needed.
🔒 Ethics & Disclaimer

LexRecon is intended only for authorized security testing.

    No exploitation

    No scanning by default

    No bypass attempts

    Passive-first, safe-by-design

Do not use LexRecon against systems you do not own or have explicit permission to test.
👤 Author

Omar Abdelsalam
Bug Bounty Hunter · Offensive Security Engineer · Tool Developer
⭐ Final Note

LexRecon does not try to “find bugs”.

It does something more valuable:

    It puts you in the best possible position to find real bugs faster.



