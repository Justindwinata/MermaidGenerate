# Training Guide

## Recommended Mode

Start with LoRA. It is the most practical mode for Colab-scale experiments.

## QLoRA 4-bit

Use QLoRA when CUDA and bitsandbytes are available. If loading fails, switch to LoRA or reduce memory settings.

## Full Fine-Tuning

Full fine-tuning trains all model weights and can fail on limited GPU memory. The project reports the real error and recommends smaller settings or PEFT modes.

## Output Paths

- LoRA/QLoRA: `outputs/adapters/<timestamp>/`
- Full Fine-Tuning: `outputs/full_models/<timestamp>/`

LoRA/QLoRA adapters are zipped for download.

## Generation Reliability Note

LoRA smoke training can complete successfully while the model still produces imperfect Mermaid syntax. The runtime therefore uses extraction, validation, and deterministic repair/compile fallback before rendering. This guard keeps the UI demo reliable without claiming the model itself is perfect.
