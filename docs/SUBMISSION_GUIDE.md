# Submission Guide

## What to Submit

Submit the repository with the primary notebook:

- `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`

Also include:

- `app.py`
- `src/mermaid_generate/`
- `requirements.txt`
- `datasets/examples/`
- `datasets/curated/`
- `datasets/evaluation/manual_eval_prompts.jsonl`
- `docs/`

Use `docs/FINAL_SUBMISSION_PACKAGE.md` as the exact final package checklist.

Do not submit generated model weights unless explicitly requested. `outputs/` is gitignored because training artifacts can be large.

## Demo Flow

1. Open the notebook in Google Colab.
2. Select GPU runtime.
3. Run installation and import cells.
4. Run GPU check.
5. Validate curated dataset.
6. Load model.
7. Launch Gradio.
8. Open the generated `gradio.live` link in Colab. Do not open `0.0.0.0:7860`.
9. Show **Generator Mermaid** with one Mind Map and one Venn prompt.
10. Show **Dataset & Fine-Tuning** upload and validation.
11. Run LoRA smoke training only if GPU is available.
12. Refresh status until real logs/progress are visible.
13. Download adapter ZIP after successful LoRA/QLoRA.
14. Generate another diagram after adapter activation.

For a local laptop demo:

```bash
python app.py --local
```

Open:

```text
http://127.0.0.1:7860
```

## Explaining Training Modes

- **LoRA:** trains small adapter weights while base model remains mostly frozen. Recommended for smoke demo.
- **QLoRA 4-bit:** loads base model in 4-bit with bitsandbytes and trains adapters. Requires compatible CUDA.
- **Full Fine-Tuning:** updates all model weights. It is expensive and may fail on limited GPU memory.

## Explaining Limitations Honestly

State clearly:

- The runtime is Transformers/PyTorch, not paid API inference.
- llama.cpp/GGUF is future optional compatibility only.
- Example and curated datasets are useful for demo but still need human review.
- Model quality depends on dataset size and real training.
- Full Fine-Tuning may fail on limited GPU memory.
- QLoRA depends on CUDA/bitsandbytes compatibility.
- Venn rendering depends on Mermaid.js support.
- Local mode uses `127.0.0.1`; Colab uses a `gradio.live` public link.
- `0.0.0.0` is a bind address, not a browser URL.

## Evidence

Use `docs/SCREENSHOT_CAPTURE_PLAN.md` as the screenshot checklist. Add screenshots only after a real run. If no GPU run was executed, submit the plan and `docs/LORA_SMOKE_TEST_RESULT.md` with the honest not-executed status.

MG-0003 evidence files are stored in `docs/evidence/`:

- `COLAB_RUNTIME_REPORT.md`
- `SCREENSHOT_EVIDENCE_REPORT.md`
- `LORA_SMOKE_TRAINING_EVIDENCE.md`
- `BEFORE_AFTER_LORA_EVALUATION.md`
- `LOCAL_UI_REVISION_EVIDENCE.md`
- `screenshots/`

Use `docs/FINAL_DEMO_SCRIPT.md` for the live demo flow, `docs/FINAL_QA_AUDIT.md` for readiness status, and `docs/FINAL_SUBMISSION_CHECKLIST.md` as the final package checklist.
