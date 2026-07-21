"""Transformers/PyTorch model loading and active model state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import DEFAULT_MODEL_ID


@dataclass
class ActiveModelState:
    model_id: str = DEFAULT_MODEL_ID
    model: Any | None = None
    tokenizer: Any | None = None
    adapter_path: str | None = None
    full_model_path: str | None = None
    mode: str = "unloaded"
    device: str = "auto"
    dtype: str = "auto"
    last_error: str | None = None

    def status_text(self) -> str:
        if self.model is None or self.tokenizer is None:
            return f"Model unloaded: {self.model_id}"
        if self.adapter_path:
            return f"Active adapter: {self.adapter_path} on {self.model_id}"
        if self.full_model_path:
            return f"Active full model: {self.full_model_path}"
        return f"Active base model: {self.model_id}"


ACTIVE_MODEL_STATE = ActiveModelState()


def resolve_torch_dtype(torch_module: Any, dtype: str = "auto") -> Any:
    if dtype and dtype != "auto":
        return getattr(torch_module, dtype)
    if torch_module.cuda.is_available():
        return (
            torch_module.bfloat16
            if torch_module.cuda.is_bf16_supported()
            else torch_module.float16
        )
    return torch_module.float32


def load_base_model(
    model_id: str = DEFAULT_MODEL_ID,
    *,
    use_4bit: bool = False,
    dtype: str = "auto",
    device_map: str | dict[str, int] | None = "auto",
) -> ActiveModelState:
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from transformers import BitsAndBytesConfig
    except ImportError as exc:
        raise RuntimeError(
            "Transformers/PyTorch dependencies are not installed. "
            "Run the dependency installation cell first."
        ) from exc

    if use_4bit and not torch.cuda.is_available():
        raise RuntimeError("QLoRA/4-bit loading requires a CUDA GPU.")

    torch_dtype = resolve_torch_dtype(torch, dtype)
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        use_fast=True,
        trust_remote_code=False,
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model_kwargs: dict[str, Any] = {
        "torch_dtype": torch_dtype,
        "low_cpu_mem_usage": True,
        "trust_remote_code": False,
    }
    if device_map is not None:
        model_kwargs["device_map"] = device_map
    if use_4bit:
        model_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch_dtype,
        )

    model = AutoModelForCausalLM.from_pretrained(model_id, **model_kwargs)
    model.eval()
    model.config.use_cache = True

    ACTIVE_MODEL_STATE.model_id = model_id
    ACTIVE_MODEL_STATE.model = model
    ACTIVE_MODEL_STATE.tokenizer = tokenizer
    ACTIVE_MODEL_STATE.adapter_path = None
    ACTIVE_MODEL_STATE.full_model_path = None
    ACTIVE_MODEL_STATE.mode = "base-4bit" if use_4bit else "base"
    ACTIVE_MODEL_STATE.dtype = str(torch_dtype)
    ACTIVE_MODEL_STATE.device = str(model.get_input_embeddings().weight.device)
    ACTIVE_MODEL_STATE.last_error = None
    return ACTIVE_MODEL_STATE


def load_adapter(
    adapter_path: str | Path,
    *,
    model_id: str = DEFAULT_MODEL_ID,
    use_4bit: bool = False,
) -> ActiveModelState:
    try:
        from peft import PeftModel
    except ImportError as exc:
        raise RuntimeError("PEFT is required to load LoRA/QLoRA adapters.") from exc

    state = load_base_model(model_id=model_id, use_4bit=use_4bit)
    path = Path(adapter_path)
    if not path.exists():
        raise FileNotFoundError(f"Adapter path not found: {path}")
    state.model = PeftModel.from_pretrained(
        state.model,
        str(path),
        is_trainable=False,
    )
    state.model.eval()
    state.adapter_path = str(path)
    state.mode = "adapter-4bit" if use_4bit else "adapter"
    return state


def load_full_model(model_path: str | Path) -> ActiveModelState:
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Full model path not found: {path}")
    state = load_base_model(model_id=str(path), use_4bit=False)
    state.full_model_path = str(path)
    state.mode = "full_model"
    return state
