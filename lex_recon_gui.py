import os

def ensure_tools():
    os.makedirs("tools", exist_ok=True)

    if not os.path.exists("tools/LinkFinder"):
        print("[+] Downloading LinkFinder...")
        os.system(
            "git clone https://github.com/GerbenJavado/LinkFinder tools/LinkFinder"
        )

    if not os.path.exists("tools/ParamSpider"):
        print("[+] Downloading ParamSpider...")
        os.system(
            "git clone https://github.com/devanshbatham/ParamSpider tools/ParamSpider"
        )

ensure_tools()
