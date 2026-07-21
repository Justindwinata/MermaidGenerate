"""Utilities used by the Colab notebook."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_src_path(project_root: str | Path = ".") -> Path:
    root = Path(project_root).resolve()
    src = root / "src"
    if src.exists() and str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return src


def in_colab() -> bool:
    try:
        import google.colab  # noqa: F401
    except ImportError:
        return False
    return True
