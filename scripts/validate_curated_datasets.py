"""Validate curated MermaidGenerate datasets and print a compact report."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mermaid_generate.dataset_validator import validate_dataset_file


DEFAULT_DATASETS = [
    ROOT / "datasets" / "curated" / "mindmap_curated.jsonl",
    ROOT / "datasets" / "curated" / "venn_curated.jsonl",
    ROOT / "datasets" / "curated" / "mixed_mindmap_venn_curated.jsonl",
]


def summarize(path: Path) -> dict[str, object]:
    path = path if path.is_absolute() else ROOT / path
    path = path.resolve()
    report = validate_dataset_file(path)
    language_counts = Counter(
        sample.get("language", "unknown")
        for sample in report.valid_data
    )
    try:
        display_path = str(path.relative_to(ROOT))
    except ValueError:
        display_path = str(path)
    return {
        "file": display_path,
        "total_samples": report.total_samples,
        "valid_samples": report.valid_samples,
        "invalid_samples": report.invalid_samples,
        "warning_samples": report.warning_samples,
        "diagram_type_counts": report.diagram_type_counts,
        "language_counts": dict(language_counts),
        "duplicate_count": report.duplicate_count,
        "train_ready": report.train_ready,
        "error": report.error,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate MermaidGenerate curated datasets."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=DEFAULT_DATASETS,
        help="Dataset paths to validate.",
    )
    args = parser.parse_args()

    failed = False
    for path in args.paths:
        summary = summarize(path)
        print(summary)
        if summary["invalid_samples"] or summary["duplicate_count"] or summary["error"]:
            failed = True
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
