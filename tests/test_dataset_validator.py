from pathlib import Path

from mermaid_generate.dataset_validator import validate_dataset_file, validate_samples


def test_validate_dataset_report_counts(tmp_path: Path) -> None:
    path = tmp_path / "dataset.jsonl"
    valid = '{"prompt":"Create mind map about online learning","completion":"mindmap\\n  root((Online Learning))\\n    Platforms\\n      LMS"}'
    duplicate = valid
    invalid = '{"prompt":"","completion":"```mermaid\\nflowchart TD\\n A-->B\\n```"}'
    path.write_text("\n".join([valid, duplicate, invalid]), encoding="utf-8")

    report = validate_dataset_file(path)
    data = report.as_dict()

    assert data["total_samples"] == 3
    assert data["valid_samples"] == 2
    assert data["invalid_samples"] == 1
    assert data["duplicate_count"] == 1
    assert data["diagram_type_counts"] == {"mindmap": 2}
    assert data["train_ready"] is True
    assert any(
        "markdown code fences" in reason
        for reason in data["invalid_rows"][0]["reasons"]
    )


def test_zero_valid_samples_not_train_ready() -> None:
    report = validate_samples(
        [
            {
                "id": "bad",
                "diagram_type": "",
                "prompt": "",
                "target": "flowchart TD\n A-->B",
                "source_format": "prompt_completion",
                "row_index": 0,
            }
        ]
    )

    assert report.valid_samples == 0
    assert report.train_ready is False
