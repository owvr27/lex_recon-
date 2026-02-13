from __future__ import annotations
import shutil
from dataclasses import dataclass
from typing import List

REQUIRED = ["subfinder", "assetfinder", "httpx", "gau", "waybackurls"]
OPTIONAL = ["ffuf", "katana"]

@dataclass
class DependencyReport:
    missing_required: List[str]
    missing_optional: List[str]

def check_dependencies() -> DependencyReport:
    missing_required = [t for t in REQUIRED if shutil.which(t) is None]
    missing_optional = [t for t in OPTIONAL if shutil.which(t) is None]
    return DependencyReport(missing_required, missing_optional)

def print_dependency_report(rep: DependencyReport) -> None:
    print("\n[+] Dependency check\n")
    for t in REQUIRED:
        ok = (t not in rep.missing_required)
        print(f"{'[✓]' if ok else '[✗]'} {t}" + ("" if ok else " (missing)"))

    print("\nOptional:")
    for t in OPTIONAL:
        ok = (t not in rep.missing_optional)
        print(f"{'[✓]' if ok else '[!]'} {t}" + ("" if ok else " (optional missing)"))

    if rep.missing_required:
        print("\n[!] Missing required tools:", ", ".join(rep.missing_required))
