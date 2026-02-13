
#!/usr/bin/env python3
import argparse
from core.engine import run

BANNER = r"""
██╗     ███████╗██╗  ██╗
██║     ██╔════╝╚██╗██╔╝
██║     █████╗   ╚███╔╝
██║     ██╔══╝   ██╔██╗
███████╗███████╗██╔╝ ██╗
╚══════╝╚══════╝╚═╝  ╚═╝

        LexRecon v3
"""

print(BANNER)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", required=True)
parser.add_argument("--fast", action="store_true")
parser.add_argument("--deep", action="store_true")
parser.add_argument("--smart", action="store_true")

args = parser.parse_args()

mode = "smart"
if args.fast: mode = "fast"
if args.deep: mode = "deep"

run(args.domain, mode, vars(args))
