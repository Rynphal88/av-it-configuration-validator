"""Read-only AV/IT configuration-validation scaffold."""

from .engine import evaluate_rules
from .parser import parse_scene_text

__all__ = ["evaluate_rules", "parse_scene_text"]
