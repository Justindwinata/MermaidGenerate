# Screenshot Evidence Report

Report date: 2026-07-22 Asia/Jakarta

## Capture Status

Real local Gradio screenshots were captured from `http://127.0.0.1:7903/`.

## Captured Screenshots

- `docs/evidence/screenshots/02_gradio_generator_empty.png`
  - Real screenshot of the **Generator Mermaid** tab in unloaded/empty state.
- `docs/evidence/screenshots/05_dataset_upload_tab.png`
  - Real screenshot of the **Dataset & Fine-Tuning** tab before validation.
- `docs/evidence/screenshots/06_dataset_validation_result.png`
  - Real screenshot after uploading and validating `datasets/curated/mixed_mindmap_venn_curated.jsonl`.
- `docs/evidence/screenshots/07_training_controls.png`
  - Real screenshot of visible LoRA/QLoRA/Full Fine-Tuning controls.
- `docs/evidence/screenshots/08_training_logs_or_ready_state.png`
  - Real screenshot of the ready/validated training state. It does not show real training logs because training was not executed.
- `docs/evidence/screenshots/10_final_demo_overview.png`
  - Real screenshot of the final local UI overview after dataset validation.
- `docs/evidence/screenshots/fix/01_mindmap_render_success.png`
  - Real local render-fix screenshot using final valid Mind Map code.
- `docs/evidence/screenshots/fix/02_venn_render_success.png`
  - Real local render-fix screenshot using final valid Venn code with renderer conversion.
- `docs/evidence/screenshots/fix/03_validation_success.png`
  - Real local screenshot showing valid final code and rendered previews.
- `docs/evidence/screenshots/fix/05_iframe_preview_render_success.png`
  - Real local browser screenshot showing the iframe-based preview rendering visible Mind Map and Venn SVG diagrams with the same `build_mermaid_preview_html` helper used by Gradio.

## Screenshots Not Captured

The following were not captured because they require a real Colab/model/training run:

- `01_notebook_overview.png`
  - Requires opening the notebook in Colab or a browser notebook viewer.
- `09_adapter_download_state.png`
  - Requires successful real LoRA/QLoRA training and adapter ZIP generation.

## Notes

- No fake screenshots were created.
- The captured screenshots prove the local Gradio app launches, tabs render, curated dataset upload works, dataset validation works, training controls are visible, and the patched iframe renderer can produce visible Mind Map and Venn SVG diagrams.
- They do not prove Colab GPU execution, successful LoRA training, adapter ZIP creation, or before/after model improvement.

## Manual Screenshot Checklist

During the final Colab demo, capture:

1. Notebook overview in Colab.
2. Mind Map generation result.
3. Venn generation result.
4. Real training progress/loss logs.
5. Adapter ZIP download state after successful training.
6. Before/after generation comparison if adapter training succeeds.
