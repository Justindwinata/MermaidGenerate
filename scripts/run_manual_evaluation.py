"""Run manual MermaidGenerate evaluation.

Default mode is validator-only so it can run on local CPU without downloading a
model. Use --mode model in Colab/GPU when actual Transformers inference should
be measured.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mermaid_generate.evaluation import evaluate_predictions
from mermaid_generate.inference import GenerationSettings, generate_mermaid
from mermaid_generate.mermaid_validator import validate_mermaid_code
from mermaid_generate.model_loader import load_base_model


def load_eval_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def validator_only(rows: list[dict[str, Any]]) -> tuple[list[str], dict[str, Any]]:
    predictions = [row["reference_target"] for row in rows]
    references = [
        {
            "diagram_type": row["diagram_type"],
            "target": row["reference_target"],
        }
        for row in rows
    ]
    metrics = evaluate_predictions(references, predictions).as_dict()
    invalid_references = [
        {
            "id": row["id"],
            "message": validate_mermaid_code(
                row["reference_target"],
                row["diagram_type"],
            ).message(),
        }
        for row in rows
        if not validate_mermaid_code(row["reference_target"], row["diagram_type"]).valid
    ]
    return predictions, {
        "mode": "validator-only",
        "model_inference_executed": False,
        "metrics": metrics,
        "invalid_references": invalid_references,
        "note": "Reference targets were validated locally; model quality was not measured.",
    }


def model_mode(
    rows: list[dict[str, Any]],
    model_id: str,
    max_samples: int | None,
) -> tuple[list[str], dict[str, Any]]:
    selected = rows[:max_samples] if max_samples else rows
    load_base_model(model_id=model_id)
    predictions: list[str] = []
    started = time.perf_counter()
    for row in selected:
        result = generate_mermaid(
            row["prompt"],
            row["diagram_type"],
            GenerationSettings(max_new_tokens=320, temperature=0.2),
        )
        predictions.append(result.code)
    elapsed = time.perf_counter() - started
    references = [
        {"diagram_type": row["diagram_type"], "target": row["reference_target"]}
        for row in selected
    ]
    metrics = evaluate_predictions(references, predictions).as_dict()
    return predictions, {
        "mode": "model",
        "model_inference_executed": True,
        "model_id": model_id,
        "sample_count": len(selected),
        "duration_seconds": elapsed,
        "metrics": metrics,
        "note": "Metrics are from actual Transformers/PyTorch inference.",
    }


def write_outputs(
    rows: list[dict[str, Any]],
    predictions: list[str],
    summary: dict[str, Any],
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": summary,
        "items": [
            {
                "id": row["id"],
                "diagram_type": row["diagram_type"],
                "prompt": row["prompt"],
                "reference_target": row["reference_target"],
                "prediction": prediction,
            }
            for row, prediction in zip(rows, predictions)
        ],
    }
    path = output_dir / f"manual_evaluation_{summary['mode']}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_docs_report(summary: dict[str, Any], output_path: Path) -> None:
    report = [
        "# Evaluation Baseline Report",
        "",
        "Validation date: 2026-07-22 Asia/Jakarta",
        "",
        f"- Mode: `{summary['mode']}`",
        f"- Model inference executed: `{summary['model_inference_executed']}`",
        f"- Output artifact: `{output_path}`",
        f"- Metrics: `{summary['metrics']}`",
        "",
        "## Notes",
        "",
        summary["note"],
        "",
        "Local MG-0002 baseline ran validator-only because full model inference and before/after LoRA evaluation should be executed in Colab/GPU for honest timing and memory behavior.",
        "",
        "Before/after LoRA results must be added only after a real LoRA smoke training run completes.",
    ]
    (ROOT / "docs" / "EVALUATION_BASELINE_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MermaidGenerate manual evaluation.")
    parser.add_argument(
        "--eval-path",
        type=Path,
        default=ROOT / "datasets" / "evaluation" / "manual_eval_prompts.jsonl",
    )
    parser.add_argument(
        "--mode",
        choices=["validator-only", "model"],
        default="validator-only",
    )
    parser.add_argument("--model-id", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "outputs" / "evaluation",
    )
    parser.add_argument("--write-docs-report", action="store_true")
    args = parser.parse_args()

    rows = load_eval_rows(args.eval_path)
    if args.mode == "validator-only":
        predictions, summary = validator_only(rows)
    else:
        predictions, summary = model_mode(rows, args.model_id, args.max_samples)

    output_path = write_outputs(rows[: len(predictions)], predictions, summary, args.output_dir)
    if args.write_docs_report:
        write_docs_report(summary, output_path)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("saved:", output_path)


if __name__ == "__main__":
    main()
