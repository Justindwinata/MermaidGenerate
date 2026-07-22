from mermaid_generate.inference import (
    build_generation_prompt,
    detect_diagram_type_from_prompt,
    normalize_diagram_type,
)
from mermaid_generate.mermaid_validator import postprocess_mermaid_output
from mermaid_generate.mermaid_validator import extract_first_mermaid_diagram


def test_prompt_template_requests_code_only() -> None:
    prompt = build_generation_prompt("Create a Venn about A and B", "venn")

    assert "Return exactly one valid Mermaid Venn diagram" in prompt
    assert "Use assignment-facing first line: venn" in prompt
    assert "Do not use undefined union references" in prompt


def test_auto_detect_prefers_venn_for_compare() -> None:
    assert detect_diagram_type_from_prompt("Compare students and workers") == "venn"


def test_normalize_diagram_type() -> None:
    assert normalize_diagram_type("Mind Map") == "mindmap"
    assert normalize_diagram_type("venn-beta") == "venn"


def test_safe_prefix_repair_for_venn() -> None:
    raw = 'set A["A"]\nset B["B"]\nunion A,B\n  text "AB"'

    assert postprocess_mermaid_output(raw, "venn").startswith("venn\n")


def test_extract_removes_prompt_echo_after_diagram() -> None:
    raw = """Diagram type: Venn
User request: compare apps
venn
  set A["Instagram"]
  set B["TikTok"]
  union A,B
    text "Social Video"
User request: now make a class diagram
classDiagram
  App <|-- User"""

    assert extract_first_mermaid_diagram(raw, "venn") == (
        'venn\n  set A["Instagram"]\n  set B["TikTok"]\n  union A,B\n    text "Social Video"'
    )


def test_extract_stops_before_second_diagram_type() -> None:
    raw = """mindmap
  root((AI))
    Data
venn
  set A["A"]"""

    assert extract_first_mermaid_diagram(raw, "mindmap") == (
        "mindmap\n  root((AI))\n    Data"
    )


def test_extract_removes_class_uml_contamination() -> None:
    raw = """```mermaid
mindmap
  root((Project))
    Plan
```
@startuml
class Project"""

    assert extract_first_mermaid_diagram(raw, "mindmap") == (
        "mindmap\n  root((Project))\n    Plan"
    )
