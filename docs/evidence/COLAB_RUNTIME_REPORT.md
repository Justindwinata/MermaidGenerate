# Colab Runtime Report

Report date: 2026-07-22 Asia/Jakarta

## Execution Status

Google Colab was **not executed from this agent environment**.

## Reason

The agent is running in a local macOS workspace and does not have direct control over a Google Colab browser runtime or a Colab GPU session. Claiming Colab execution, GPU availability, training success, or notebook cell success from this environment would be inaccurate.

## Local Environment Observed

- Runtime type: local macOS workspace, not Colab
- Python: 3.12.2
- Platform: macOS-14.4.1-arm64-arm-64bit
- PyTorch: 2.8.0
- CUDA available: `False`
- GPU name: not available

## Notebook Cells Reviewed

The notebook contains clear sections for:

1. Install dependencies
2. Runtime restart note
3. Import libraries
4. GPU/runtime check
5. Project/helper module loading
6. Model loading
7. Sample inference
8. Gradio app launch
9. Dataset upload
10. Dataset validation
11. LoRA/QLoRA/Full FT instructions
12. Adapter ZIP download instructions
13. Evaluation utilities
14. Screenshot/demo evidence guidance
15. Notes, limitations, and submission guide

## User-Side Colab Verification Steps

1. Open `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` in Google Colab.
2. Select **Runtime > Change runtime type > GPU**.
3. Run the install dependency cell.
4. If package versions are changed after import, restart runtime and rerun from the first cell.
5. Run the GPU check cell and record:
   - `torch.cuda.is_available()`
   - GPU name
   - PyTorch version
   - CUDA runtime version
6. Run import/configuration cells.
7. Load `TinyLlama/TinyLlama-1.1B-Chat-v1.0`.
8. Launch Gradio with `share=True`.
9. Generate one Mind Map and one Venn example.
10. Upload `datasets/curated/mixed_mindmap_venn_curated.jsonl`.
11. Validate the dataset and confirm 150 valid samples.
12. If GPU is available, run LoRA smoke training with `configs/lora_smoke_config.json`.
13. Record logs, adapter path, ZIP path, and active adapter status if training completes.
14. Capture screenshots listed in `docs/evidence/SCREENSHOT_EVIDENCE_REPORT.md`.

## Errors Found

No new Colab-specific runtime errors were observed because Colab execution was not performed from this environment.

## Fixes Applied

- Created final evidence folder.
- Added explicit user-side Colab verification steps.
- Kept the notebook evidence language honest and reproducible.

## Final Status

Prepared for user-side Colab verification. Actual Colab runtime evidence still requires a manual Colab run.
