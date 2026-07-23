"""Run final MermaidGenerate quality evaluation.

Validator-only mode is intentionally lightweight: it validates dataset
completions and prompt coverage without downloading a model. Model mode is
available for Colab/GPU runs and records real inference results only when used.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_expanded_dataset import analyze_dataset


EVAL_PROMPTS = ROOT / "datasets" / "evaluation" / "final_eval_prompts_100.jsonl"
REFERENCE_DATASET = ROOT / "datasets" / "expanded" / "mixed_mindmap_venn_expanded_1000.jsonl"
OUTPUT_PATH = ROOT / "results" / "evaluation" / "final_eval_baseline.json"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def summarize_eval_prompts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    prompt_values = [str(row.get("prompt") or "").strip() for row in rows]
    return {
        "file": str(EVAL_PROMPTS.relative_to(ROOT)),
        "total_prompts": len(rows),
        "diagram_type_counts": dict(sorted(Counter(str(row.get("diagram_type") or "") for row in rows).items())),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "unknown") for row in rows).items())),
        "domain_counts": dict(sorted(Counter(str(row.get("domain") or "unknown") for row in rows).items())),
        "duplicate_prompt_count": len(prompt_values) - len(set(prompt_values)),
        "empty_prompt_count": sum(1 for prompt in prompt_values if not prompt),
    }


def validator_only() -> dict[str, Any]:
    prompt_rows = load_jsonl(EVAL_PROMPTS)
    dataset_result = analyze_dataset(REFERENCE_DATASET)
    prompt_summary = summarize_eval_prompts(prompt_rows)
    pass_status = (
        dataset_result["pass"]
        and prompt_summary["total_prompts"] == 100
        and prompt_summary["diagram_type_counts"].get("mindmap") == 50
        and prompt_summary["diagram_type_counts"].get("venn") == 50
        and prompt_summary["duplicate_prompt_count"] == 0
        and prompt_summary["empty_prompt_count"] == 0
    )
    return {
        "mode": "validator-only",
        "model_inference_executed": False,
        "reference_dataset": {
            "file": dataset_result["file"],
            "total": dataset_result["total"],
            "diagram_type_counts": dataset_result["diagram_type_counts"],
            "invalid_samples": dataset_result["invalid_samples"],
            "warning_samples": dataset_result["warning_samples"],
            "mermaid_invalid_count": dataset_result["mermaid_invalid_count"],
            "duplicate_prompt_count": dataset_result["duplicate_prompts"],
            "duplicate_completion_count": dataset_result["duplicate_completions"],
            "venn_undefined_union_count": dataset_result["venn_undefined_union_count"],
            "mindmap_missing_root_count": dataset_result["mindmap_missing_root_count"],
            "pass": dataset_result["pass"],
        },
        "evaluation_prompts": prompt_summary,
        "pass": pass_status,
        "note": "Validator-only mode checks syntax safety and evaluation prompt coverage. It does not measure model quality.",
    }


def model_mode(max_samples: int, model_id: str) -> dict[str, Any]:
    from src.mermaid_generate.inference import GenerationSettings, generate_mermaid
    from src.mermaid_generate.model_loader import load_base_model

    rows = load_jsonl(EVAL_PROMPTS)[:max_samples]
    load_base_model(model_id=model_id)
    started = time.perf_counter()
    items: list[dict[str, Any]] = []
    valid_count = 0
    fallback_count = 0
    for row in rows:
        result = generate_mermaid(
            str(row["prompt"]),
            str(row["diagram_type"]),
            GenerationSettings(max_new_tokens=320, temperature=0.2, top_p=0.85),
        )
        if result.validation.valid:
            valid_count += 1
        if result.fallback_used:
            fallback_count += 1
        items.append(
            {
                "id": row["id"],
                "diagram_type": row["diagram_type"],
                "prompt": row["prompt"],
                "final_code": result.code,
                "valid": result.validation.valid,
                "fallback_used": result.fallback_used,
                "repair_status": result.repair_status,
            }
        )
    elapsed = time.perf_counter() - started
    return {
        "mode": "model",
        "model_inference_executed": True,
        "model_id": model_id,
        "sample_count": len(rows),
        "duration_seconds": round(elapsed, 2),
        "syntax_validity_rate": valid_count / len(rows) if rows else 0,
        "fallback_rate": fallback_count / len(rows) if rows else 0,
        "items": items,
        "pass": valid_count == len(rows),
        "note": "Model mode uses real Transformers/PyTorch inference and should be run in Colab/GPU when possible.",
    }


def write_result(payload: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final MermaidGenerate quality evaluation.")
    parser.add_argument("--validator-only", action="store_true", help="Run syntax and prompt coverage checks only.")
    parser.add_argument("--model", action="store_true", help="Run real model inference. Use this in Colab/GPU.")
    parser.add_argument("--max-samples", type=int, default=20)
    parser.add_argument("--model-id", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    parser.add_argument("--output-path", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if args.model:
        payload = model_mode(args.max_samples, args.model_id)
    else:
        payload = validator_only()

    write_result(payload, args.output_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"saved: {args.output_path.relative_to(ROOT)}")
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
