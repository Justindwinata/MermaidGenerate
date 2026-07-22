"""Deterministic Mermaid repair and fallback compilers."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .mermaid_validator import (
    extract_first_mermaid_diagram,
    validate_mermaid_code,
)


MAX_LABEL_LENGTH = 36


@dataclass
class RepairResult:
    code: str
    used_fallback: bool
    message: str


def sanitize_label(label: str, fallback: str = "Concept") -> str:
    cleaned = re.sub(r"[\[\]{}<>`|]", " ", label or "")
    cleaned = cleaned.replace('"', "").replace("\\", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ,.;:-")
    if not cleaned:
        cleaned = fallback
    if len(cleaned) > MAX_LABEL_LENGTH:
        cleaned = cleaned[:MAX_LABEL_LENGTH].rsplit(" ", 1)[0] or cleaned[:MAX_LABEL_LENGTH]
    return cleaned


def _quoted_labels(text: str) -> list[str]:
    labels = re.findall(r'"([^"]{2,80})"', text)
    labels.extend(re.findall(r"\[([^\]]{2,80})\]", text))
    return [sanitize_label(label) for label in labels]


def _split_comparison_phrase(prompt: str) -> list[str]:
    cleaned = prompt
    cleaned = re.sub(
        r"(?i)\b(create|make|buat|diagram|venn|membandingkan|comparing|compare|tentang|about|antara|between|marketing)\b",
        " ",
        cleaned,
    )
    cleaned = cleaned.replace("/", ",")
    parts = re.split(r"\s*(?:,| dan | and | vs | versus | dengan | serta | & )\s*", cleaned, flags=re.IGNORECASE)
    labels: list[str] = []
    for part in parts:
        label = sanitize_label(part)
        label = re.sub(r"(?i)^(dan|and|serta|dengan)\s+", "", label).strip()
        if len(label) >= 2:
            labels.append(label)
    return labels


def extract_venn_labels(user_prompt: str, raw_output: str = "") -> list[str]:
    labels: list[str] = []
    for candidate in _quoted_labels(raw_output) + _split_comparison_phrase(user_prompt):
        lowered = candidate.lower()
        if lowered in {"venn", "diagram", "set", "union", "text", "marketing"}:
            continue
        if candidate not in labels:
            labels.append(candidate)
        if len(labels) == 3:
            break
    if len(labels) < 2:
        labels.extend(["Concept A", "Concept B", "Concept C"])
    return labels[:3] if len(labels) >= 3 else labels[:2]


def _overlap_labels(labels: list[str], prompt: str) -> list[str]:
    lowered = prompt.lower()
    if any(marker in lowered for marker in ("instagram", "tiktok", "whatsapp", "marketing", "sosial", "social")):
        return [
            "Audience Engagement",
            "Customer Communication",
            "Short Content Sharing",
            "Digital Marketing",
        ]
    if any(marker in lowered for marker in ("student", "siswa", "employee", "entrepreneur", "wirausaha")):
        return [
            "Working Learners",
            "Career Builders",
            "Independent Projects",
            "Lifelong Growth",
        ]
    if any(marker in lowered for marker in ("ai", "machine learning", "data science")):
        return [
            "Intelligent Models",
            "Predictive Analytics",
            "Applied Systems",
            "AI Data Products",
        ]
    return [
        f"{labels[0]} and {labels[1]}",
        f"{labels[0]} and {labels[2]}" if len(labels) > 2 else "Shared Benefits",
        f"{labels[1]} and {labels[2]}" if len(labels) > 2 else "Common Ground",
        "Shared Intersection",
    ]


def compile_safe_venn(labels: list[str], user_prompt: str) -> str:
    safe_labels = [sanitize_label(label, f"Set {index + 1}") for index, label in enumerate(labels)]
    ids = ["A", "B", "C"][: len(safe_labels)]
    overlaps = [sanitize_label(label) for label in _overlap_labels(safe_labels, user_prompt)]
    lines = ["venn"]
    for ident, label in zip(ids, safe_labels):
        lines.append(f'  set {ident}["{label}"]')
    if len(ids) == 2:
        lines.extend(["  union A,B", f'    text "{overlaps[0]}"'])
    else:
        lines.extend(
            [
                "  union A,B",
                f'    text "{overlaps[0]}"',
                "  union A,C",
                f'    text "{overlaps[1]}"',
                "  union B,C",
                f'    text "{overlaps[2]}"',
                "  union A,B,C",
                f'    text "{overlaps[3]}"',
            ]
        )
    return "\n".join(lines)


def repair_venn_candidate(candidate: str) -> str:
    lines = [line.rstrip() for line in candidate.splitlines() if line.strip()]
    if not lines:
        return ""
    output = ["venn"]
    defined: set[str] = set()
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.lower() in {"venn", "venn-beta"}:
            index += 1
            continue
        set_match = re.match(r'(?i)^set\s+([A-Z][\w-]*)\s*(?:\[\s*"?([^"\]]+)"?\s*\]|"?([^"]+)"?)?', stripped)
        if set_match:
            set_id = set_match.group(1).strip()
            label = sanitize_label(set_match.group(2) or set_match.group(3) or set_id)
            defined.add(set_id)
            output.append(f'  set {set_id}["{label}"]')
            index += 1
            continue
        union_match = re.match(r'(?i)^union\s+([A-Z][\w-]*(?:\s*,\s*[A-Z][\w-]*)*)(?:\s*\[\s*"?([^"\]]+)"?\s*\])?', stripped)
        if union_match:
            refs = [ref.strip() for ref in union_match.group(1).split(",")]
            label = union_match.group(2)
            next_label = None
            if index + 1 < len(lines):
                text_match = re.match(r'(?i)^\s*text\s+"?([^"]+)"?', lines[index + 1].strip())
                if text_match:
                    next_label = text_match.group(1)
                    index += 1
            if len(refs) >= 2 and all(ref in defined for ref in refs):
                output.append(f"  union {','.join(refs)}")
                output.append(f'    text "{sanitize_label(label or next_label or "Shared Area")}"')
            index += 1
            continue
        index += 1
    return "\n".join(output)


def repair_or_compile_venn(raw_output: str, user_prompt: str) -> RepairResult:
    candidate = extract_first_mermaid_diagram(raw_output, "venn")
    repaired = repair_venn_candidate(candidate)
    validation = validate_mermaid_code(repaired, "venn")
    if validation.valid:
        return RepairResult(validation.normalized_code, False, "Cleaned valid Venn output.")

    fallback = compile_safe_venn(extract_venn_labels(user_prompt, raw_output), user_prompt)
    fallback_validation = validate_mermaid_code(fallback, "venn")
    if not fallback_validation.valid:
        raise RuntimeError(f"Internal Venn fallback failed validation: {fallback_validation.message()}")
    return RepairResult(
        fallback_validation.normalized_code,
        True,
        "Compiled deterministic Venn fallback from prompt because model output was invalid.",
    )


def extract_mindmap_topic(user_prompt: str) -> str:
    prompt = re.sub(
        r"(?i)\b(buat|create|make|mind\s*map|mindmap|tentang|about|untuk|for|diagram|peta pikiran)\b",
        " ",
        user_prompt,
    )
    prompt = re.sub(r"\s+", " ", prompt).strip(" .,:;-")
    prompt = re.sub(r"(?i)\b(mahasiswa|students?|pemula|beginners?)\b", " ", prompt)
    prompt = re.sub(r"\s+", " ", prompt).strip(" .,:;-")
    if not prompt:
        return "Main Topic"
    topic = prompt.title()
    topic = re.sub(r"\bAi\b", "AI", topic)
    return sanitize_label(topic, "Main Topic")


def _is_indonesian_prompt(prompt: str) -> bool:
    lowered = f" {prompt.lower()} "
    return any(marker in lowered for marker in (" buat ", " tentang ", " mahasiswa", " belajar ", " strategi ", " untuk "))


def _mindmap_branches(topic: str, prompt: str) -> list[tuple[str, list[str]]]:
    lowered = prompt.lower()
    if "ai" in lowered or "machine learning" in lowered:
        if _is_indonesian_prompt(prompt):
            return [
                ("Dasar AI", ["Machine Learning", "Deep Learning", "Data"]),
                ("Praktik", ["Proyek Kecil", "Eksperimen Model", "Evaluasi"]),
                ("Tools", ["Python", "Notebook", "Library AI"]),
                ("Portofolio", ["Dokumentasi", "GitHub", "Presentasi"]),
            ]
        return [
            ("AI Basics", ["Machine Learning", "Deep Learning", "Data"]),
            ("Practice", ["Small Projects", "Model Experiments", "Evaluation"]),
            ("Tools", ["Python", "Notebook", "AI Libraries"]),
            ("Portfolio", ["Documentation", "GitHub", "Presentation"]),
        ]
    if any(marker in lowered for marker in ("marketing", "umkm", "business", "bisnis")):
        return [
            ("Content Strategy", ["Short Video", "Educational Post", "Testimonial"]),
            ("Channels", ["Instagram", "TikTok", "WhatsApp"]),
            ("Customers", ["Persona", "Needs", "Feedback"]),
            ("Metrics", ["Reach", "Engagement", "Conversion"]),
        ]
    if _is_indonesian_prompt(prompt):
        return [
            ("Konsep Utama", ["Definisi", "Tujuan", "Manfaat"]),
            ("Aktivitas", ["Perencanaan", "Praktik", "Evaluasi"]),
            ("Sumber Daya", ["Tools", "Referensi", "Komunitas"]),
            ("Hasil", ["Dokumentasi", "Presentasi", "Perbaikan"]),
        ]
    return [
        ("Core Ideas", ["Definition", "Goals", "Benefits"]),
        ("Activities", ["Planning", "Practice", "Evaluation"]),
        ("Resources", ["Tools", "References", "Community"]),
        ("Outcomes", ["Documentation", "Presentation", "Iteration"]),
    ]


def compile_safe_mindmap(user_prompt: str) -> str:
    topic = extract_mindmap_topic(user_prompt)
    lines = ["mindmap", f"  root(({topic}))"]
    for branch, children in _mindmap_branches(topic, user_prompt):
        lines.append(f"    {sanitize_label(branch)}")
        for child in children:
            lines.append(f"      {sanitize_label(child)}")
    return "\n".join(lines)


def repair_mindmap_candidate(candidate: str) -> str:
    lines = [line.rstrip() for line in candidate.splitlines() if line.strip()]
    if not lines:
        return ""
    if lines[0].strip().lower() != "mindmap":
        candidate = f"mindmap\n{candidate}"
        lines = [line.rstrip() for line in candidate.splitlines() if line.strip()]
    root_seen = False
    repaired = ["mindmap"]
    for line in lines[1:]:
        stripped = sanitize_label(line.strip())
        if not stripped:
            continue
        if "classdiagram" in stripped.lower() or "flowchart" in stripped.lower() or "uml" in stripped.lower():
            break
        leading = len(line) - len(line.lstrip(" "))
        if "root" in stripped.lower() and not root_seen:
            repaired.append(f"  {line.strip()}")
            root_seen = True
            continue
        if "root" in stripped.lower() and root_seen:
            continue
        indent = max(4, leading if leading % 2 == 0 else leading + 1)
        repaired.append(f"{' ' * indent}{stripped}")
    return "\n".join(repaired)


def repair_or_compile_mindmap(raw_output: str, user_prompt: str) -> RepairResult:
    candidate = extract_first_mermaid_diagram(raw_output, "mindmap")
    repaired = repair_mindmap_candidate(candidate)
    validation = validate_mermaid_code(repaired, "mindmap")
    if validation.valid:
        return RepairResult(validation.normalized_code, False, "Cleaned valid Mind Map output.")

    fallback = compile_safe_mindmap(user_prompt)
    fallback_validation = validate_mermaid_code(fallback, "mindmap")
    if not fallback_validation.valid:
        raise RuntimeError(f"Internal Mind Map fallback failed validation: {fallback_validation.message()}")
    return RepairResult(
        fallback_validation.normalized_code,
        True,
        "Compiled deterministic Mind Map fallback from prompt because model output was invalid.",
    )
