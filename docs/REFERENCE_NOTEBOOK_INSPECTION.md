# Reference Notebook Inspection

Inspection date: 2026-07-22

## `2fa1391d-0227-4bdc-b8d0-13379ae145a6.ipynb`

This notebook contains a flowchart-focused Mermaid generator. It installs `llama-cpp-python`, detects the Colab CUDA environment, loads a GGUF Gemma wrapper model, then exposes a Flask-based web app with Mermaid v11 rendering and Cloudflare Tunnel access.

Useful implementation references:

- Colab environment readiness checks.
- Background generation job structure.
- Mermaid output cleanup before rendering.
- Browser rendering pattern using a pinned Mermaid script.
- User-facing render error handling.

Items intentionally not copied into MermaidGenerate:

- The primary llama.cpp/GGUF runtime.
- Gemma4 GGUF model identity.
- Flowchart target behavior.
- Flask-first app structure.

Reason: MG-0001 requires Transformers and PyTorch inference as the primary runtime and restricts final generation targets to Mind Map and Venn Diagram.

## `llm-012-qwen2.5-1.5b-web-upload-finetuning-ui.ipynb`

This notebook is closer to the required architecture. It uses Hugging Face Transformers and PyTorch, supports dataset upload, dataset validation, LoRA/QLoRA/full fine-tuning, browser-triggered training, cancellation, logs, result download, and active adapter/model updates.

Useful implementation references:

- Dependency version pinning for Transformers, Datasets, PEFT, Accelerate, and bitsandbytes.
- Dataset normalization from common supervised fine-tuning formats.
- Browser-driven training job state.
- Honest progress and loss reporting through training callbacks.
- Adapter saving, ZIP download, and active adapter activation.
- Runtime restart warnings when package versions change in Colab.

Items intentionally not copied into MermaidGenerate:

- Qwen project identity as the main project model.
- Flowchart-oriented prompting and validation.
- Flask UI implementation details where Gradio Blocks is required.

Decision for MermaidGenerate:

- Use `TinyLlama/TinyLlama-1.1B-Chat-v1.0` as the default local-friendly LLaMA-family model.
- Use Transformers and PyTorch for inference and fine-tuning.
- Use PEFT for LoRA/QLoRA.
- Use Gradio Blocks with two tabs: Generator Mermaid and Dataset & Fine-Tuning.
- Pin Mermaid.js to a version that supports Mind Map and Venn. Mermaid official documentation identifies Venn as `venn-beta` in Mermaid `v11.12.3+`; this project pins a newer v11 release and accepts `venn` by normalizing it to renderer-compatible `venn-beta` for preview.
