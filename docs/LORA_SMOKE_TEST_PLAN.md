# LoRA Smoke Test Plan

## Purpose

Verify the complete demo path without claiming full model quality:

1. Load the curated mixed dataset.
2. Validate dataset quality.
3. Run a short LoRA training job from the browser UI.
4. Confirm progress, loss logs, cancellation path, and result summary.
5. Confirm adapter output and ZIP file.
6. Confirm the trained adapter becomes active for inference.
7. Run before/after Mermaid generation and validation.

## Recommended Runtime

- Google Colab GPU runtime.
- Default model: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`.
- Dataset: `datasets/curated/mixed_mindmap_venn_curated.jsonl`.

## Smoke Config

Use `configs/lora_smoke_config.json`:

- Mode: LoRA
- Max samples: 32
- Epochs: 1
- Batch size: 1
- Gradient accumulation: 4
- Max sequence length: 512
- Learning rate: `2e-4`
- Validation split: `0.1`

## UI Steps

1. Open `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` in Colab.
2. Run dependency install, imports, GPU check, model loading, and Gradio launch cells.
3. Open the Gradio link.
4. In **Dataset & Fine-Tuning**, upload `datasets/curated/mixed_mindmap_venn_curated.jsonl`.
5. Validate the dataset and confirm 150 valid samples.
6. Select LoRA.
7. Enter smoke config values.
8. Start Fine-Tuning.
9. Refresh status and capture logs/loss/progress.
10. Confirm output path and ZIP download.
11. Return to **Generator Mermaid** and generate one Mind Map and one Venn sample.

## Pass Criteria

- Dataset validates with zero invalid rows.
- Training status reaches completed.
- Logs include real loss/progress entries.
- Adapter path exists under `outputs/adapters/`.
- ZIP path exists for download.
- Active model/adaptor status changes.
- Generated Mermaid output validates as Mind Map or Venn.

## Fail Criteria

- CUDA unavailable for intended training run.
- bitsandbytes/CUDA incompatibility blocks QLoRA.
- CUDA out-of-memory interrupts training.
- Dataset validation reports zero valid samples.
- Training status is failed or cancelled.

Any failure must be recorded honestly in `docs/LORA_SMOKE_TEST_RESULT.md`.
