# LoRA Smoke Test Result

Result date: 2026-07-22 Asia/Jakarta

## Execution Status

Real LoRA smoke training was **not executed** in the local MG-0002 environment.

## Local Environment Observed

- Python: 3.12.2
- Platform: macOS-14.4.1-arm64-arm-64bit
- PyTorch: 2.8.0
- CUDA available: `False`

## Reason

The available local environment does not expose a CUDA GPU. Running LoRA training on CPU would be slow and not representative of the intended Colab GPU assignment demo.

## Prepared Path

- Config exists: `configs/lora_smoke_config.json`
- Dataset exists: `datasets/curated/mixed_mindmap_venn_curated.jsonl`
- Dataset validation result: 150 valid samples, 0 invalid samples
- Browser UI training path exists in **Dataset & Fine-Tuning**
- Adapter activation/download path exists in backend and UI

## Required Future Result Fields After Colab GPU Run

When the smoke test is executed in Colab GPU, update this file with:

- Runtime type
- GPU name
- Start/end time and duration
- Final training status
- Final train/eval loss if available
- Adapter output path
- Adapter ZIP path
- Active adapter status text
- Before/after prompt
- Before/after Mermaid output validation result
- Any error message if failed

No training success is claimed until those fields are filled from a real run.
