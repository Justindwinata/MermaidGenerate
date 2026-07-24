# Final Submission Package

Use this guide when preparing the final academic submission for MermaidGenerate.

The lecturer requires three main items:

1. notebook with inference, dataset upload, and training/fine-tuning;
2. varied dataset;
3. video that demonstrates the application works.

MG-0008 prepares these requirements through the final ZIP package and video script docs.

## 0. Final ZIP Package

Generate the final package locally:

```bash
python3 scripts/build_submission_package.py
python3 scripts/verify_submission_package.py
```

Expected output:

```text
dist/MermaidGenerate_Final_Submission.zip
```

The ZIP includes notebook, datasets, source code, important docs, reports, manifest, and video demo scripts. It excludes large model checkpoints, adapters, caches, virtual environments, and generated training outputs.

## 1. Primary Notebook

Submit:

- `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`

This is the primary assignment deliverable. It contains setup, GPU check, dataset validation, inference, fine-tuning, Gradio launch, troubleshooting, limitations, and submission notes.

## 2. Dataset Files

Submit:

- `datasets/curated/mixed_mindmap_venn_curated.jsonl`

Optional supporting datasets:

- `datasets/curated/mindmap_curated.jsonl`
- `datasets/curated/venn_curated.jsonl`
- `datasets/examples/mindmap_examples.jsonl`
- `datasets/examples/venn_examples.jsonl`
- `datasets/expanded/mindmap_expanded.jsonl`
- `datasets/expanded/venn_expanded.jsonl`
- `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`
- `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`
- `datasets/evaluation/final_eval_prompts_100.jsonl`

The mixed curated dataset contains 150 validated samples: 75 Mind Map and 75 Venn.
The expanded mixed datasets contain 500 and 1000 validated examples for stronger LoRA experiments.

## 3. Source Code

Submit:

- `app.py`
- `src/mermaid_generate/`
- `requirements.txt`
- `configs/lora_smoke_config.json`
- `configs/lora_medium_dataset_config.json`
- `configs/lora_expanded_dataset_config.json`
- `scripts/`

These files preserve the local web app, dataset validation, Mermaid repair, preview rendering, Transformers/PyTorch inference, training manager, and adapter handling.

## 4. Documentation

Submit or reference:

- `README.md`
- `docs/DATASET_SPECIFICATION.md`
- `docs/TRAINING_GUIDE.md`
- `docs/LOCAL_RUN_GUIDE.md`
- `docs/NOTEBOOK_GUIDE.md`
- `docs/FINAL_DEMO_SCRIPT.md`
- `docs/FINAL_QA_AUDIT.md`
- `docs/FINAL_SUBMISSION_CHECKLIST.md`
- `docs/SUBMISSION_GUIDE.md`
- `docs/TROUBLESHOOTING.md` if present
- `docs/DATASET_EXPANSION_REPORT.md`
- `docs/DATASET_USAGE_GUIDE.md`
- `docs/FINAL_EVALUATION_GUIDE.md`

## 5. Evidence

Include evidence docs and screenshots if required:

- `docs/evidence/FINAL_EVIDENCE_SUMMARY.md`
- `docs/evidence/GENERATOR_RUNTIME_EVIDENCE.md`
- `docs/evidence/LOCAL_UI_REVISION_EVIDENCE.md`
- `docs/evidence/SCREENSHOT_EVIDENCE_REPORT.md`
- `docs/evidence/screenshots/`
- `results/dataset_quality/expanded_dataset_summary.json`
- `results/dataset_quality/expanded_dataset_summary.md`
- `results/evaluation/final_eval_baseline.json`

If a fresh Colab training demo is run, capture screenshots for:

- GPU runtime check
- Gradio Generator Mermaid tab
- Mind Map render result
- Venn render result
- dataset validation with 150 valid samples
- LoRA training logs/loss/progress
- completed adapter status
- adapter ZIP download

Do not create fake screenshots.

## 6. Adapter ZIP and Model Outputs

Adapter ZIP files may be generated during the demo, for example:

```text
outputs/adapters/lora-<timestamp>.zip
```

Do not commit large adapters, full model checkpoints, caches, or generated output folders unless the lecturer explicitly requests a small artifact. `outputs/` should remain gitignored except `outputs/.gitkeep`.

## 7. GitHub Repository Link

Submit or show:

```text
https://github.com/Justindwinata/MermaidGenerate
```

## 7A. Video Demo Materials

Use these files to record the lecturer video:

- `docs/VIDEO_DEMO_SCRIPT_DETAILED.md`
- `docs/VIDEO_DEMO_CHECKLIST.md`
- `docs/VIDEO_DEMO_NARRATION_SHORT.md`
- `docs/VIDEO_DEMO_NARRATION_FULL.md`
- `docs/NOTEBOOK_CELL_WALKTHROUGH.md`
- `docs/SOURCE_CODE_WALKTHROUGH.md`
- `docs/DATASET_VIDEO_EXPLANATION.md`

## 8. Final Demo Access Modes

Local laptop:

```bash
python app.py --local
```

Open:

```text
http://127.0.0.1:7860
```

Google Colab:

- run the notebook launch cell with `share=True`
- open the generated `https://xxxxx.gradio.live` URL
- do not open `0.0.0.0:7860` in your browser

## 9. Final Submission Reminder

The submitted project should clearly state:

- inference uses Transformers and PyTorch;
- fine-tuning uses PEFT LoRA/QLoRA/Full FT paths;
- no paid API is used;
- llama.cpp/GGUF is future optional compatibility only;
- model quality depends on dataset and training;
- fallback repair is used to guarantee valid Mermaid syntax for rendering.
