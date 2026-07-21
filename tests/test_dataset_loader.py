from pathlib import Path

from mermaid_generate.dataset_loader import load_and_normalize_dataset


def test_load_jsonl_messages_prompt_completion_instruction(tmp_path: Path) -> None:
    path = tmp_path / "mixed.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"messages":[{"role":"user","content":"Create mind map about AI"},{"role":"assistant","content":"mindmap\\n  root((AI))\\n    Data"}]}',
                '{"prompt":"Create a Venn about product teams","completion":"venn\\n  set A[\\"Design\\"]\\n  set B[\\"Engineering\\"]\\n  union A,B[\\"Product\\"]"}',
                '{"instruction":"Create a Mermaid mind map.","input":"Topic: UMKM","output":"mindmap\\n  root((UMKM))\\n    Sales"}',
            ]
        ),
        encoding="utf-8",
    )

    samples = load_and_normalize_dataset(path)

    assert [sample["source_format"] for sample in samples] == [
        "messages",
        "prompt_completion",
        "instruction_output",
    ]
    assert samples[0]["diagram_type"] == "mindmap"
    assert samples[1]["diagram_type"] == "venn"
    assert "Input: Topic: UMKM" in samples[2]["prompt"]


def test_load_json_data_wrapper(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text(
        '{"data":[{"prompt":"Create mindmap for learning","completion":"mindmap\\n  root((Learning))\\n    Practice"}]}',
        encoding="utf-8",
    )

    samples = load_and_normalize_dataset(path)

    assert len(samples) == 1
    assert samples[0]["id"]
