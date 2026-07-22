# Local UI Revision Plan

Plan date: 2026-07-23 Asia/Jakarta

## Current Behavior

MermaidGenerate currently launches through `app.py` with:

- host default: `127.0.0.1`
- port default: `7860`
- share default: `False`
- optional public Gradio link through `--share`

The Google Colab notebook imports the same helper modules and launches the Gradio app for browser use. In Colab, a public share link is useful because Colab localhost is not directly reachable from the user's laptop browser.

## What Will Change

The revision will make the launch behavior explicit:

- `python app.py` starts local mode.
- `python app.py --local` starts local mode.
- `python app.py --host 127.0.0.1 --port 7860` can override local bind settings.
- `python app.py --share` enables a Gradio public link.
- `python app.py --colab` enables Colab-friendly share mode.
- startup logs will clearly print mode, host, port, local URL, and share guidance.

The Gradio UI will be restyled with a navy, orange, and black/dark visual system while preserving the existing two-tab Gradio layout.

## What Must Not Change

The following functions and modules must remain available and functional:

- dataset loader
- dataset validator
- Mermaid validator
- iframe Mermaid preview renderer
- Mind Map repair compiler
- Venn repair compiler
- model loader
- Transformers/PyTorch inference pipeline
- training manager
- adapter manager
- Gradio UI callbacks
- Colab notebook launch flow
- LoRA, QLoRA 4-bit, and Full Fine-Tuning controls
- adapter ZIP download

The runtime must remain Transformers + PyTorch + PEFT. llama.cpp/GGUF remains future optional compatibility only.

## Verification Plan

Function preservation will be checked with:

- `pytest -q`
- `python3 -m compileall src app.py`
- `python app.py --help`
- launch configuration tests for local/share/Colab modes
- preview renderer tests for iframe output and Venn `venn-beta` conversion
- dataset validator tests against the curated mixed dataset
- local smoke start where possible with `python app.py --local --port 7860`

Manual UI smoke criteria:

- Generator Mermaid tab loads.
- Dataset & Fine-Tuning tab loads.
- Mind Map prompt returns final valid `mindmap` code and rendered preview.
- Venn prompt returns final valid `venn` code and rendered preview.
- Dataset validation still reports curated dataset as train-ready.
- Training controls, logs, status, cancel, adapter activation, and adapter ZIP download remain visible.
