from mermaid_generate.diagram_repair import repair_or_compile_mindmap
from mermaid_generate.mermaid_validator import validate_mermaid_code


def test_invalid_output_gets_repaired() -> None:
    result = repair_or_compile_mindmap("", "Buat mind map tentang strategi belajar AI untuk mahasiswa.")

    assert result.used_fallback
    assert result.code.startswith("mindmap\n")
    assert "root((Strategi Belajar AI" in result.code
    assert validate_mermaid_code(result.code, "mindmap").valid


def test_class_diagram_text_gets_removed() -> None:
    raw = """mindmap
  root((Project))
    Plan
classDiagram
  A <|-- B"""

    result = repair_or_compile_mindmap(raw, "Create a mind map about project planning.")

    assert "classDiagram" not in result.code
    assert validate_mermaid_code(result.code, "mindmap").valid


def test_missing_prefix_gets_repaired() -> None:
    raw = "  root((Digital Marketing))\n    Channels\n      Instagram"

    result = repair_or_compile_mindmap(raw, "Create a mind map about digital marketing.")

    assert not result.used_fallback
    assert result.code.startswith("mindmap\n")
    assert validate_mermaid_code(result.code, "mindmap").valid


def test_indonesian_prompt_creates_indonesian_friendly_output() -> None:
    result = repair_or_compile_mindmap("", "Buat mind map tentang strategi belajar AI untuk mahasiswa.")

    assert "Dasar AI" in result.code
    assert "Praktik" in result.code
    assert "Portofolio" in result.code


def test_english_prompt_creates_english_friendly_output() -> None:
    result = repair_or_compile_mindmap("", "Create a mind map about AI learning strategy.")

    assert "AI Basics" in result.code
    assert "Practice" in result.code
    assert validate_mermaid_code(result.code, "mindmap").valid
