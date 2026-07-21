"""Adapter/model activation and artifact helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .config import DEFAULT_MODEL_ID
from .model_loader import ACTIVE_MODEL_STATE, ActiveModelState, load_adapter, load_full_model
from .training import TrainingResult, create_zip


@dataclass
class AdapterMetadata:
    active: bool
    mode: str
    model_id: str
    adapter_path: str | None = None
    full_model_path: str | None = None
    zip_path: str | None = None
    status: str = ""

    def as_dict(self) -> dict[str, str | bool | None]:
        return asdict(self)


def current_adapter_metadata() -> AdapterMetadata:
    state = ACTIVE_MODEL_STATE
    return AdapterMetadata(
        active=state.model is not None and state.tokenizer is not None,
        mode=state.mode,
        model_id=state.model_id,
        adapter_path=state.adapter_path,
        full_model_path=state.full_model_path,
        status=state.status_text(),
    )


def ensure_adapter_zip(adapter_path: str | Path) -> str:
    path = Path(adapter_path)
    if not path.exists():
        raise FileNotFoundError(f"Adapter path not found: {path}")
    zip_path = path.with_suffix(".zip")
    if zip_path.exists():
        return str(zip_path)
    return create_zip(path)


def activate_adapter_output(
    adapter_path: str | Path,
    *,
    model_id: str = DEFAULT_MODEL_ID,
    use_4bit: bool = False,
) -> ActiveModelState:
    return load_adapter(adapter_path, model_id=model_id, use_4bit=use_4bit)


def activate_full_model_output(model_path: str | Path) -> ActiveModelState:
    return load_full_model(model_path)


def activate_training_result(
    result: TrainingResult,
    *,
    model_id: str = DEFAULT_MODEL_ID,
) -> AdapterMetadata:
    if result.status != "completed" or not result.output_path:
        raise RuntimeError("Only a completed training result can be activated.")

    if result.mode in {"lora", "qlora"}:
        state = activate_adapter_output(
            result.output_path,
            model_id=model_id,
            use_4bit=result.mode == "qlora",
        )
        zip_path = result.zip_path or ensure_adapter_zip(result.output_path)
        return AdapterMetadata(
            active=True,
            mode=state.mode,
            model_id=state.model_id,
            adapter_path=state.adapter_path,
            zip_path=zip_path,
            status=state.status_text(),
        )

    state = activate_full_model_output(result.output_path)
    return AdapterMetadata(
        active=True,
        mode=state.mode,
        model_id=state.model_id,
        full_model_path=state.full_model_path,
        status=state.status_text(),
    )
