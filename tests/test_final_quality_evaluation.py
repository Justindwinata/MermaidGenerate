from pathlib import Path

from scripts.run_final_quality_evaluation import EVAL_PROMPTS, validator_only


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_final_eval_prompt_file_exists_and_is_balanced() -> None:
    assert EVAL_PROMPTS.exists()

    result = validator_only()
    prompts = result["evaluation_prompts"]

    assert prompts["total_prompts"] == 100
    assert prompts["diagram_type_counts"] == {"mindmap": 50, "venn": 50}
    assert prompts["duplicate_prompt_count"] == 0
    assert prompts["empty_prompt_count"] == 0


def test_validator_only_final_quality_evaluation_passes_without_model() -> None:
    result = validator_only()

    assert result["mode"] == "validator-only"
    assert result["model_inference_executed"] is False
    assert result["reference_dataset"]["total"] == 1000
    assert result["reference_dataset"]["pass"] is True
    assert result["pass"] is True
