from mermaid_generate.diagram_repair import repair_or_compile_venn
from mermaid_generate.mermaid_validator import validate_mermaid_code


def test_undefined_union_gets_repaired_with_fallback() -> None:
    raw = 'venn\n  set A["Instagram"]\n  union A,Live Shows\n    text "Bad"'

    result = repair_or_compile_venn(raw, "Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.")

    assert result.used_fallback
    assert validate_mermaid_code(result.code, "venn").valid
    assert "Live Shows" not in result.code


def test_extra_uml_text_gets_removed() -> None:
    raw = """venn
  set A["AI"]
  set B["Data Science"]
  union A,B
    text "Models"
classDiagram
  Foo <|-- Bar"""

    result = repair_or_compile_venn(raw, "Compare AI and data science.")

    assert not result.used_fallback
    assert "classDiagram" not in result.code
    assert validate_mermaid_code(result.code, "venn").valid


def test_invalid_labels_get_sanitized() -> None:
    result = repair_or_compile_venn("", 'Compare "Bad[One]" and "Two`Thing".')

    assert validate_mermaid_code(result.code, "venn").valid
    assert "[" not in result.code.splitlines()[1].split('"')[1]
    assert "`" not in result.code


def test_two_set_prompt_works() -> None:
    result = repair_or_compile_venn("", "Create a Venn diagram comparing online learning and offline learning.")

    assert result.code.count("  set ") == 2
    assert validate_mermaid_code(result.code, "venn").valid


def test_three_set_indonesian_prompt_works() -> None:
    result = repair_or_compile_venn("", "Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.")

    assert result.code.startswith("venn\n")
    assert 'set A["Instagram"]' in result.code
    assert 'set B["TikTok"]' in result.code
    assert 'set C["WhatsApp"]' in result.code
    assert validate_mermaid_code(result.code, "venn").valid
