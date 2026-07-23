import json
from pathlib import Path

from mermaid_generate.dataset_loader import load_and_normalize_dataset
from mermaid_generate.dataset_validator import validate_dataset_file, validate_samples
from mermaid_generate.diagram_repair import (
    repair_or_compile_mindmap,
    repair_or_compile_venn,
)
from mermaid_generate.mermaid_preview import build_mermaid_preview_html
from mermaid_generate.mermaid_validator import validate_mermaid_code


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_dataset_loader_accepts_required_formats(tmp_path: Path) -> None:
    path = tmp_path / "formats.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "messages": [
                            {"role": "user", "content": "Create mind map about AI"},
                            {"role": "assistant", "content": "mindmap\n  root((AI))\n    Data"},
                        ]
                    }
                ),
                json.dumps(
                    {
                        "prompt": "Create a Venn about AI and data science",
                        "completion": 'venn\n  set A["AI"]\n  set B["Data Science"]\n  union A,B\n    text "Models"',
                    }
                ),
                json.dumps(
                    {
                        "instruction": "Create a Mermaid mind map.",
                        "input": "Topic: UMKM",
                        "output": "mindmap\n  root((UMKM))\n    Sales",
                    }
                ),
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
    assert [sample["diagram_type"] for sample in samples] == ["mindmap", "venn", "mindmap"]


def test_curated_mixed_dataset_validates() -> None:
    report = validate_dataset_file(ROOT_DIR / "datasets/curated/mixed_mindmap_venn_curated.jsonl")

    assert report.total_samples >= 150
    assert report.valid_samples == report.total_samples
    assert report.invalid_samples == 0
    assert report.duplicate_count == 0
    assert report.diagram_type_counts.get("mindmap", 0) == 75
    assert report.diagram_type_counts.get("venn", 0) == 75
    assert report.train_ready is True


def test_dataset_validator_rejects_empty_target_wrong_type_and_duplicates() -> None:
    samples = [
        {
            "id": "ok",
            "diagram_type": "mindmap",
            "prompt": "Create mind map",
            "target": "mindmap\n  root((Topic))\n    Branch",
            "source_format": "prompt_completion",
            "row_index": 0,
        },
        {
            "id": "empty-target",
            "diagram_type": "mindmap",
            "prompt": "Create mind map",
            "target": "",
            "source_format": "prompt_completion",
            "row_index": 1,
        },
        {
            "id": "wrong-type",
            "diagram_type": "mindmap",
            "prompt": "Create Venn",
            "target": 'venn\n  set A["A"]\n  set B["B"]\n  union A,B\n    text "AB"',
            "source_format": "prompt_completion",
            "row_index": 2,
        },
        {
            "id": "dup",
            "diagram_type": "mindmap",
            "prompt": "Create mind map",
            "target": "mindmap\n  root((Topic))\n    Branch",
            "source_format": "prompt_completion",
            "row_index": 3,
        },
    ]

    report = validate_samples(samples)

    assert report.valid_samples == 2
    assert report.invalid_samples == 2
    assert report.duplicate_count == 1
    invalid_reasons = " ".join(" ".join(row["reasons"]) for row in report.invalid_rows)
    assert "target is empty" in invalid_reasons
    assert "does not match target prefix" in invalid_reasons


def test_mermaid_validator_final_invalid_cases() -> None:
    undefined_union = 'venn\n  set A["A"]\n  set B["B"]\n  union A,C\n    text "Bad"'
    fenced = "```mermaid\nmindmap\n  root((A))\n    B\n```"

    assert validate_mermaid_code("mindmap\n  root((AI))\n    Data", "mindmap").valid
    assert validate_mermaid_code(
        'venn\n  set A["A"]\n  set B["B"]\n  union A,B\n    text "AB"',
        "venn",
    ).valid
    assert not validate_mermaid_code(undefined_union, "venn").valid
    assert not validate_mermaid_code(fenced, "mindmap").valid


def test_repair_fallback_handles_bad_and_empty_outputs() -> None:
    mindmap = repair_or_compile_mindmap(
        "classDiagram\n  A <|-- B",
        "Buat mind map tentang strategi belajar AI untuk mahasiswa.",
    )
    venn = repair_or_compile_venn(
        "",
        "Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.",
    )

    assert validate_mermaid_code(mindmap.code, "mindmap").valid
    assert "classDiagram" not in mindmap.code
    assert mindmap.used_fallback is True
    assert validate_mermaid_code(venn.code, "venn").valid
    assert venn.used_fallback is True


def test_preview_renderer_returns_iframe_not_plain_text_only() -> None:
    html = build_mermaid_preview_html("mindmap\n  root((AI))\n    Data")
    venn_html = build_mermaid_preview_html(
        'venn\n  set A["A"]\n  set B["B"]\n  union A,B\n    text "AB"'
    )

    assert "<iframe" in html
    assert "mermaid@" in html
    assert "Rendered Mermaid preview" in html
    assert "Final Mermaid code" in html
    assert "venn-beta" in venn_html


def test_notebook_json_and_required_sections_exist() -> None:
    notebook = json.loads((ROOT_DIR / "MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb").read_text())
    markdown = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    )

    required_phrases = [
        "Project Overview",
        "Install Dependencies",
        "Restart runtime note",
        "Import Libraries",
        "GPU and Runtime Check",
        "Dataset Upload and Validation",
        "Mermaid Validator and Preview Renderer",
        "Model Loading with Transformers and PyTorch",
        "Mermaid Inference",
        "LoRA / QLoRA / Full Fine-Tuning",
        "Gradio Web App",
        "Local laptop",
        "Colab",
        "Common errors",
        "Limitations",
        "Submission Guide",
    ]

    for phrase in required_phrases:
        assert phrase in markdown
