"""Deterministic, non-executing parser for selected line-oriented scene data."""

from __future__ import annotations

import shlex


class SceneParseError(ValueError):
    """Raised when selected scene content cannot be parsed safely."""


def parse_scene_text(text: str, *, max_chars: int = 2_000_000) -> dict[str, tuple[str, ...]]:
    """Parse path-prefixed lines without executing or modifying their content.

    The prototype accepts only text within a fixed size boundary. Blank lines and
    comment lines are ignored. Duplicate paths are rejected because silently
    overwriting a value would weaken traceability.
    """

    if len(text) > max_chars:
        raise SceneParseError("scene text exceeds the configured size limit")

    parsed: dict[str, tuple[str, ...]] = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith("/"):
            raise SceneParseError(f"line {line_number} does not start with a configuration path")
        try:
            tokens = shlex.split(line, comments=False, posix=True)
        except ValueError as exc:
            raise SceneParseError(f"line {line_number} is malformed") from exc
        if len(tokens) < 2:
            raise SceneParseError(f"line {line_number} has no value")
        path, values = tokens[0], tuple(tokens[1:])
        if path in parsed:
            raise SceneParseError(f"duplicate path at line {line_number}: {path}")
        parsed[path] = values
    return parsed
