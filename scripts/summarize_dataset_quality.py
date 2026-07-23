"""Create JSON and Markdown quality reports for expanded datasets."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_expanded_dataset import validate_all


REPORT_DIR = ROOT / "results" / "dataset_quality"
SUMMARY_JSON = REPORT_DIR / "expanded_dataset_summary.json"
SUMMARY_MD = REPORT_DIR / "expanded_dataset_summary.md"


def _recommendation(dataset: dict[str, Any]) -> str:
    total = int(dataset["total"])
    if total <= 500:
        return "Use for faster LoRA training and iteration."
    return "Use when there is enough Colab time for stronger LoRA training."


def build_summary() -> dict[str, Any]:
    validation = validate_all()
    datasets = []
    for item in validation["datasets"]:
        datasets.append(
            {
                "file": item["file"],
                "total_examples": item["total"],
                "mindmap_count": item["diagram_type_counts"].get("mindmap", 0),
                "venn_count": item["diagram_type_counts"].get("venn", 0),
                "language_distribution": item["language_counts"],
                "domain_distribution": item["domain_counts"],
                "average_prompt_length": item["average_prompt_length"],
                "average_completion_length": item["average_completion_length"],
                "duplicate_prompt_count": item["duplicate_prompts"],
                "duplicate_completion_count": item["duplicate_completions"],
                "invalid_count": item["invalid_samples"] + item["mermaid_invalid_count"],
                "warning_count": item["warning_samples"],
                "venn_undefined_union_count": item["venn_undefined_union_count"],
                "mindmap_missing_root_count": item["mindmap_missing_root_count"],
                "balanced": item["balanced"],
                "pass": item["pass"],
                "recommendation": _recommendation(item),
                "sample_examples": item["sample_rows"][:2],
            }
        )
    return {
        "generated_on": date.today().isoformat(),
        "all_passed": validation["all_passed"],
        "datasets": datasets,
        "demo_recommendation": {
            "quick_smoke": "datasets/curated/mixed_mindmap_venn_curated.jsonl",
            "medium_training": "datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl",
            "larger_training": "datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl",
        },
    }


def write_markdown(summary: dict[str, Any]) -> None:
    lines = [
        "# Expanded Dataset Quality Summary",
        "",
        f"Generated on: {summary['generated_on']}",
        f"Overall status: {'PASS' if summary['all_passed'] else 'FAIL'}",
        "",
        "## Dataset Results",
        "",
        "| File | Total | Mind Map | Venn | Invalid | Warnings | Prompt Dupes | Completion Dupes | Balanced |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in summary["datasets"]:
        lines.append(
            "| {file} | {total_examples} | {mindmap_count} | {venn_count} | {invalid_count} | "
            "{warning_count} | {duplicate_prompt_count} | {duplicate_completion_count} | {balanced} |".format(
                **item
            )
        )
    lines.extend(
        [
            "",
            "## Recommended Use",
            "",
            "- Quick Colab smoke test: `datasets/curated/mixed_mindmap_venn_curated.jsonl`.",
            "- Medium LoRA training: `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`.",
            "- Larger LoRA training: `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`.",
            "",
            "The expanded datasets are deterministic and validated against the project Mermaid validator. The mixed datasets are balanced 50/50, while the mindmap-only and Venn-only files are intentionally single-diagram-type datasets. They improve coverage, but final model quality still depends on GPU resources, training time, and model capacity.",
        ]
    )
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    summary = build_summary()
    SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(summary)
    print(f"Wrote {SUMMARY_JSON.relative_to(ROOT)}")
    print(f"Wrote {SUMMARY_MD.relative_to(ROOT)}")
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
