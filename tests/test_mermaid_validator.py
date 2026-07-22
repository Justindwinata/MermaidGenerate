from mermaid_generate.mermaid_validator import (
    postprocess_mermaid_output,
    validate_mermaid_code,
)


def test_valid_mindmap() -> None:
    code = "mindmap\n  root((AI))\n    Data\n    Models"

    result = validate_mermaid_code(code, expected_type="mindmap")

    assert result.valid
    assert result.diagram_type == "mindmap"


def test_valid_venn_assignment_prefix_renderer_beta() -> None:
    code = 'venn\n  set A["Students"]\n  set B["Workers"]\n  union A,B\n    text "Working Students"'

    result = validate_mermaid_code(code, expected_type="venn")

    assert result.valid
    assert result.normalized_code.startswith("venn\n")
    assert result.renderer_code.startswith("venn-beta\n")


def test_venn_rejects_bracket_union_label() -> None:
    code = 'venn\n  set A["A"]\n  set B["B"]\n  union A,B["AB"]'

    result = validate_mermaid_code(code, expected_type="venn")

    assert not result.valid
    assert any("bracket syntax" in error for error in result.errors)


def test_postprocess_removes_fence_and_explanation() -> None:
    raw = "Here is the code:\n```mermaid\nmindmap\n  root((Cloud))\n    Compute\n```"

    assert postprocess_mermaid_output(raw, "mindmap") == (
        "mindmap\n  root((Cloud))\n    Compute"
    )


def test_invalid_mixed_diagram() -> None:
    result = validate_mermaid_code("mindmap\n  root((A))\nvenn\n  set A")

    assert not result.valid
    assert any("must not mix" in error for error in result.errors)
