"""Run the Unit 6 controlled evaluation and save reproducible JSON evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from av_validator.evaluation import run_controlled_evaluation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the sanitized Unit 6 evaluation corpus."
    )
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = run_controlled_evaluation(args.baseline, args.rules)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "method",
                    "correctness",
                    "performance",
                    "qualitative_usability",
                )
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
