"""Load declarative validation rules against an approved baseline."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from typing import Mapping

from .models import Rule, Severity


class RuleCatalogError(ValueError):
    """Raised when a rule catalog is malformed or incomplete."""


def load_rules(
    path: str | Path, baseline: Mapping[str, tuple[str, ...]]
) -> tuple[list[Rule], str]:
    """Create rules whose expected values come from the approved baseline."""

    catalog_path = Path(path)
    raw = catalog_path.read_bytes()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuleCatalogError("rule catalog is not valid UTF-8 JSON") from exc

    entries = payload.get("rules") if isinstance(payload, dict) else None
    if not isinstance(entries, list) or not entries:
        raise RuleCatalogError("rule catalog must contain a non-empty rules list")

    rules: list[Rule] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise RuleCatalogError(f"rule {index} must be an object")
        required = ("id", "name", "path", "severity", "rationale")
        missing = [field for field in required if not isinstance(entry.get(field), str)]
        if missing:
            raise RuleCatalogError(f"rule {index} has missing or invalid fields: {', '.join(missing)}")
        if entry["id"] in seen_ids:
            raise RuleCatalogError(f"duplicate rule id: {entry['id']}")
        if entry["path"] not in baseline:
            raise RuleCatalogError(
                f"baseline does not define the protected path for {entry['id']}: {entry['path']}"
            )
        try:
            severity = Severity(entry["severity"])
        except ValueError as exc:
            raise RuleCatalogError(
                f"rule {entry['id']} uses an unsupported severity: {entry['severity']}"
            ) from exc
        seen_ids.add(entry["id"])
        rules.append(
            Rule(
                rule_id=entry["id"],
                name=entry["name"],
                path=entry["path"],
                expected=baseline[entry["path"]],
                severity=severity,
                rationale=entry["rationale"],
            )
        )
    return rules, sha256(raw).hexdigest()
