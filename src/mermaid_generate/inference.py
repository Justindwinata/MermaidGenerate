"""Mermaid generation with Transformers/PyTorch."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from .mermaid_validator import postprocess_mermaid_output, validate_mermaid_code
from .model_loader import ACTIVE_MODEL_STATE, ActiveModelState, load_base_model


SYSTEM_PROMPT = """You are a Mermaid diagram generator.
Return only valid Mermaid code.
Do not include markdown code fences.
Do not explain the answer."""


@dataclass
class GenerationSettings:
    max_new_tokens: int = 320
    temperature: float = 0.2
    top_p: float = 0.9
    repetition_penalty: float = 1.05


@dataclass
class InferenceResult:
    code: str
    raw_output: str
    valid: bool
    validation_message: str
    inference_time_seconds: float
    model_status: str


def normalize_diagram_type(diagram_type: str) -> str:
    value = (diagram_type or "auto").strip().lower()
    if value in {"mind map", "mind-map", "mindmap"}:
        return "mindmap"
    if value in {"venn", "venn diagram", "venn-diagram", "venn-beta"}:
        return "venn"
    return "auto"


def detect_diagram_type_from_prompt(prompt: str) -> str:
    lowered = prompt.lower()
    if "venn" in lowered or "compare" in lowered or "intersection" in lowered:
        return "venn"
    if "mind map" in lowered or "mindmap" in lowered or "hierarchy" in lowered:
        return "mindmap"
    return "mindmap"


def build_generation_prompt(user_prompt: str, diagram_type: str) -> str:
    normalized_type = normalize_diagram_type(diagram_type)
    if normalized_type == "auto":
        normalized_type = detect_diagram_type_from_prompt(user_prompt)
    label = "Mind Map" if normalized_type == "mindmap" else "Venn Diagram"
    type_rules = (
        "- output should start with mindmap\n"
        "- use valid Mermaid mindmap indentation\n"
        "- represent hierarchical concepts clearly"
        if normalized_type == "mindmap"
        else "- output should start with venn\n"
        "- use set and union statements\n"
        "- represent sets and intersections clearly"
    )
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Diagram type: {label}\n"
        f"User request: {user_prompt.strip()}\n\n"
        f"Rules:\n{type_rules}\n\n"
        "Mermaid code:"
    )


def apply_chat_template(tokenizer: Any, prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
    return prompt


def ensure_model_loaded(state: ActiveModelState | None = None) -> ActiveModelState:
    state = state or ACTIVE_MODEL_STATE
    if state.model is None or state.tokenizer is None:
        return load_base_model(model_id=state.model_id)
    return state


def generate_mermaid(
    user_prompt: str,
    diagram_type: str = "auto",
    settings: GenerationSettings | None = None,
    *,
    state: ActiveModelState | None = None,
) -> InferenceResult:
    if not user_prompt or not user_prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("PyTorch is required for inference.") from exc

    settings = settings or GenerationSettings()
    normalized_type = normalize_diagram_type(diagram_type)
    if normalized_type == "auto":
        normalized_type = detect_diagram_type_from_prompt(user_prompt)

    active_state = ensure_model_loaded(state)
    model = active_state.model
    tokenizer = active_state.tokenizer
    prompt = build_generation_prompt(user_prompt, normalized_type)
    prompt_text = apply_chat_template(tokenizer, prompt)
    started = time.perf_counter()

    inputs = tokenizer(
        prompt_text,
        return_tensors="pt",
        add_special_tokens=False,
    )
    input_device = model.get_input_embeddings().weight.device
    inputs = {key: value.to(input_device) for key, value in inputs.items()}
    do_sample = settings.temperature > 0
    generation_kwargs = {
        "max_new_tokens": int(settings.max_new_tokens),
        "do_sample": do_sample,
        "repetition_penalty": float(settings.repetition_penalty),
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
        "use_cache": True,
    }
    if do_sample:
        generation_kwargs["temperature"] = float(settings.temperature)
        generation_kwargs["top_p"] = float(settings.top_p)

    with torch.no_grad():
        output_ids = model.generate(**inputs, **generation_kwargs)

    new_tokens = output_ids[0][inputs["input_ids"].shape[-1] :]
    raw_output = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    code = postprocess_mermaid_output(raw_output, expected_type=normalized_type)
    validation = validate_mermaid_code(code, expected_type=normalized_type)
    elapsed = time.perf_counter() - started

    return InferenceResult(
        code=validation.normalized_code or code,
        raw_output=raw_output,
        valid=validation.valid,
        validation_message=validation.message(),
        inference_time_seconds=elapsed,
        model_status=active_state.status_text(),
    )
