"""Fine-tuning backend for LoRA, QLoRA, and full model training."""

from __future__ import annotations

import math
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .config import DEFAULT_MODEL_ID
from .inference import SYSTEM_PROMPT


ProgressCallback = Callable[[dict[str, Any]], None]
CancelCallback = Callable[[], bool]


@dataclass
class FineTuningConfig:
    mode: str = "LoRA"
    model_id: str = DEFAULT_MODEL_ID
    output_root: str = "outputs"
    epochs: float = 1.0
    learning_rate: float = 2e-4
    batch_size: int = 1
    gradient_accumulation: int = 4
    max_seq_length: int = 1024
    validation_split: float = 0.1
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    seed: int = 42

    def normalized_mode(self) -> str:
        value = self.mode.strip().lower()
        if value in {"lora", "qlora 4-bit", "qlora", "qlora-4bit"}:
            return "qlora" if "q" in value else "lora"
        if value in {"full fine-tuning", "full", "full_finetuning"}:
            return "full"
        raise ValueError("mode must be LoRA, QLoRA 4-bit, or Full Fine-Tuning")

    def validate(self) -> None:
        self.normalized_mode()
        if self.epochs <= 0:
            raise ValueError("epochs must be greater than 0")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be greater than 0")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")
        if self.gradient_accumulation <= 0:
            raise ValueError("gradient_accumulation must be greater than 0")
        if self.max_seq_length < 128:
            raise ValueError("max_seq_length should be at least 128")
        if not 0 <= self.validation_split < 0.8:
            raise ValueError("validation_split must be in [0, 0.8)")


@dataclass
class TrainingResult:
    status: str
    mode: str
    output_path: str | None = None
    zip_path: str | None = None
    train_loss: float | None = None
    eval_loss: float | None = None
    message: str = ""
    logs: list[str] = field(default_factory=list)


LORA_TARGET_MODULES = [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj",
]


def build_training_text(sample: dict[str, Any]) -> str:
    diagram_type = "Mind Map" if sample["diagram_type"] == "mindmap" else "Venn Diagram"
    user_content = (
        f"Diagram type: {diagram_type}\n"
        f"User request: {sample['prompt']}\n"
        "Return only Mermaid code."
    )
    return (
        f"<|system|>\n{SYSTEM_PROMPT}\n"
        f"<|user|>\n{user_content}\n"
        f"<|assistant|>\n{sample['target'].strip()}"
    )


def split_train_eval(
    samples: list[dict[str, Any]],
    validation_split: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not samples:
        raise ValueError("Cannot train with zero valid samples.")
    if len(samples) == 1 or validation_split <= 0:
        return samples, []
    eval_size = max(1, int(math.ceil(len(samples) * validation_split)))
    eval_size = min(eval_size, len(samples) - 1)
    return samples[:-eval_size], samples[-eval_size:]


def make_output_dir(config: FineTuningConfig) -> Path:
    mode = config.normalized_mode()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    if mode in {"lora", "qlora"}:
        root = Path(config.output_root) / "adapters"
    else:
        root = Path(config.output_root) / "full_models"
    output_dir = root / f"{mode}-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=False)
    return output_dir


def create_zip(output_dir: str | Path) -> str:
    path = Path(output_dir)
    archive = shutil.make_archive(str(path), "zip", root_dir=str(path))
    return archive


class CancelTrainingCallback:
    def __init__(self, should_cancel: CancelCallback | None = None) -> None:
        self.should_cancel = should_cancel or (lambda: False)

    def to_trainer_callback(self) -> Any:
        from transformers import TrainerCallback

        outer = self

        class _Callback(TrainerCallback):
            def on_step_end(self, args, state, control, **kwargs):  # type: ignore[no-untyped-def]
                if outer.should_cancel():
                    control.should_training_stop = True
                return control

        return _Callback()


class ProgressLoggingCallback:
    def __init__(self, report_progress: ProgressCallback | None = None) -> None:
        self.report_progress = report_progress or (lambda payload: None)

    def to_trainer_callback(self) -> Any:
        from transformers import TrainerCallback

        outer = self

        class _Callback(TrainerCallback):
            def on_log(self, args, state, control, logs=None, **kwargs):  # type: ignore[no-untyped-def]
                payload = dict(logs or {})
                payload.update(
                    {
                        "step": state.global_step,
                        "epoch": state.epoch,
                        "max_steps": state.max_steps,
                        "progress": (
                            state.global_step / state.max_steps
                            if state.max_steps
                            else 0
                        ),
                    }
                )
                outer.report_progress(payload)
                return control

        return _Callback()


def tokenize_training_dataset(
    samples: list[dict[str, Any]],
    tokenizer: Any,
    max_seq_length: int,
) -> Any:
    from datasets import Dataset

    texts = [build_training_text(sample) for sample in samples]
    dataset = Dataset.from_dict({"text": texts})

    def tokenize(batch: dict[str, list[str]]) -> dict[str, Any]:
        tokenized = tokenizer(
            batch["text"],
            truncation=True,
            max_length=max_seq_length,
            padding=False,
        )
        tokenized["labels"] = [ids.copy() for ids in tokenized["input_ids"]]
        return tokenized

    return dataset.map(tokenize, batched=True, remove_columns=["text"])


def load_model_for_training(config: FineTuningConfig) -> tuple[Any, Any]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    mode = config.normalized_mode()
    if mode == "qlora" and not torch.cuda.is_available():
        raise RuntimeError("QLoRA 4-bit requires a CUDA GPU and bitsandbytes.")

    dtype = (
        torch.bfloat16
        if torch.cuda.is_available() and torch.cuda.is_bf16_supported()
        else torch.float16
        if torch.cuda.is_available()
        else torch.float32
    )
    tokenizer = AutoTokenizer.from_pretrained(config.model_id, use_fast=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model_kwargs: dict[str, Any] = {
        "torch_dtype": dtype,
        "low_cpu_mem_usage": True,
        "trust_remote_code": False,
    }
    if torch.cuda.is_available():
        model_kwargs["device_map"] = {"": 0}
    if mode == "qlora":
        model_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=dtype,
        )

    model = AutoModelForCausalLM.from_pretrained(config.model_id, **model_kwargs)
    model.config.use_cache = False
    return model, tokenizer


def apply_peft_if_needed(model: Any, config: FineTuningConfig) -> Any:
    mode = config.normalized_mode()
    if mode == "full":
        return model

    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

    if mode == "qlora":
        model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=LORA_TARGET_MODULES,
    )
    return get_peft_model(model, lora_config)


