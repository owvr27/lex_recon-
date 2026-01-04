

██╗ ███████╗██╗ ██╗
██║ ██╔════╝╚██╗██╔╝
██║ █████╗ ╚███╔╝
██║ ██╔══╝ ██╔██╗
███████╗███████╗██╔╝ ██╗
╚══════╝╚══════╝╚═╝ ╚═╝

    LΞX Recon Tool

Made by Omar Abdelsalam


# LΞX Recon Tool

LΞX is a **professional reconnaissance automation tool** built for **bug bounty hunters** and **penetration testers**.  
It automates high-quality **passive reconnaissance** using industry-standard tools and methodologies.

The tool is available in **both GUI and CLI versions**, allowing flexibility for different workflows.

---

## ✨ Features

- 🔍 Subdomain enumeration using **subfinder + amass**
- 🌐 Live host detection via **httpx**
- 🧼 Clean, deduplicated output
- 📁 Domain-based result structure
- 🖥️ GUI mode for ease of use
- 🧑‍💻 CLI mode for automation & scripting
- ⚡ Passive-first, low-noise recon
- 🧠 Designed using real bug bounty best practices

---

## 🖥️ Modes

### GUI Mode
- Button-based interface
- Ideal for beginners and visual workflows

Run:
```bash
python3 lex_gui.py

CLI Mode

    Fast and scriptable

    Feels like professional tools (subfinder, amass, etc.)

Run:

chmod +x lex.py
./lex.py -d example.com --subdomains

📁 Output Structure

results/
 └── example.com/
     └── live_subdomains.txt

🛠 Requirements

    Python 3.8+

    subfinder

    amass

    httpx

Install tools before running LΞX.
👤 Author

Omar Abdelsalam
⚠️ Disclaimer

This tool is intended only for authorized security testing.
Do not use it against systems you do not own or have explicit permission to test.
🚀 Roadmap (Planned)

    --all recon flag

    URL & JS file discovery

    Parameter enumeration

    Colored CLI output

    Dark GUI theme

    Windows .exe release

    Docker support

⭐ If you find LΞX useful, consider starring the repo.


