# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from argparse import ArgumentParser
from contextlib import nullcontext
import json
import sys

from .config import ConfigLoader


def _open_or_std(filename, std, encoding="utf-8", mode="r"):
    """Open `filename` or std (if `filename` is '-')"""
    if filename == "-":
        return nullcontext(std)
    return open(filename, encoding=encoding, mode=mode)


def open_file_or_stdin(filename, encoding="utf-8", mode="r"):
    """Open `filename` or stdin (if `filename` is '-')"""
    return _open_or_std(filename, sys.stdin, encoding, mode)


def open_file_or_stdout(filename, encoding="utf-8", mode="w"):
    """Open `filename` or stdout (if `filename` is '-') for writing."""
    return _open_or_std(filename, sys.stdout, encoding, mode)


def main():
    ap = ArgumentParser(description=main.__doc__)
    ap.add_argument(
        "-p",
        "--path",
        default=False,
        type=str,
        help="path to extract from config file",
    )
    ap.add_argument(
        "-i",
        "--indent",
        default=False,
        action="store_true",
        help="pretty-print JSON output",
    )
    ap.add_argument(
        "-e",
        "--env",
        help="env var to load config from. Overrides --file",
    )
    ap.add_argument(
        "-o",
        "--output",
        default="-",
        help='output filename, or stdout if "-" (default)',
    )
    ap.add_argument(
        "file",
        default="-",
        nargs="?",
        help='input filename, or stdin if "-" (default). Ignored if --env is set',
    )
    args = ap.parse_args()
    cfg = ConfigLoader()
    with open_file_or_stdout(args.output) as fod:
        if args.env:
            res = cfg.load(args.env)
        else:
            with open_file_or_stdin(args.file) as fid:
                res = cfg.load(fobj=fid)

        if args.path:
            res = res[args.path]

        if args.indent:
            output = json.dumps(res, indent=4)
        else:
            output = json.dumps(res)

        fod.write(output)
        fod.write("\n")


if __name__ == "__main__":
    main()
