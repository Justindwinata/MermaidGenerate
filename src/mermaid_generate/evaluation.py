"""Basic evaluation utilities for MermaidGenerate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable

from .mermaid_validator import (
    infer_diagram_type,
    normalize_for_assignment,
    strip_markdown_fences,
    validate_mermaid_code,
)


@dataclass
class EvaluationMetrics:
    total: int
    syntax_validity_rate: float
    diagram_type_accuracy: float
    prefix_accuracy: float
    exact_match_rate: float
    invalid_output_count: int
    markdown_fence_violation_count: int

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def normalize_exact(text: str) -> str:
    lines = [
        " ".join(line.strip().split())
        for line in normalize_for_assignment(text).splitlines()
        if line.strip()
    ]
    return "\n".join(lines)


def evaluate_predictions(
    references: list[dict[str, str]],
    predictions: list[str],
) -> EvaluationMetrics:
    total = len(references)
    if total != len(predictions):
        raise ValueError("references and predictions must have the same length")
    if total == 0:
        return EvaluationMetrics(0, 0.0, 0.0, 0.0, 0.0, 0, 0)

    valid_count = 0
    type_count = 0
    prefix_count = 0
    exact_count = 0
    fence_count = 0

    for sample, prediction in zip(references, predictions):
        expected_type = sample["diagram_type"]
        result = validate_mermaid_code(prediction, expected_type=expected_type)
        cleaned_prediction = normalize_for_assignment(strip_markdown_fences(prediction))
        predicted_type = infer_diagram_type(cleaned_prediction)
        if result.valid:
            valid_count += 1
        if predicted_type == expected_type:
            type_count += 1
        if cleaned_prediction.lstrip().lower().startswith(expected_type):
            prefix_count += 1
        if "```" in prediction:
            fence_count += 1
        if normalize_exact(sample["target"]) == normalize_exact(prediction):
            exact_count += 1

    return EvaluationMetrics(
        total=total,
        syntax_validity_rate=valid_count / total,
        diagram_type_accuracy=type_count / total,
        prefix_accuracy=prefix_count / total,
        exact_match_rate=exact_count / total,
        invalid_output_count=total - valid_count,
        markdown_fence_violation_count=fence_count,
    )


def run_manual_test_set(
    samples: list[dict[str, str]],
    generate_fn: Callable[[str, str], str],
) -> dict[str, object]:
    predictions = [
        generate_fn(sample["prompt"], sample["diagram_type"])
        for sample in samples
    ]
    metrics = evaluate_predictions(samples, predictions)
    return {
        "metrics": metrics.as_dict(),
        "predictions": predictions,
    }
