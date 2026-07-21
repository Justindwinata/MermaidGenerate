from mermaid_generate.training import (
    FineTuningConfig,
    build_training_text,
    split_train_eval,
)
from mermaid_generate.training_manager import TrainingJobState


def test_training_config_normalizes_modes() -> None:
    assert FineTuningConfig(mode="LoRA").normalized_mode() == "lora"
    assert FineTuningConfig(mode="QLoRA 4-bit").normalized_mode() == "qlora"
    assert FineTuningConfig(mode="Full Fine-Tuning").normalized_mode() == "full"


def test_split_train_eval_keeps_train_sample() -> None:
    samples = [{"id": str(i)} for i in range(5)]
    train, eval_data = split_train_eval(samples, 0.2)

    assert len(train) == 4
    assert len(eval_data) == 1


def test_build_training_text_contains_target() -> None:
    text = build_training_text(
        {
            "diagram_type": "mindmap",
            "prompt": "Create topic map",
            "target": "mindmap\n  root((Topic))",
        }
    )

    assert "Return only valid Mermaid code" in text
    assert "mindmap\n  root((Topic))" in text


def test_training_job_state_serializes_result_none() -> None:
    state = TrainingJobState(job_id="abc", status="idle")

    assert state.as_dict()["job_id"] == "abc"
