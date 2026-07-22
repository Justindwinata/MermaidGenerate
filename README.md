# MermaidGenerate

MermaidGenerate is a local-first and Google Colab-compatible AI project for generating Mermaid **Mind Map** and **Venn Diagram** code with a Hugging Face **Transformers + PyTorch** language model.

Primary deliverable:

`MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`

Default model:

`TinyLlama/TinyLlama-1.1B-Chat-v1.0`

## Assignment Requirement Checklist

- Google Colab-compatible notebook exists.
- Mermaid inference uses Transformers and PyTorch.
- Browser UI uses Gradio Blocks.
- UI tab **Generator Mermaid** exists.
- UI tab **Dataset & Fine-Tuning** exists.
- Dataset upload and validation support JSON/JSONL.
- Accepted dataset formats: `messages`, `prompt`/`completion`, and `instruction`/`output` with optional `input`.
- Fine-tuning modes exist: LoRA, QLoRA 4-bit, and Full Fine-Tuning.
- Training is launched from the browser UI.
- Training status, progress, loss logs, cancellation, and result display are wired.
- LoRA/QLoRA adapters can be saved and zipped for download.
- Trained adapter/model activation path exists.
- Evaluation utilities and manual prompts are included.

## Supported Diagrams

The final project targets only:

- Mind Map: output starts with `mindmap`.
- Venn Diagram: output starts with `venn`.

Flowchart generation is not the final target. The original flowchart reference notebook was used only for implementation inspection.

## Runtime Decision

The project intentionally uses Transformers, PyTorch, and PEFT because the assignment requires this runtime. llama.cpp/GGUF is documented only as future optional compatibility and is not the primary inference or training path.

No paid API is used.

## Open in Colab

1. Open `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` in Google Colab.
2. Select **Runtime > Change runtime type > GPU** for model loading and training.
3. Run cells from top to bottom.
4. Use the GPU check cell to confirm CUDA availability.
5. Launch the Gradio app cell with `share=True`.
6. Open the generated Gradio public link.

Colab usually needs a Gradio public link because Colab localhost is not directly accessible from your laptop browser.

## Run Locally

```bash
pip install -r requirements.txt
python app.py --local
```

Then open:

```text
http://127.0.0.1:7860
```

Local laptop mode does not require Gradio Live. Optional modes:

```bash
python app.py --local --port 7861
python app.py --share
python app.py --colab
```

## Dataset Files

Starter examples:

- `datasets/examples/mindmap_examples.jsonl`
- `datasets/examples/venn_examples.jsonl`

Curated datasets for MG-0002:

- `datasets/curated/mindmap_curated.jsonl`
- `datasets/curated/venn_curated.jsonl`
- `datasets/curated/mixed_mindmap_venn_curated.jsonl`

Manual evaluation prompts:

- `datasets/evaluation/manual_eval_prompts.jsonl`

## Upload and Validate Dataset

In the Gradio UI, open **Dataset & Fine-Tuning**, upload a JSON or JSONL file, then click **Validate Dataset**. The report shows total samples, valid samples, invalid samples, warning count, duplicate count, diagram distribution, source format distribution, and invalid row preview.

Training is blocked if there are zero valid samples.

## Fine-Tuning

Recommended smoke demo:

- Dataset: `datasets/curated/mixed_mindmap_venn_curated.jsonl`
- Config: `configs/lora_smoke_config.json`
- Mode: LoRA
- Epochs: 1
- Batch size: 1
- Gradient accumulation: 4
- Max sequence length: 512
- Learning rate: `2e-4`
- Validation split: `0.1`

Use QLoRA only when CUDA and bitsandbytes are compatible. Use Full Fine-Tuning only when GPU memory is sufficient.

## Download Adapter

After successful LoRA/QLoRA training, the backend saves the adapter under `outputs/adapters/<timestamp>/` and creates a ZIP file. The UI exposes the ZIP through the download component.

`outputs/` is gitignored except `outputs/.gitkeep`.

