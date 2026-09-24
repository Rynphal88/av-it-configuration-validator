"""Read-only input checks for scene files used by the prototype."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


class InputIntegrityError(ValueError):
    """Raised when an input file fails a documented integrity check."""


@dataclass(frozen=True)
class SceneArtifact:
    path: Path
    text: str
    size_bytes: int
    sha256: str


def read_scene_file(path: str | Path, *, max_bytes: int = 2_000_000) -> SceneArtifact:
    """Read an allowlisted scene file without changing it."""

    scene_path = Path(path)
    if scene_path.suffix.lower() != ".scn":
        raise InputIntegrityError("scene input must use the .scn extension")
    if not scene_path.is_file():
        raise InputIntegrityError(f"scene input does not exist: {scene_path}")

    raw = scene_path.read_bytes()
    if len(raw) > max_bytes:
        raise InputIntegrityError("scene input exceeds the configured size limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InputIntegrityError("scene input is not valid UTF-8 text") from exc

    return SceneArtifact(
        path=scene_path,
        text=text,
        size_bytes=len(raw),
        sha256=sha256(raw).hexdigest(),
    )
