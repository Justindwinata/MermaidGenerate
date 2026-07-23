# Final Submission Checklist

## Required Files

- [x] Notebook exists: `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`
- [x] Web app exists: `app.py`
- [x] Source package exists: `src/mermaid_generate/`
- [x] Requirements exist: `requirements.txt`
- [x] README exists: `README.md`
- [x] Documentation exists: `docs/`
- [x] Local run guide exists: `docs/LOCAL_RUN_GUIDE.md`
- [x] Local UI revision plan exists: `docs/LOCAL_UI_REVISION_PLAN.md`
- [x] Final QA audit exists: `docs/FINAL_QA_AUDIT.md`
- [x] Final submission package guide exists: `docs/FINAL_SUBMISSION_PACKAGE.md`

## Launch Modes

- [x] Local-first command documented: `python app.py --local`.
- [x] Default local URL documented: `http://127.0.0.1:7860`.
- [x] Colab/share mode documented: `python app.py --colab` or notebook `share=True`.
- [x] Gradio Live is optional for local laptop usage.

## Dataset Files

- [x] Starter Mind Map examples exist.
- [x] Starter Venn examples exist.
- [x] Curated Mind Map dataset exists.
- [x] Curated Venn dataset exists.
- [x] Curated mixed dataset exists.
- [x] Manual evaluation prompts exist.

## Evidence Status

- [x] Colab runtime report exists.
- [x] Screenshot evidence report exists.
- [x] Real local Gradio screenshots exist.
- [x] LoRA smoke training evidence report exists.
- [x] Before/after LoRA evaluation evidence report exists.
- [x] Final demo script exists.
- [x] Generation failure analysis exists.
- [x] Generator runtime evidence exists.
- [x] Render-fix screenshots exist, including iframe preview evidence for visible Mind Map and Venn SVG diagrams.

## LoRA Smoke Test Status

- [ ] Real Colab GPU LoRA smoke training completed.
- [ ] Adapter ZIP generated from real training.
- [ ] Before/after model metrics recorded.

Current status: not completed locally because CUDA is unavailable.

## Repository Hygiene

- [x] `outputs/` is gitignored except `.gitkeep`.
- [x] No checkpoints or model weights are committed.
- [x] Evidence screenshots are lightweight.
- [x] Tests pass.
- [x] Curated dataset validation passes.
- [x] Large model/checkpoint outputs are not committed.

## Known Limitations to State

- Colab GPU training evidence still requires user-side execution.
- Screenshots of actual generation/training success require a real model/training run.
- Local mode requires dependencies installed on the local machine.
- Local model loading may require enough RAM or VRAM.
- Colab still benefits from a Gradio public share link for browser access.
- Model quality depends on dataset size and training.
- Full Fine-Tuning may fail on limited GPU.
- QLoRA requires compatible CUDA/bitsandbytes.
- Venn rendering depends on Mermaid.js support.
- llama.cpp/GGUF remains future optional compatibility.
- No paid API is used.
- Repair fallback is used to guarantee valid Mermaid syntax when raw model output is invalid.
