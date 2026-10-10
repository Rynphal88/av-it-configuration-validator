"""Environment-backed runtime configuration for the validator."""

from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigurationError(ValueError):
    """Raised when a runtime setting is unsupported or unsafe."""


@dataclass(frozen=True)
class Settings:
    """Validated runtime settings with conservative local defaults."""

    max_scene_bytes: int = 2_000_000
    output_format: str = "text"

    @classmethod
    def from_env(cls) -> Settings:
        raw_max = os.getenv("AV_VALIDATOR_MAX_SCENE_BYTES", "2000000")
        raw_format = os.getenv("AV_VALIDATOR_OUTPUT_FORMAT", "text").lower()
        try:
            max_scene_bytes = int(raw_max)
        except ValueError as exc:
            raise ConfigurationError(
                "AV_VALIDATOR_MAX_SCENE_BYTES must be a positive integer"
            ) from exc
        if max_scene_bytes <= 0:
            raise ConfigurationError(
                "AV_VALIDATOR_MAX_SCENE_BYTES must be a positive integer"
            )
        if raw_format not in {"text", "json"}:
            raise ConfigurationError(
                "AV_VALIDATOR_OUTPUT_FORMAT must be either text or json"
            )
        return cls(max_scene_bytes=max_scene_bytes, output_format=raw_format)
