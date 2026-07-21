# LoRA Smoke Training Evidence

Report date: 2026-07-22 Asia/Jakarta

## Execution Status

Real LoRA smoke training was **not executed** in this local agent environment.

## Reason

The local environment does not expose a CUDA GPU:

- `torch.cuda.is_available()`: `False`

Running the configured LoRA smoke training on CPU would be slow, not representative of the intended Colab GPU demo, and could produce misleading runtime evidence.

## Runtime Type

- Runtime type: local macOS workspace, not Colab
- Training mode intended: LoRA
- GPU: not available

## Dataset and Config Prepared

- Config: `configs/lora_smoke_config.json`
- Dataset: `datasets/curated/mixed_mindmap_venn_curated.jsonl`
- Dataset samples available: 150
- Intended max samples for smoke test: 32
- Epochs: 1
- Batch size: 1
- Gradient accumulation: 4
- Max sequence length: 512
- Learning rate: `2e-4`
- Validation split: `0.1`

## Final Status

- Training final status: not executed
- Final loss: not available
- Validation loss: not available
- Adapter output path: not available
- Adapter ZIP path: not available
- Active adapter status: not changed

## Screenshot References

- Ready-state UI screenshot: `docs/evidence/screenshots/08_training_logs_or_ready_state.png`
- Training controls screenshot: `docs/evidence/screenshots/07_training_controls.png`

These screenshots show the UI path is ready, not that training completed.

## Required Colab GPU Follow-Up

To produce real training evidence:

1. Open the notebook in Google Colab.
2. Select GPU runtime.
3. Confirm `torch.cuda.is_available() == True`.
4. Launch Gradio.
5. Upload and validate `datasets/curated/mixed_mindmap_venn_curated.jsonl`.
6. Enter `configs/lora_smoke_config.json` values.
7. Start LoRA training from the browser UI.
8. Record start/end time, duration, final status, loss logs, adapter path, ZIP path, and active adapter status.
9. Capture real training logs and adapter download screenshots.

No adapter or ZIP success is claimed until that Colab GPU run completes.
