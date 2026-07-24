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
- Add MG-0003 final evidence package: Colab runtime report, real local Gradio screenshots, LoRA smoke evidence, before/after evaluation evidence, final demo script, and final submission checklist.
- Fix curated dataset validation script path handling for relative paths.
- Add MG-0004 render fix: stronger prompt templates, robust Mermaid extraction, Venn and Mind Map repair compilers, stricter Venn syntax, dataset alignment, final-code UI output, and render-fix evidence screenshots.
- Fix Gradio Mermaid preview rendering by moving Mermaid.js execution into an iframe `srcdoc` renderer; local evidence confirms visible Mind Map and Venn SVG output.
- Add MG-0005 local-first launch support with `--local`, `--share`, `--colab`, `--host`, and `--port`.
- Redesign the Gradio UI with a navy/orange/black theme, cleaner Generator and Dataset & Fine-Tuning layouts, and dataset validation cards.
- Document local laptop and Colab/share launch modes with local smoke evidence.
- Add MG-0006 final QA audit, final regression tests, stabilized notebook access notes, final submission package guide, and troubleshooting guide.
- Verify final release readiness: notebook JSON, curated dataset, local/share launch config, Mermaid repair/preview tests, and Git hygiene without committed model artifacts.
- Add MG-0007 expanded datasets: 500 Mind Map, 500 Venn, balanced 500/1000 mixed training datasets, and 100 final evaluation prompts.
- Add deterministic dataset builder, expanded dataset validation, quality reports, final quality evaluation runner, and LoRA configs for smoke, medium, and expanded dataset runs.
- Add expanded dataset regression tests and polish demo UI wording for dataset readiness and syntax-safety fallback.
- Add MG-0008 final submission README, manifest, ZIP packaging scripts, verification script, detailed Indonesian video demo script, narration scripts, notebook/source walkthroughs, and dataset video explanation.
- Verify local final submission package generation at `dist/MermaidGenerate_Final_Submission.zip`; ZIP remains an ignored reproducible build artifact.
