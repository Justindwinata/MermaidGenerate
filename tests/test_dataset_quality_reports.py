import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_dataset_quality_report_exists_and_passes() -> None:
    path = ROOT_DIR / "results" / "dataset_quality" / "expanded_dataset_summary.json"

    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["all_passed"] is True
    assert len(data["datasets"]) == 4
    assert data["demo_recommendation"]["medium_training"].endswith("mixed_mindmap_venn_expanded_500.jsonl")


def test_dataset_quality_report_has_expected_counts() -> None:
    data = json.loads(
        (ROOT_DIR / "results" / "dataset_quality" / "expanded_dataset_summary.json").read_text(
            encoding="utf-8"
        )
    )
    by_file = {item["file"]: item for item in data["datasets"]}

    mixed_1000 = by_file["datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl"]
    assert mixed_1000["total_examples"] == 1000
    assert mixed_1000["mindmap_count"] == 500
    assert mixed_1000["venn_count"] == 500
    assert mixed_1000["invalid_count"] == 0
    assert mixed_1000["duplicate_prompt_count"] == 0
    assert mixed_1000["duplicate_completion_count"] == 0


def test_training_configs_exist_with_required_keys() -> None:
    required = {
        "mode",
        "dataset_path",
        "expected_use_case",
        "epochs",
        "batch_size",
        "gradient_accumulation",
        "max_sequence_length",
        "learning_rate",
        "validation_split",
        "model_id",
    }
    for filename in [
        "lora_smoke_config.json",
        "lora_medium_dataset_config.json",
        "lora_expanded_dataset_config.json",
    ]:
        path = ROOT_DIR / "configs" / filename
        data = json.loads(path.read_text(encoding="utf-8"))

        assert required.issubset(data)
        assert Path(ROOT_DIR / data["dataset_path"]).exists()
        assert data["mode"] == "LoRA"
