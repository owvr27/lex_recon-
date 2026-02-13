import os
import json
from datetime import datetime
from modules import subdomains, urls, js, params
from core.utils import ensure_dir, count_lines
from core.report import build_report

BASE_RESULTS = "results"


def run(domain, mode):
    print(f"\n[+] Target: {domain}")
    print(f"[+] Mode: {mode}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = os.path.join(BASE_RESULTS, f"{domain}_{timestamp}")
    ensure_dir(target_dir)

    results = {}

    # --- SUBDOMAIN PHASE ---
    brute = False
    if mode == "deep":
        brute = True

    print("[*] Running subdomain discovery...")
    results["subs"] = subdomains.run(
        domain,
        passive=True,
        brute=brute,
        live=True
    )

    # SMART escalation
    if mode == "smart":
        sub_count = count_lines(results["subs"]["all"])
        if sub_count < 50:
            print("[!] Low subdomain count detected — escalating to brute mode")
            results["subs"] = subdomains.run(
                domain,
                passive=True,
                brute=True,
                live=True
            )

    # --- URL COLLECTION ---
    print("[*] Collecting URLs...")
    results["urls"] = urls.run(domain)

    # --- JS ANALYSIS ---
    print("[*] Extracting JS endpoints...")
    results["js"] = js.run(domain)

    # --- PARAM DISCOVERY ---
    print("[*] Discovering parameters...")
    results["params"] = params.run(domain)

    # --- REPORTING ---
    print("[*] Building final report...")
    report = build_report(domain, results, target_dir)

    with open(os.path.join(target_dir, "report.json"), "w") as f:
        json.dump(report, f, indent=4)

    print(f"\n[✓] Recon complete.")
    print(f"[✓] Results saved to: {target_dir}")
