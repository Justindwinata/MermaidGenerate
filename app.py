"""Gradio web application for MermaidGenerate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mermaid_generate.adapter_manager import current_adapter_metadata
from mermaid_generate.dataset_validator import validate_dataset_file
from mermaid_generate.inference import GenerationSettings, generate_mermaid
from mermaid_generate.mermaid_preview import build_mermaid_preview_html
from mermaid_generate.training import FineTuningConfig
from mermaid_generate.training_manager import TRAINING_MANAGER


APP_TITLE = "MermaidGenerate - Local AI Mermaid Diagram Generator"
APP_SUBTITLE = (
    "Generate Mind Map and Venn Diagram Mermaid code using a locally "
    "fine-tuned Transformers/PyTorch model."
)

APP_CSS = """
.mg-status {
  border: 1px solid #d8dee8;
  border-radius: 8px;
  padding: 12px;
  background: #f7f9fc;
}
.mg-note {
  color: #475569;
  font-size: 0.92rem;
}
.mg-preview pre {
  white-space: pre-wrap;
}
.mg-preview-status {
  color: #b42318;
  font-weight: 600;
}
"""

DATASET_STATE: dict[str, Any] = {
    "path": None,
    "report": None,
    "valid_data": [],
}
LAST_TRAINING_JOB_ID: str | None = None


def readable_model_status() -> str:
    metadata = current_adapter_metadata()
    suffix = (
        "\nRuntime: Transformers + PyTorch. "
        "Venn preview renders assignment-facing 'venn' code through Mermaid 'venn-beta'."
    )
    return metadata.status + suffix


def normalize_ui_diagram_type(value: str) -> str:
    mapping = {
        "Mind Map": "mindmap",
        "Venn Diagram": "venn",
        "Auto Detect": "auto",
    }
    return mapping.get(value, "auto")


def generate_from_ui(
    diagram_type: str,
    prompt: str,
    max_new_tokens: int,
    temperature: float,
    top_p: float,
    repetition_penalty: float,
) -> tuple[str, str, str, str, str]:
    if not prompt or not prompt.strip():
        code = ""
        preview = build_mermaid_preview_html("")
        return (
            readable_model_status(),
            code,
            preview,
            "Prompt cannot be empty.",
            "0.00 s",
        )

    try:
        result = generate_mermaid(
            prompt,
            normalize_ui_diagram_type(diagram_type),
            GenerationSettings(
                max_new_tokens=int(max_new_tokens),
                temperature=float(temperature),
                top_p=float(top_p),
                repetition_penalty=float(repetition_penalty),
            ),
        )
        preview = build_mermaid_preview_html(result.code)
        return (
            result.model_status,
            result.code,
            preview,
            result.validation_message,
            f"{result.inference_time_seconds:.2f} s",
        )
    except Exception as exc:
        code = ""
        return (
            readable_model_status(),
            code,
            build_mermaid_preview_html(code),
            f"Inference failed: {exc}",
            "0.00 s",
        )


def clear_generator() -> tuple[str, str, str, str]:
    return "", build_mermaid_preview_html(""), "Waiting for generation.", "0.00 s"


def validate_upload(file_obj: Any) -> tuple[list[list[Any]], str, str, str, str]:
    if file_obj is None:
        DATASET_STATE.update({"path": None, "report": None, "valid_data": []})
        return [], "No dataset uploaded.", "{}", "{}", "No invalid rows."

    path = Path(getattr(file_obj, "name", str(file_obj)))
    report = validate_dataset_file(path)
    DATASET_STATE["path"] = str(path)
    DATASET_STATE["report"] = report.as_dict()
    DATASET_STATE["valid_data"] = report.valid_data

    preview_rows = [
        [
            sample["id"],
            sample["diagram_type"],
            sample["source_format"],
            sample["language"],
            sample["domain"],
            sample["complexity"],
            sample["prompt"][:120],
            sample["target"][:160],
        ]
        for sample in report.valid_data[:10]
    ]
    summary = (
        f"File: {path.name}\n"
        f"Total: {report.total_samples}\n"
        f"Valid: {report.valid_samples}\n"
        f"Invalid: {report.invalid_samples}\n"
        f"Warnings: {report.warning_samples}\n"
        f"Duplicates: {report.duplicate_count}\n"
        f"Train ready: {report.train_ready}\n"
        f"Error: {report.error or '-'}"
    )
    invalid_text = "\n".join(
        f"Row {row['row_index']}: {', '.join(row['reasons'])}"
        for row in report.invalid_rows[:10]
    ) or "No invalid rows."
    return (
        preview_rows,
        summary,
        str(report.diagram_type_counts),
        str(report.source_format_counts),
        invalid_text,
    )


def start_training_from_ui(
    mode: str,
    epochs: float,
    learning_rate: float,
    batch_size: int,
    gradient_accumulation: int,
    max_seq_length: int,
    validation_split: float,
) -> tuple[str, str, str, str | None, str]:
    global LAST_TRAINING_JOB_ID

    valid_data = DATASET_STATE.get("valid_data") or []
    if not valid_data:
        return (
            "failed",
            "No valid dataset samples. Upload and validate a dataset first.",
            "",
            None,
            readable_model_status(),
        )

    config = FineTuningConfig(
        mode=mode,
        epochs=float(epochs),
        learning_rate=float(learning_rate),
        batch_size=int(batch_size),
        gradient_accumulation=int(gradient_accumulation),
        max_seq_length=int(max_seq_length),
        validation_split=float(validation_split),
    )
    try:
        LAST_TRAINING_JOB_ID = TRAINING_MANAGER.start(valid_data, config)
        return (
            "training",
            (
                f"Training job started: {LAST_TRAINING_JOB_ID}\n"
                "Use Refresh Status to read real progress/loss logs. "
                "Do not close the runtime during training."
            ),
            LAST_TRAINING_JOB_ID,
            None,
            readable_model_status(),
        )
    except Exception as exc:
        return "failed", str(exc), "", None, readable_model_status()


def refresh_training_status() -> tuple[str, str, str, str | None, str]:
    job_id = LAST_TRAINING_JOB_ID
    if not job_id:
        return "idle", "No training job started.", "", None, readable_model_status()
    state = TRAINING_MANAGER.get(job_id)
    if state is None:
        return "failed", f"Training job not found: {job_id}", "", None, readable_model_status()

    if state.status == "completed" and state.activation is None:
        try:
            metadata = TRAINING_MANAGER.activate_completed_result(job_id)
            state.activation = metadata.as_dict()
            state.logs.append(f"Activated training output: {metadata.status}")
        except Exception as exc:
            state.logs.append(f"Activation failed: {exc}")

    result = state.result
    download_path = result.zip_path if result and result.zip_path else None
    result_summary = ""
    if result is not None:
        result_summary = (
            f"Status: {result.status}\n"
            f"Mode: {result.mode}\n"
            f"Output: {result.output_path}\n"
            f"ZIP: {result.zip_path}\n"
            f"Train loss: {result.train_loss}\n"
            f"Eval loss: {result.eval_loss}\n"
            f"Message: {result.message}"
        )
    else:
        result_summary = f"Progress: {state.progress:.0%}\nMetrics: {state.latest_metrics}"

    logs = "\n".join(state.logs[-80:])
    return state.status, result_summary, logs, download_path, readable_model_status()


def cancel_training() -> tuple[str, str]:
    if not LAST_TRAINING_JOB_ID:
        return "idle", "No active training job."
    try:
        TRAINING_MANAGER.cancel(LAST_TRAINING_JOB_ID)
        return "cancelling", "Cancellation requested."
    except Exception as exc:
        return "failed", str(exc)


def clear_training_state() -> tuple[str, str, str, str | None]:
    global LAST_TRAINING_JOB_ID
    try:
        TRAINING_MANAGER.clear()
        LAST_TRAINING_JOB_ID = None
        return "idle", "Training state cleared.", "", None
    except Exception as exc:
        return "failed", str(exc), "", None


def build_app() -> Any:
    import gradio as gr

    with gr.Blocks(title=APP_TITLE, css=APP_CSS) as demo:
        gr.Markdown(f"# {APP_TITLE}\n{APP_SUBTITLE}")
        gr.Markdown(
            "Primary runtime: **Transformers + PyTorch + PEFT**. "
            "No paid API is used. Venn diagrams are generated as `venn` for the assignment "
            "and rendered internally through Mermaid's current `venn-beta` preview syntax."
        )
        with gr.Tabs():
            with gr.Tab("Generator Mermaid"):
                model_status = gr.Textbox(
                    value=readable_model_status,
                    label="Active model/adaptor status",
                    interactive=False,
                )
                with gr.Row():
                    with gr.Column(scale=1):
                        diagram_type = gr.Dropdown(
                            ["Mind Map", "Venn Diagram", "Auto Detect"],
                            value="Auto Detect",
                            label="Diagram type",
                        )
                        prompt = gr.Textbox(
                            label="Prompt",
                            lines=8,
                            placeholder="Create a mind map about online learning...",
                        )
                        with gr.Row():
                            generate_button = gr.Button("Generate", variant="primary")
                            clear_button = gr.Button("Clear")
                        gr.Examples(
                            examples=[
                                ["Mind Map", "Buat mind map tentang strategi belajar AI untuk mahasiswa informatika."],
                                ["Mind Map", "Create a mind map about digital marketing for a small food business."],
                                ["Venn Diagram", "Create a Venn diagram comparing students, employees, and entrepreneurs."],
                                ["Venn Diagram", "Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing."],
                                ["Auto Detect", "Compare cloud computing, edge computing, and on-premise infrastructure."],
                            ],
                            inputs=[diagram_type, prompt],
                        )
                    with gr.Column(scale=1):
                        max_new_tokens = gr.Slider(64, 1024, value=320, step=16, label="max_new_tokens")
                        temperature = gr.Slider(0.0, 1.5, value=0.2, step=0.05, label="temperature")
                        top_p = gr.Slider(0.1, 1.0, value=0.9, step=0.05, label="top_p")
                        repetition_penalty = gr.Slider(1.0, 1.5, value=1.05, step=0.01, label="repetition_penalty")
                        inference_time = gr.Textbox(label="Inference time", value="0.00 s", interactive=False)
                        validation_result = gr.Textbox(label="Mermaid syntax validation", lines=4, interactive=False)
                with gr.Row():
                    code_output = gr.Code(label="Copyable Mermaid code", language="markdown", lines=16)
                    preview_output = gr.HTML(label="Rendered Mermaid preview", value=build_mermaid_preview_html(""))

                generate_button.click(
                    generate_from_ui,
                    inputs=[
                        diagram_type,
                        prompt,
                        max_new_tokens,
                        temperature,
                        top_p,
                        repetition_penalty,
                    ],
                    outputs=[
                        model_status,
                        code_output,
                        preview_output,
                        validation_result,
                        inference_time,
                    ],
                )
                clear_button.click(
                    clear_generator,
                    outputs=[
                        code_output,
                        preview_output,
                        validation_result,
                        inference_time,
                    ],
                )

            with gr.Tab("Dataset & Fine-Tuning"):
                gr.Markdown(
                    "Upload JSON/JSONL with messages, prompt-completion, or instruction-output samples. "
                    "For the MG-0002 smoke demo, use `datasets/curated/mixed_mindmap_venn_curated.jsonl`."
                )
                dataset_file = gr.File(
                    label="Dataset upload",
                    file_types=[".json", ".jsonl"],
                )
                validate_button = gr.Button("Validate Dataset", variant="primary")
                dataset_preview = gr.Dataframe(
                    headers=[
                        "id",
                        "diagram_type",
                        "source_format",
                        "language",
                        "domain",
                        "complexity",
                        "prompt",
                        "target",
                    ],
                    label="Dataset preview",
                    interactive=False,
                )
                with gr.Row():
                    validation_summary = gr.Textbox(label="Validation summary", lines=8)
                    invalid_rows = gr.Textbox(label="Invalid rows preview", lines=8)
                with gr.Row():
                    diagram_distribution = gr.Textbox(label="Diagram type distribution")
                    source_distribution = gr.Textbox(label="Source format distribution")

                validate_button.click(
                    validate_upload,
                    inputs=[dataset_file],
                    outputs=[
                        dataset_preview,
                        validation_summary,
                        diagram_distribution,
                        source_distribution,
                        invalid_rows,
                    ],
                )

                gr.Markdown("### Fine-Tuning")
                gr.Markdown(
                    "Recommended LoRA smoke values: 1 epoch, batch size 1, gradient accumulation 4, "
                    "max sequence length 512, learning rate 2e-4, validation split 0.1. "
                    "Training is real; progress appears after clicking Refresh Status."
                )
                with gr.Row():
                    mode = gr.Dropdown(
                        ["LoRA", "QLoRA 4-bit", "Full Fine-Tuning"],
                        value="LoRA",
                        label="Fine-tuning mode",
                    )
                    epochs = gr.Number(value=1, label="epochs")
                    learning_rate = gr.Number(value=2e-4, label="learning rate")
                with gr.Row():
                    batch_size = gr.Number(value=1, label="batch size", precision=0)
                    gradient_accumulation = gr.Number(value=4, label="gradient accumulation", precision=0)
                    max_seq_length = gr.Number(value=1024, label="max sequence length", precision=0)
                    validation_split = gr.Slider(0.0, 0.5, value=0.1, step=0.05, label="validation split ratio")

                with gr.Row():
                    start_button = gr.Button("Start Fine-Tuning", variant="primary")
                    cancel_button = gr.Button("Cancel Training")
                    refresh_button = gr.Button("Refresh Status")
                    clear_training_button = gr.Button("Clear Training State")

                training_status = gr.Textbox(label="Training status", value="idle")
                job_id_box = gr.Textbox(label="Training job id")
                result_summary = gr.Textbox(label="Result summary / progress display", lines=8)
                training_logs = gr.Textbox(label="Training logs and loss logs", lines=12)
                active_status = gr.Textbox(
                    label="Active adapter/model status",
                    value=readable_model_status,
                    interactive=False,
                )
                adapter_download = gr.File(label="Download ZIP for LoRA/QLoRA adapter")

                start_button.click(
                    start_training_from_ui,
                    inputs=[
                        mode,
                        epochs,
                        learning_rate,
                        batch_size,
                        gradient_accumulation,
                        max_seq_length,
                        validation_split,
                    ],
                    outputs=[
                        training_status,
                        result_summary,
                        job_id_box,
                        adapter_download,
                        active_status,
                    ],
                )
                refresh_button.click(
                    refresh_training_status,
                    outputs=[
                        training_status,
                        result_summary,
                        training_logs,
                        adapter_download,
                        active_status,
                    ],
                )
                cancel_button.click(
                    cancel_training,
                    outputs=[training_status, result_summary],
                )
                clear_training_button.click(
                    clear_training_state,
                    outputs=[
                        training_status,
                        result_summary,
                        training_logs,
                        adapter_download,
                    ],
                )

        gr.Markdown(
            "Limitations: model quality depends on dataset size and training; example datasets are small; "
            "full fine-tuning may require high GPU memory; QLoRA requires CUDA/bitsandbytes; "
            "Venn preview uses Mermaid v11 venn-beta renderer support; llama.cpp/GGUF is future optional compatibility; "
            "no paid API is used."
        )
    return demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument("--host", default="127.0.0.1", help="Host interface.")
    parser.add_argument("--port", default=7860, type=int, help="Port.")
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a Gradio share URL. Useful in Colab.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    app = build_app()
    app.launch(server_name=args.host, server_port=args.port, share=args.share)


if __name__ == "__main__":
    main()
