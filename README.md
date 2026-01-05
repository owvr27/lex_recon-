

        LΞX Recon
   Made by Omar Abdelsalam

# LΞX Recon

LΞX Recon is a **professional reconnaissance automation framework** designed for **real bug bounty hunters and penetration testers**.

It focuses on **high-signal attack surface discovery**, not noisy scanning.

---

## ✨ Features

- Subdomain enumeration (subfinder + amass)
- Live host detection (httpx)
- URL collection (gau + wayback)
- JavaScript endpoint extraction
- Parameter discovery
- **API recon (REST, GraphQL, Swagger)**
- Tech stack fingerprinting
- Modern dark GUI + powerful CLI

---

## ⚡ Recon Modes

### FAST
- Subdomains
- Live hosts
- URLs

Best for quick triage.

### DEEP
- FAST recon +
- JS files & endpoints
- Parameters
- API endpoints
- Tech stack

Best for full bug-hunting.

---

## 🖥 Usage

### GUI
```bash
python3 lex_recon_gui.py
---

###Cli 
python3 lex_recon_cli.py -d example.com --deep


🔧 Dependencies

LΞX Recon auto-downloads:

LinkFinder

ParamSpider

External tools required:

subfinder

amass

httpx

gau

waybackurls

whatweb

⚠️ Disclaimer

For authorized security testing only.
Do not use against systems you do not own or have permission to test.

👤 Author

Omar Abdelsalam
