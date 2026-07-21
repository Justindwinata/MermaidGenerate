# Screenshot Capture Plan

Status date: 2026-07-22 Asia/Jakarta

## Status

Screenshots were **not captured** during MG-0002 local execution.

## Reason

The requested evidence should represent the real demo environment. Local execution did not include Colab GPU training, trained adapter output, or browser-based training logs from a real run. Creating screenshots without those real states would be misleading.

## Capture Checklist

Capture these only after running the notebook/UI in Colab or the intended demo environment:

1. `01_colab_notebook_overview.png`: notebook open in Colab.
2. `02_generator_tab_mindmap.png`: Generator tab with a valid Mind Map output.
3. `03_generator_tab_venn.png`: Generator tab with a valid Venn output.
4. `04_dataset_upload_validation.png`: curated dataset uploaded and validated.
5. `05_training_controls.png`: LoRA smoke config entered.
6. `06_training_logs.png`: real training progress/loss logs.
7. `07_adapter_download.png`: real adapter ZIP download visible.
8. `08_rendered_mermaid_preview.png`: rendered Mermaid preview.

## Rules

- Do not add screenshots unless they are captured from a real run.
- Do not edit screenshots to imply success that did not happen.
- If training fails, capture the failure state and document the exact error.
