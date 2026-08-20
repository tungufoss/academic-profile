"""Command-line entry points for academic-profile."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from academic_profile import __version__
from academic_profile.reporting import SchemeError
from academic_profile.schemes import available_schemes, load_scheme


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="academic-profile",
        description="Public-safe academic profile data helpers.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subcommands = parser.add_subparsers(dest="command")
    subcommands.add_parser("doctor", help="print a minimal installation check")

    schemes = subcommands.add_parser("schemes", help="validate and summarize bundled reporting schemes")
    schemes.add_argument("name", nargs="?", help="reporting scheme name; omit to list all bundled schemes")
    schemes.add_argument(
        "--review-notes",
        action="store_true",
        help="also print entries whose interpretation still needs human review",
    )
    return parser


def _run_schemes(name: str | None, show_review_notes: bool) -> int:
    """Validate bundled scheme data and print a machine-readable summary."""

    names = available_schemes() if name is None else (name,)
    payload: list[dict[str, object]] = []

    for scheme_name in names:
        try:
            scheme = load_scheme(scheme_name)
        except SchemeError as error:
            print(json.dumps({"scheme": scheme_name, "status": "invalid", "error": str(error)}, ensure_ascii=False))
            return 1

        summary: dict[str, object] = {"plugin": scheme_name, **scheme.summary()}
        if show_review_notes:
            summary["review_notes"] = list(scheme.review_notes)
            summary["entry_review_notes"] = [
                {"code": entry.code, "review_note": entry.review_note}
                for entry in scheme.entries_needing_review()
            ]
        payload.append(summary)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        print(json.dumps({"package": "academic-profile", "version": __version__, "status": "ok"}))
        return 0

    if args.command == "schemes":
        return _run_schemes(args.name, args.review_notes)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
