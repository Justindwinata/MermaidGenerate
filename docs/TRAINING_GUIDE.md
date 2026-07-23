# Training Guide

## Recommended Mode

Start with LoRA. It is the most practical mode for Colab-scale experiments.

Recommended smoke values:

- dataset: `datasets/curated/mixed_mindmap_venn_curated.jsonl`
- epochs: `1`
- batch size: `1`
- gradient accumulation: `4`
- max sequence length: `512`
- learning rate: `2e-4`
- validation split: `0.1`

## QLoRA 4-bit

Use QLoRA when CUDA and bitsandbytes are available. If loading fails, switch to LoRA or reduce memory settings.

## Full Fine-Tuning

Full fine-tuning trains all model weights and can fail on limited GPU memory. The project reports the real error and recommends smaller settings or PEFT modes.

## Output Paths

- LoRA/QLoRA: `outputs/adapters/<timestamp>/`
- Full Fine-Tuning: `outputs/full_models/<timestamp>/`

LoRA/QLoRA adapters are zipped for download.

The adapter ZIP appears in the UI after successful LoRA/QLoRA training and after clicking **Refresh Status** if the job completed in the background.

## Generation Reliability Note

LoRA smoke training can complete successfully while the model still produces imperfect Mermaid syntax. The runtime therefore uses extraction, validation, and deterministic repair/compile fallback before rendering. This guard keeps the UI demo reliable without claiming the model itself is perfect.

## Demo Honesty

Do not claim training success unless the UI reports completed status and real logs/loss are visible. If CUDA is unavailable or a training mode fails because of memory or bitsandbytes compatibility, report the exact error and switch to LoRA or smaller settings.
