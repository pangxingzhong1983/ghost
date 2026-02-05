#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Windows-friendly launcher: keeps a minimal, non-POSIX interface so PyInstaller
can run without termios/pty. Exposes a tiny help and defers to ghostgen when
requested. This is intentionally limited; full interactive shell remains
available on Linux/macOS/Android.
"""

import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ghostwin",
        description="Ghost (Windows limited mode). Use ghostgen to generate payloads."
    )
    parser.add_argument(
        "--ghostgen",
        action="store_true",
        help="Show how to run the payload generator (ghostgen).",
    )
    args = parser.parse_args(argv)

    if args.ghostgen:
        print("Run payload generator with: python -m ghost.cli.ghostgen")
    else:
        print("Ghost Windows build runs in compatibility mode; interactive shell is available on Linux/macOS/Android.")
        print("To generate payloads, run: python -m ghost.cli.ghostgen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