## Evaluation

Run validator-only evaluation locally:

```bash
python scripts/run_manual_evaluation.py --mode validator-only --write-docs-report
```

Run actual model inference evaluation in Colab/GPU:

```bash
python scripts/run_manual_evaluation.py --mode model --max-samples 20
```

Baseline notes are documented in `docs/EVALUATION_BASELINE_REPORT.md`.

## Demo Evidence

Screenshots were not faked. MG-0003 captured real local Gradio screenshots under `docs/evidence/screenshots/` for:

- generator empty state
- dataset upload tab
- dataset validation result
- training controls
- ready state/final overview

Screenshots for real generation results, training logs, and adapter download still require a Colab/model/training run.

Evidence docs:

- `docs/evidence/COLAB_RUNTIME_REPORT.md`
- `docs/evidence/SCREENSHOT_EVIDENCE_REPORT.md`
- `docs/evidence/LORA_SMOKE_TRAINING_EVIDENCE.md`
- `docs/evidence/BEFORE_AFTER_LORA_EVALUATION.md`

Final demo materials:

- `docs/FINAL_DEMO_SCRIPT.md`
- `docs/FINAL_SUBMISSION_CHECKLIST.md`

## MG-0004 Render Fix

Manual Colab testing showed LoRA training completed and an adapter ZIP was generated, but raw generation still produced invalid Mermaid. The fix adds:

- strict diagram-specific prompt templates
- robust first-diagram extraction
- Venn repair/compiler fallback
- Mind Map repair/compiler fallback
- stricter Venn syntax validation
- renderer conversion from assignment-facing `venn` to Mermaid `venn-beta`
- UI display of final valid code instead of invalid raw output

Evidence:

- `docs/evidence/GENERATION_FAILURE_ANALYSIS.md`
- `docs/evidence/GENERATOR_RUNTIME_EVIDENCE.md`
- `docs/evidence/FINAL_EVIDENCE_SUMMARY.md`
- `docs/evidence/screenshots/fix/`

Latest render fix evidence:

- `docs/evidence/screenshots/fix/05_iframe_preview_render_success.png` shows both Mind Map and Venn diagrams rendered through the iframe-based Mermaid preview. This fixes the manual retest issue where valid Mermaid code appeared but no SVG diagram was visible in Gradio.

## Limitations

- Colab GPU smoke training was not executed locally during MG-0002 because CUDA is unavailable in the local environment.
- Model quality depends on dataset size and training quality.
- Curated datasets are larger than starter examples but still need human review.
- Full Fine-Tuning may fail on limited GPU memory.
- QLoRA requires compatible CUDA and bitsandbytes.
- Venn rendering depends on Mermaid.js Venn support; preview uses Mermaid `venn-beta` internally.
- llama.cpp/GGUF remains optional future compatibility unless implemented later.

## Documentation

- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/DATASET_SPECIFICATION.md`
- `docs/TRAINING_GUIDE.md`
- `docs/NOTEBOOK_GUIDE.md`
- `docs/EVALUATION_PLAN.md`
- `docs/CURATED_DATASET_NOTES.md`
- `docs/CURATED_DATASET_VALIDATION_REPORT.md`
- `docs/EVALUATION_BASELINE_REPORT.md`
- `docs/LORA_SMOKE_TEST_PLAN.md`
- `docs/LORA_SMOKE_TEST_RESULT.md`
- `docs/LOCAL_RUN_GUIDE.md`
- `docs/LOCAL_UI_REVISION_PLAN.md`
- `docs/SCREENSHOT_CAPTURE_PLAN.md`
- `docs/SUBMISSION_GUIDE.md`
- `docs/FINAL_DEMO_SCRIPT.md`
- `docs/FINAL_SUBMISSION_CHECKLIST.md`
- `docs/evidence/`
- `docs/REFERENCE_NOTEBOOK_INSPECTION.md`
- `docs/DECISION_LOG.md`
