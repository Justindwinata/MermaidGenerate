"""Small shared utilities for MermaidGenerate."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any


def stable_id(*parts: str) -> str:
    payload = "\n".join(parts).encode("utf-8", errors="replace")
    return hashlib.sha256(payload).hexdigest()[:16]


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def compact_text(value: Any) -> str:
    text = "" if value is None else str(value)
    return re.sub(r"\s+", " ", text).strip()


def infer_language(text: str) -> str:
    lowered = f" {text.lower()} "
    id_markers = [
        " tentang ",
        " buat ",
        " jelaskan ",
        " siswa ",
        " pekerja ",
        " umkm ",
        " pendidikan ",
        " kesehatan ",
    ]
    en_markers = [
        " about ",
        " create ",
        " explain ",
        " students ",
        " workers ",
        " education ",
        " health ",
        " business ",
    ]
    id_score = sum(marker in lowered for marker in id_markers)
    en_score = sum(marker in lowered for marker in en_markers)
    if id_score > en_score:
        return "id"
    if en_score > id_score:
        return "en"
    return "unknown"


def infer_complexity(target: str) -> str:
    non_empty_lines = [
        line for line in target.splitlines() if line.strip()
    ]
    if len(non_empty_lines) <= 5:
        return "simple"
    if len(non_empty_lines) <= 12:
        return "medium"
    return "complex"


def infer_domain(prompt: str) -> str:
    lowered = prompt.lower()
    domains = {
        "education": ["learning", "school", "student", "education", "kelas", "siswa", "belajar"],
        "business": ["business", "startup", "marketing", "umkm", "sales", "customer"],
        "technology": ["ai", "software", "cloud", "data", "cyber", "teknologi", "aplikasi"],
        "health": ["health", "wellness", "medical", "kesehatan", "gizi", "mental"],
    }
    for domain, markers in domains.items():
        if any(marker in lowered for marker in markers):
            return domain
    return "general"
