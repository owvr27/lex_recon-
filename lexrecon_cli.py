#!/usr/bin/env python3
import argparse
import sys
from core.engine import run
from core.deps import check_dependencies

BANNER = r"""
██╗     ███████╗██╗  ██╗
██║     ██╔════╝╚██╗██╔╝
██║     █████╗   ╚███╔╝
██║     ██╔══╝   ██╔██╗
███████╗███████╗██╔╝ ██╗
╚══════╝╚══════╝╚═╝  ╚═╝

        LexRecon v4
"""

print(BANNER)

parser = argparse.ArgumentParser(description="LexRecon v4 - Professional Recon Framework")

parser.add_argument("-d", "--domain", required=True, help="Target domain")
parser.add_argument("--fast", action="store_true", help="Fast passive mode")
parser.add_argument("--deep", action="store_true", help="Deep mode (includes brute)")
parser.add_argument("--smart", action="store_true", help="Smart adaptive mode")
parser.add_argument("--check", action="store_true", help="Check dependencies and exit")

args = parser.parse_args()

if args.check:
    check_dependencies()
    sys.exit(0)

mode = "smart"
if args.fast:
    mode = "fast"
elif args.deep:
    mode = "deep"

run(args.domain, mode)
