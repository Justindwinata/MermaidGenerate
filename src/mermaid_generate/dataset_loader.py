"""Dataset loading and normalization for MermaidGenerate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import (
    compact_text,
    infer_complexity,
    infer_domain,
    infer_language,
    stable_id,
)


SUPPORTED_EXTENSIONS = {".json", ".jsonl"}


class DatasetLoadError(ValueError):
    """Raised when an uploaded dataset cannot be parsed."""


def load_raw_records(path: str | Path) -> list[dict[str, Any]]:
    dataset_path = Path(path)
    suffix = dataset_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise DatasetLoadError("Dataset must be a .json or .jsonl file.")

    text = dataset_path.read_text(encoding="utf-8")
    if not text.strip():
        raise DatasetLoadError("Dataset file is empty.")

    try:
        if suffix == ".jsonl":
            records = [
                json.loads(line)
                for line in text.splitlines()
                if line.strip()
            ]
        else:
            loaded = json.loads(text)
            if isinstance(loaded, list):
                records = loaded
            elif isinstance(loaded, dict) and isinstance(loaded.get("data"), list):
                records = loaded["data"]
            else:
                records = [loaded]
    except json.JSONDecodeError as exc:
        raise DatasetLoadError(f"Invalid JSON: {exc}") from exc

    if not all(isinstance(item, dict) for item in records):
        raise DatasetLoadError("Every dataset row must be a JSON object.")
    return records


def extract_messages_sample(record: dict[str, Any]) -> tuple[str, str] | None:
    messages = record.get("messages")
    if not isinstance(messages, list):
        return None

    user_parts: list[str] = []
    assistant_parts: list[str] = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        role = compact_text(message.get("role")).lower()
        content = compact_text(message.get("content"))
        if role == "user":
            user_parts.append(content)
        elif role == "assistant":
            assistant_parts.append(content)

    prompt = "\n".join(part for part in user_parts if part).strip()
    target = assistant_parts[-1].strip() if assistant_parts else ""
    return prompt, target


def normalize_record(record: dict[str, Any], row_index: int) -> dict[str, Any]:
    source_format = "unknown"
    prompt = ""
    target = ""

    messages_sample = extract_messages_sample(record)
    if messages_sample is not None:
        source_format = "messages"
        prompt, target = messages_sample
    elif "prompt" in record or "completion" in record:
        source_format = "prompt_completion"
        prompt = compact_text(record.get("prompt"))
        target = str(record.get("completion") or "").strip()
    elif "instruction" in record or "output" in record:
        source_format = "instruction_output"
        instruction = compact_text(record.get("instruction"))
        input_text = compact_text(record.get("input"))
        prompt = (
            f"{instruction}\n\nInput: {input_text}".strip()
            if input_text
            else instruction
        )
        target = str(record.get("output") or "").strip()

    target_prefix = target.lstrip().split(maxsplit=1)[0].lower() if target.strip() else ""
    if target_prefix == "mindmap":
        diagram_type = "mindmap"
    elif target_prefix in {"venn", "venn-beta"}:
        diagram_type = "venn"
    else:
        diagram_type = compact_text(record.get("diagram_type")).lower()
        if diagram_type in {"mind map", "mind-map"}:
            diagram_type = "mindmap"
        if diagram_type in {"venn diagram", "venn-diagram"}:
            diagram_type = "venn"

    sample_id = compact_text(record.get("id")) or stable_id(
        str(row_index),
        prompt,
        target,
    )

    return {
        "id": sample_id,
        "diagram_type": diagram_type,
        "prompt": prompt,
        "target": target,
        "source_format": source_format,
        "language": compact_text(record.get("language")) or infer_language(prompt),
        "domain": compact_text(record.get("domain")) or infer_domain(prompt),
        "complexity": compact_text(record.get("complexity")) or infer_complexity(target),
        "row_index": row_index,
        "raw": record,
    }


def load_and_normalize_dataset(path: str | Path) -> list[dict[str, Any]]:
    return [
        normalize_record(record, index)
        for index, record in enumerate(load_raw_records(path))
    ]
