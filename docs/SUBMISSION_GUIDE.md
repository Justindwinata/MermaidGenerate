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

Do not submit generated model weights unless explicitly requested. `outputs/` is gitignored because training artifacts can be large.

## Demo Flow

1. Open the notebook in Google Colab.
2. Select GPU runtime.
3. Run installation and import cells.
4. Run GPU check.
5. Validate curated dataset.
6. Load model.
7. Launch Gradio.
8. Show **Generator Mermaid** with one Mind Map and one Venn prompt.
9. Show **Dataset & Fine-Tuning** upload and validation.
10. Run LoRA smoke training only if GPU is available.
11. Refresh status until real logs/progress are visible.
12. Download adapter ZIP after successful LoRA/QLoRA.
13. Generate another diagram after adapter activation.

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

## Evidence

Use `docs/SCREENSHOT_CAPTURE_PLAN.md` as the screenshot checklist. Add screenshots only after a real run. If no GPU run was executed, submit the plan and `docs/LORA_SMOKE_TEST_RESULT.md` with the honest not-executed status.
