"""Domain models for validation rules and findings."""

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFORMATIONAL = "informational"


@dataclass(frozen=True)
class Rule:
    rule_id: str
    name: str
    path: str
    expected: tuple[str, ...]
    severity: Severity
    rationale: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    name: str
    path: str
    expected: tuple[str, ...]
    observed: tuple[str, ...] | None
    severity: Severity
    rationale: str
