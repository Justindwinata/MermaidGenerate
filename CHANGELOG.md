# Changelog

## Unreleased

- Initialize MermaidGenerate notebook-first project.
- Add reference notebook inspection foundation.
- Add dataset loader and validator for messages, prompt-completion, and instruction-output formats.
- Add Mermaid Mind Map and Venn validation plus Mermaid.js preview rendering.
- Add Transformers/PyTorch inference pipeline with TinyLlama default.
- Add LoRA, QLoRA 4-bit, and Full Fine-Tuning backend.
- Add adapter activation, ZIP artifact handling, and evaluation utilities.
- Add Gradio web UI with Generator Mermaid and Dataset & Fine-Tuning tabs.
- Add Google Colab notebook deliverable.
- Add example Mind Map and Venn datasets.
- Document limitations: llama.cpp/GGUF is future optional compatibility, full fine-tuning may need high GPU memory, QLoRA requires CUDA/bitsandbytes, Venn depends on Mermaid v11 support, and no paid API is used.
- Polish Colab notebook QA flow with GPU check, demo steps, common errors, and smoke-training guidance.
- Add curated datasets: 75 Mind Map, 75 Venn, and 150 balanced mixed examples.
- Add curated dataset validation script and report.
- Add manual evaluation prompts, validator-only baseline report, and optional model inference runner.
- Add LoRA smoke config, smoke test plan, and honest not-executed local result because CUDA is unavailable.
- Polish Gradio demo copy and README/submission documentation.
- Add screenshot capture plan without fake screenshots.
