"""Command-line entry points for academic-profile."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from academic_profile import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="academic-profile",
        description="Public-safe academic profile data helpers.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subcommands = parser.add_subparsers(dest="command")
    subcommands.add_parser("doctor", help="print a minimal installation check")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        print(json.dumps({"package": "academic-profile", "version": __version__, "status": "ok"}))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
