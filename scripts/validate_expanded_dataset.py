"""Validate expanded MermaidGenerate datasets with strict quality checks."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.mermaid_generate.dataset_loader import load_and_normalize_dataset, load_raw_records
from src.mermaid_generate.dataset_validator import validate_dataset_file
from src.mermaid_generate.mermaid_validator import validate_mermaid_code


DATASET_PATHS = (
    ROOT / "datasets" / "expanded" / "mindmap_expanded.jsonl",
    ROOT / "datasets" / "expanded" / "venn_expanded.jsonl",
    ROOT / "datasets" / "expanded" / "mixed_mindmap_venn_expanded_500.jsonl",
    ROOT / "datasets" / "expanded" / "mixed_mindmap_venn_expanded_1000.jsonl",
)


def _counter_dict(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def _raw_duplicate_count(records: list[dict[str, Any]], field: str) -> int:
    values = [str(record.get(field) or "").strip() for record in records]
    counts = Counter(values)
    return sum(count - 1 for value, count in counts.items() if value and count > 1)


def analyze_dataset(path: Path) -> dict[str, Any]:
    raw_records = load_raw_records(path)
    normalized = load_and_normalize_dataset(path)
    report = validate_dataset_file(path)

    mermaid_invalid_rows: list[dict[str, Any]] = []
    venn_undefined_union = 0
    mindmap_missing_root = 0
    markdown_fence_count = 0

    for index, sample in enumerate(normalized):
        target = str(sample.get("target") or "")
        expected = str(sample.get("diagram_type") or "auto")
        validation = validate_mermaid_code(target, expected_type=expected)
        if "```" in target:
            markdown_fence_count += 1
        if sample.get("diagram_type") == "mindmap" and "root" not in target.lower():
            mindmap_missing_root += 1
        if sample.get("diagram_type") == "venn" and any(
            "undefined set" in error.lower() for error in validation.errors
        ):
            venn_undefined_union += 1
        if not validation.valid:
            mermaid_invalid_rows.append(
                {
                    "row_index": index,
                    "id": sample.get("id"),
                    "diagram_type": sample.get("diagram_type"),
                    "errors": validation.errors,
                }
            )

    diagram_counts = _counter_dict([str(item.get("diagram_type") or "") for item in normalized])
    language_counts = _counter_dict([str(item.get("language") or "unknown") for item in normalized])
    domain_counts = _counter_dict([str(item.get("domain") or "unknown") for item in normalized])
    total = len(normalized)
    mindmap_count = diagram_counts.get("mindmap", 0)
    venn_count = diagram_counts.get("venn", 0)
    balance_delta = abs(mindmap_count - venn_count)

    prompt_lengths = [len(str(record.get("prompt") or "")) for record in raw_records]
    completion_lengths = [len(str(record.get("completion") or "")) for record in raw_records]

    result = {
        "file": str(path.relative_to(ROOT)),
        "total": total,
        "valid_samples": report.valid_samples,
        "invalid_samples": report.invalid_samples,
        "warning_samples": report.warning_samples,
        "diagram_type_counts": diagram_counts,
        "language_counts": language_counts,
        "domain_counts": domain_counts,
        "source_format_counts": report.source_format_counts,
        "duplicate_prompt_target_pairs": report.duplicate_count,
        "duplicate_prompts": _raw_duplicate_count(raw_records, "prompt"),
        "duplicate_completions": _raw_duplicate_count(raw_records, "completion"),
        "markdown_fence_count": markdown_fence_count,
        "mermaid_invalid_count": len(mermaid_invalid_rows),
        "venn_undefined_union_count": venn_undefined_union,
        "mindmap_missing_root_count": mindmap_missing_root,
        "balanced": balance_delta <= max(1, total // 20),
        "average_prompt_length": round(sum(prompt_lengths) / total, 2) if total else 0,
        "average_completion_length": round(sum(completion_lengths) / total, 2) if total else 0,
        "sample_rows": raw_records[:3],
        "first_invalid_rows": mermaid_invalid_rows[:10],
    }
    result["pass"] = (
        result["invalid_samples"] == 0
        and result["warning_samples"] == 0
        and result["duplicate_prompt_target_pairs"] == 0
        and result["duplicate_prompts"] == 0
        and result["duplicate_completions"] == 0
        and result["markdown_fence_count"] == 0
        and result["mermaid_invalid_count"] == 0
        and result["venn_undefined_union_count"] == 0
        and result["mindmap_missing_root_count"] == 0
    )
    return result


def validate_all() -> dict[str, Any]:
    datasets = [analyze_dataset(path) for path in DATASET_PATHS]
    return {
        "datasets": datasets,
        "all_passed": all(item["pass"] for item in datasets),
    }


def main() -> int:
    result = validate_all()
    for item in result["datasets"]:
        status = "PASS" if item["pass"] else "FAIL"
        print(
            f"{status} {item['file']}: total={item['total']} "
            f"invalid={item['invalid_samples']} warnings={item['warning_samples']} "
            f"mermaid_invalid={item['mermaid_invalid_count']} "
            f"prompt_dupes={item['duplicate_prompts']} "
            f"completion_dupes={item['duplicate_completions']}"
        )
        if not item["pass"]:
            print(json.dumps(item["first_invalid_rows"], ensure_ascii=False, indent=2))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
