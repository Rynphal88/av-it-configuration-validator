"""Command-line interface for the integrated validator."""

from __future__ import annotations

import argparse
import sys

from .catalog import RuleCatalogError
from .config import ConfigurationError, Settings
from .integrity import InputIntegrityError
from .parser import SceneParseError
from .reporting import format_json_report, format_text_report
from .service import validate_configuration


def build_parser(settings: Settings | None = None) -> argparse.ArgumentParser:
    settings = settings or Settings()
    parser = argparse.ArgumentParser(
        description="Read-only validation of a sanitized X32 scene against an approved baseline."
    )
    parser.add_argument("--candidate", required=True, help="candidate .scn file")
    parser.add_argument("--baseline", required=True, help="approved baseline .scn file")
    parser.add_argument("--rules", required=True, help="declarative JSON rule catalog")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default=settings.output_format,
        help="report format (default: environment setting or text)",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=settings.max_scene_bytes,
        help="maximum bytes accepted for each scene file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        settings = Settings.from_env()
        args = build_parser(settings).parse_args(argv)
        if args.max_bytes <= 0:
            raise ConfigurationError("--max-bytes must be a positive integer")
        report = validate_configuration(
            args.candidate,
            args.baseline,
            args.rules,
            max_scene_bytes=args.max_bytes,
        )
    except (
        ConfigurationError,
        InputIntegrityError,
        SceneParseError,
        RuleCatalogError,
        OSError,
    ) as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 1

    formatter = format_json_report if args.format == "json" else format_text_report
    print(formatter(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
