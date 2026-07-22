"""Mermaid cleanup, validation, and safe renderer normalization."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

DiagramType = Literal["mindmap", "venn", "auto"]

STOP_MARKERS = (
    "diagram type:",
    "user request:",
    "result expectations:",
    "output format:",
    "required format:",
    "rules:",
    "outline:",
    "</mermaid>",
    "classdiagram",
    "class diagram",
    "flowchart",
    "sequencediagram",
    "sequence diagram",
    "uml",
    "@startuml",
    "@enduml",
)


@dataclass
class MermaidValidationResult:
    valid: bool
    diagram_type: str | None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    normalized_code: str = ""
    renderer_code: str = ""

    def message(self) -> str:
        if self.valid:
            details = [f"Valid {self.diagram_type} Mermaid code."]
            details.extend(f"Warning: {warning}" for warning in self.warnings)
            return "\n".join(details)
        return "\n".join(self.errors) if self.errors else "Invalid Mermaid code."


def strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    fence_match = re.search(
        r"```(?:mermaid)?\s*(.*?)```",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if fence_match:
        return fence_match.group(1).strip()
    return cleaned.replace("```", "").strip()


def remove_explanation_text(text: str) -> str:
    lines = strip_markdown_fences(text).splitlines()
    start_index = None
    for index, line in enumerate(lines):
        stripped = line.strip().lower()
        if stripped.startswith("mindmap") or stripped.startswith("venn"):
            start_index = index
            break
    if start_index is None:
        return "\n".join(lines).strip()
    return "\n".join(lines[start_index:]).strip()


def normalize_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def _line_starts_diagram(line: str) -> str | None:
    stripped = line.strip().lower()
    if stripped == "mindmap":
        return "mindmap"
    if stripped in {"venn", "venn-beta"}:
        return "venn"
    return None


def _is_stop_line(line: str, expected_type: str, started: bool) -> bool:
    stripped = line.strip()
    lowered = stripped.lower()
    if not stripped:
        return False
    line_type = _line_starts_diagram(stripped)
    if started and line_type and line_type != expected_type:
        return True
    if started and line_type == expected_type:
        return True
    if any(marker in lowered for marker in STOP_MARKERS):
        return True
    if lowered.startswith(("here is", "explanation", "note:", "notes:", "the diagram")):
        return True
    if lowered.startswith(("```", "~~~")):
        return True
    return False


def extract_first_mermaid_diagram(text: str, expected_type: str = "auto") -> str:
    """Extract the first Mermaid Mind Map or Venn block from noisy LLM output."""

    expected = expected_type.lower().replace("mind map", "mindmap")
    if expected not in {"mindmap", "venn"}:
        expected = "auto"

    cleaned = normalize_line_endings(strip_markdown_fences(text or ""))
    if not cleaned:
        return ""

    lines = cleaned.splitlines()
    start_index = None
    detected_type = None

    for index, line in enumerate(lines):
        line_type = _line_starts_diagram(line)
        if line_type and (expected == "auto" or line_type == expected):
            start_index = index
            detected_type = line_type
            break

    if start_index is None:
        if expected in {"mindmap", "venn"}:
            repaired, _ = safe_repair_missing_prefix(cleaned, expected)
            if repaired != cleaned:
                return extract_first_mermaid_diagram(repaired, expected)
        return cleaned.strip()

    kept: list[str] = []
    for line in lines[start_index:]:
        if kept and _is_stop_line(line, detected_type or expected, started=True):
            break
        kept.append(line.rstrip())

    while kept and not kept[-1].strip():
        kept.pop()

    return normalize_for_assignment("\n".join(kept))


def infer_diagram_type(code: str) -> str | None:
    lowered = code.lstrip().lower()
    if lowered.startswith("mindmap"):
        return "mindmap"
    if lowered.startswith("venn"):
        return "venn"
    return None


def normalize_venn_for_renderer(code: str) -> str:
    stripped = code.lstrip()
    if stripped.lower().startswith("venn-beta"):
        return stripped
    if stripped.lower().startswith("venn"):
        return re.sub(r"(?i)^venn\b", "venn-beta", stripped, count=1)
    return code.strip()


def normalize_for_assignment(code: str) -> str:
    stripped = code.strip()
    if stripped.lower().startswith("venn-beta"):
        return re.sub(r"(?i)^venn-beta\b", "venn", stripped, count=1)
    return stripped


def safe_repair_missing_prefix(code: str, expected_type: str) -> tuple[str, str | None]:
    stripped = code.strip()
    lowered = stripped.lower()
    if not stripped or infer_diagram_type(stripped):
        return stripped, None

    if expected_type == "mindmap" and re.search(r"(?m)^\s*root\s*\(", stripped):
        return f"mindmap\n{stripped}", "Added missing mindmap prefix."
    if expected_type == "venn" and re.search(r"(?m)^\s*(set|union)\s+", stripped):
        return f"venn\n{stripped}", "Added missing venn prefix."
    if expected_type in {"mindmap", "venn"} and not any(
        marker in lowered for marker in ("flowchart", "sequence", "classdiagram")
    ):
        first_line = stripped.splitlines()[0].lower()
        if expected_type == "mindmap" and "root" in first_line:
            return f"mindmap\n{stripped}", "Added likely mindmap prefix."
        if expected_type == "venn" and ("set " in first_line or "union " in first_line):
            return f"venn\n{stripped}", "Added likely venn prefix."
    return stripped, None


def postprocess_mermaid_output(raw_output: str, expected_type: str = "auto") -> str:
    cleaned = extract_first_mermaid_diagram(raw_output, expected_type)
    expected = expected_type.lower().replace("mind map", "mindmap")
    if expected in {"mindmap", "venn"}:
        cleaned, _ = safe_repair_missing_prefix(cleaned, expected)
    return normalize_for_assignment(cleaned)


def validate_mindmap(code: str) -> list[str]:
    errors: list[str] = []
    lines = [line.rstrip() for line in code.splitlines() if line.strip()]
    if not lines or lines[0].strip().lower() != "mindmap":
        errors.append("Mind Map output must start with mindmap.")
    if len(lines) < 3:
        errors.append("Mind Map should contain a root and at least one child.")
    if lines and not any("root" in line.lower() for line in lines[1:4]):
        errors.append("Mind Map should include a root node near the top.")
    for line in lines[1:]:
        leading = len(line) - len(line.lstrip(" "))
        if leading % 2 != 0:
            errors.append("Mind Map indentation should use even spaces.")
            break
    return errors


def validate_venn(code: str) -> list[str]:
    errors: list[str] = []
    renderer_code = normalize_venn_for_renderer(code)
    lines = [line.strip() for line in renderer_code.splitlines() if line.strip()]
    if not lines or lines[0].lower() != "venn-beta":
        errors.append("Venn output must start with venn or venn-beta.")
    set_ids: set[str] = set()
    union_count = 0
    for line in lines[1:]:
        if line.lower().startswith("set "):
            parts = line.split(maxsplit=2)
            if len(parts) >= 2:
                set_ids.add(parts[1].split("[", 1)[0].split(":", 1)[0].strip().strip('"'))
        elif line.lower().startswith("union "):
            union_count += 1
            body = line.split(maxsplit=1)[1]
            ids_part = body.split("[", 1)[0].split(":", 1)[0]
            referenced = [item.strip().strip('"') for item in ids_part.split(",") if item.strip()]
            if len(referenced) < 2:
                errors.append("Venn union must reference at least two sets.")
            missing = [item for item in referenced if item not in set_ids]
            if missing:
                errors.append(f"Venn union references undefined set(s): {', '.join(missing)}.")
    if len(set_ids) < 2:
        errors.append("Venn diagram should define at least two sets.")
    if union_count < 1:
        errors.append("Venn diagram should define at least one union/intersection.")
    return errors


def validate_mermaid_code(
    code: str,
    expected_type: str = "auto",
) -> MermaidValidationResult:
    normalized = normalize_for_assignment(strip_markdown_fences(code))
    diagram_type = infer_diagram_type(normalized)
    errors: list[str] = []
    warnings: list[str] = []

    if not normalized:
        errors.append("Mermaid output is empty.")
    if "```" in code:
        errors.append("Mermaid output must not include markdown code fences.")
    if diagram_type is None:
        errors.append("Mermaid output must start with mindmap or venn.")

    lowered = normalized.lower()
    if "mindmap" in lowered and "venn" in lowered:
        errors.append("Mermaid output must not mix mindmap and venn syntax.")

    expected = expected_type.lower().replace("mind map", "mindmap")
    if expected in {"mindmap", "venn"} and diagram_type and diagram_type != expected:
        errors.append(f"Expected {expected} output, got {diagram_type}.")

    if diagram_type == "mindmap":
        errors.extend(validate_mindmap(normalized))
        renderer_code = normalized
    elif diagram_type == "venn":
        errors.extend(validate_venn(normalized))
        renderer_code = normalize_venn_for_renderer(normalized)
        if normalized.lstrip().lower().startswith("venn"):
            warnings.append("Preview renders Venn as Mermaid venn-beta syntax.")
    else:
        renderer_code = normalized

    return MermaidValidationResult(
        valid=not errors,
        diagram_type=diagram_type,
        errors=errors,
        warnings=warnings,
        normalized_code=normalized,
        renderer_code=renderer_code,
    )
