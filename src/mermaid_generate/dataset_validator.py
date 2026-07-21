"""Validation report builder for MermaidGenerate datasets."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .dataset_loader import DatasetLoadError, load_and_normalize_dataset


MIN_TARGET_LENGTH = 12
MAX_TARGET_LENGTH = 8000


@dataclass
class RowIssue:
    row_index: int
    sample_id: str
    reasons: list[str]
    prompt: str
    target_preview: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "row_index": self.row_index,
            "id": self.sample_id,
            "reasons": self.reasons,
            "prompt": self.prompt[:180],
            "target_preview": self.target_preview[:220],
        }


@dataclass
class DatasetValidationReport:
    total_samples: int = 0
    valid_samples: int = 0
    invalid_samples: int = 0
    warning_samples: int = 0
    diagram_type_counts: dict[str, int] = field(default_factory=dict)
    source_format_counts: dict[str, int] = field(default_factory=dict)
    duplicate_count: int = 0
    invalid_rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    normalized_preview: list[dict[str, Any]] = field(default_factory=list)
    valid_data: list[dict[str, Any]] = field(default_factory=list)
    train_ready: bool = False
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "total_samples": self.total_samples,
            "valid_samples": self.valid_samples,
            "invalid_samples": self.invalid_samples,
            "warning_samples": self.warning_samples,
            "diagram_type_counts": self.diagram_type_counts,
            "source_format_counts": self.source_format_counts,
            "duplicate_count": self.duplicate_count,
            "invalid_rows": self.invalid_rows[:10],
            "warnings": self.warnings[:10],
            "normalized_preview": self.normalized_preview[:10],
            "train_ready": self.train_ready,
            "error": self.error,
        }


def target_prefix(target: str) -> str:
    stripped = target.lstrip()
    if stripped.lower().startswith("venn-beta"):
        return "venn"
    if stripped.lower().startswith("venn"):
        return "venn"
    if stripped.lower().startswith("mindmap"):
        return "mindmap"
    return ""


def validate_normalized_sample(sample: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    prompt = str(sample.get("prompt") or "").strip()
    target = str(sample.get("target") or "").strip()
    diagram_type = str(sample.get("diagram_type") or "").strip().lower()
    prefix = target_prefix(target)

    if sample.get("source_format") == "unknown":
        errors.append("unsupported source format")
    if not prompt:
        errors.append("prompt is empty")
    if not target:
        errors.append("target is empty")
    if target and not prefix:
        errors.append("target must start with mindmap, venn, or venn-beta")
    if "```" in target:
        errors.append("target contains markdown code fences")
    if diagram_type not in {"mindmap", "venn"}:
        errors.append("diagram_type must be mindmap or venn")
    if prefix and diagram_type in {"mindmap", "venn"} and prefix != diagram_type:
        errors.append("diagram_type does not match target prefix")
    if target and len(target) < MIN_TARGET_LENGTH:
        errors.append("target is too short")
    if len(target) > MAX_TARGET_LENGTH:
        errors.append("target is too long")
    if len(prompt) < 8:
        warnings.append("prompt is very short")

    return errors, warnings


def validate_samples(samples: list[dict[str, Any]]) -> DatasetValidationReport:
    report = DatasetValidationReport(total_samples=len(samples))
    pair_counts = Counter(
        (
            str(sample.get("prompt") or "").strip().lower(),
            str(sample.get("target") or "").strip(),
        )
        for sample in samples
    )

    valid_data: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    invalid_rows: list[dict[str, Any]] = []

    for sample in samples:
        errors, row_warnings = validate_normalized_sample(sample)
        pair_key = (
            str(sample.get("prompt") or "").strip().lower(),
            str(sample.get("target") or "").strip(),
        )
        if pair_counts[pair_key] > 1:
            row_warnings.append("duplicate prompt/target pair")

        if errors:
            invalid_rows.append(
                RowIssue(
                    row_index=int(sample.get("row_index", -1)),
                    sample_id=str(sample.get("id", "")),
                    reasons=errors,
                    prompt=str(sample.get("prompt") or ""),
                    target_preview=str(sample.get("target") or ""),
                ).as_dict()
            )
        else:
            clean_sample = {
                key: value
                for key, value in sample.items()
                if key not in {"raw", "row_index"}
            }
            valid_data.append(clean_sample)
            if row_warnings:
                warnings.append(
                    RowIssue(
                        row_index=int(sample.get("row_index", -1)),
                        sample_id=str(sample.get("id", "")),
                        reasons=row_warnings,
                        prompt=str(sample.get("prompt") or ""),
                        target_preview=str(sample.get("target") or ""),
                    ).as_dict()
                )

    report.valid_data = valid_data
    report.valid_samples = len(valid_data)
    report.invalid_samples = len(invalid_rows)
    report.warning_samples = len(warnings)
    report.invalid_rows = invalid_rows
    report.warnings = warnings
    report.duplicate_count = sum(count - 1 for count in pair_counts.values() if count > 1)
    report.diagram_type_counts = dict(Counter(sample["diagram_type"] for sample in valid_data))
    report.source_format_counts = dict(Counter(sample["source_format"] for sample in valid_data))
    report.normalized_preview = valid_data[:10]
    report.train_ready = report.valid_samples > 0
    return report


def validate_dataset_file(path: str | Path) -> DatasetValidationReport:
    try:
        samples = load_and_normalize_dataset(path)
    except (DatasetLoadError, OSError) as exc:
        return DatasetValidationReport(error=str(exc))
    return validate_samples(samples)