def run_fine_tuning(
    samples: list[dict[str, Any]],
    config: FineTuningConfig,
    *,
    report_progress: ProgressCallback | None = None,
    should_cancel: CancelCallback | None = None,
) -> TrainingResult:
    config.validate()
    mode = config.normalized_mode()
    if mode == "full":
        report_progress and report_progress(
            {
                "status": "loading_model",
                "warning": (
                    "Full fine-tuning may require high GPU memory. "
                    "If CUDA OOM occurs, use LoRA or QLoRA."
                ),
            }
        )

    train_samples, eval_samples = split_train_eval(samples, config.validation_split)
    output_dir = make_output_dir(config)
    logs: list[str] = []

    try:
        import torch
        from transformers import DataCollatorForLanguageModeling, Trainer
        from transformers import TrainingArguments

        report_progress and report_progress({"status": "loading_model"})
        model, tokenizer = load_model_for_training(config)
        model = apply_peft_if_needed(model, config)

        report_progress and report_progress({"status": "preparing_dataset"})
        train_dataset = tokenize_training_dataset(
            train_samples,
            tokenizer,
            config.max_seq_length,
        )
        eval_dataset = (
            tokenize_training_dataset(eval_samples, tokenizer, config.max_seq_length)
            if eval_samples
            else None
        )

        training_args = TrainingArguments(
            output_dir=str(output_dir / "checkpoints"),
            num_train_epochs=config.epochs,
            per_device_train_batch_size=config.batch_size,
            per_device_eval_batch_size=config.batch_size,
            gradient_accumulation_steps=config.gradient_accumulation,
            learning_rate=config.learning_rate,
            logging_steps=1,
            eval_strategy="steps" if eval_dataset is not None else "no",
            eval_steps=10 if eval_dataset is not None else None,
            save_strategy="epoch",
            report_to=[],
            fp16=torch.cuda.is_available() and not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_available() and torch.cuda.is_bf16_supported(),
            remove_unused_columns=False,
        )
        callbacks = [
            ProgressLoggingCallback(report_progress).to_trainer_callback(),
            CancelTrainingCallback(should_cancel).to_trainer_callback(),
        ]
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
            callbacks=callbacks,
        )

        report_progress and report_progress({"status": "training"})
        train_output = trainer.train()
        if should_cancel and should_cancel():
            return TrainingResult(
                status="cancelled",
                mode=mode,
                output_path=str(output_dir),
                message="Training cancelled at a safe callback boundary.",
                logs=logs,
            )

        eval_loss = None
        if eval_dataset is not None:
            metrics = trainer.evaluate()
            eval_loss = metrics.get("eval_loss")

        report_progress and report_progress({"status": "saving"})
        trainer.save_model(str(output_dir))
        tokenizer.save_pretrained(str(output_dir))
        zip_path = create_zip(output_dir) if mode in {"lora", "qlora"} else None
        return TrainingResult(
            status="completed",
            mode=mode,
            output_path=str(output_dir),
            zip_path=zip_path,
            train_loss=getattr(train_output, "training_loss", None),
            eval_loss=eval_loss,
            message="Training completed and output saved.",
            logs=logs,
        )
    except RuntimeError as exc:
        message = str(exc)
        if "out of memory" in message.lower() or "cuda" in message.lower():
            message = (
                f"{message}\nRecommendation: reduce batch size/max sequence "
                "length or use LoRA/QLoRA instead of full fine-tuning."
            )
        return TrainingResult(
            status="failed",
            mode=mode,
            output_path=str(output_dir),
            message=message,
            logs=logs,
        )
