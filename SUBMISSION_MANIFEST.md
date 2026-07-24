# MermaidGenerate Submission Manifest

Generated for: final assignment packaging.

Repository URL: `https://github.com/Justindwinata/MermaidGenerate`

The packaging script generates a timestamped copy of this manifest inside `dist/MermaidGenerate_Final_Submission/` with file sizes and the current Git commit hash.

## Lecturer Requirement Mapping

| Requirement | Included file(s) | Purpose | Status |
|---|---|---|---|
| Notebook with inference/upload dataset/training | `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` | Main Google Colab notebook containing setup, inference, dataset validation, Gradio UI, and fine-tuning workflow. | Included |
| Dataset | `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl` | Final expanded dataset with 1000 balanced examples. | Included |
| Demo-friendly dataset | `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl` | Faster dataset for practical demo training. | Included |
| Smoke-test dataset | `datasets/curated/mixed_mindmap_venn_curated.jsonl` | Small validated dataset for quick LoRA smoke runs. | Included |
| Evaluation prompts | `datasets/evaluation/final_eval_prompts_100.jsonl` | Prompt-only final evaluation set. | Included |
| Video demonstration | `docs/VIDEO_DEMO_SCRIPT_DETAILED.md`, `docs/VIDEO_DEMO_CHECKLIST.md`, narration docs | Complete guide for recording the required video. | Included |
| Source code | `app.py`, `src/mermaid_generate/`, `scripts/`, `configs/` | Web app, inference, validation, training, dataset generation, evaluation, and packaging code. | Included |
| Documentation | `README.md`, `docs/*.md`, evidence summary, QA audit | Explains architecture, dataset, training, evaluation, local/Colab usage, and limitations. | Included |
| Reports | `results/dataset_quality/expanded_dataset_summary.*`, `results/evaluation/final_eval_baseline.json` | Dataset validation and validator-only evaluation evidence. | Included |

## Required Files in Final ZIP

- `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`
- `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`
- `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`
- `datasets/curated/mixed_mindmap_venn_curated.jsonl`
- `datasets/evaluation/final_eval_prompts_100.jsonl`
- `docs/VIDEO_DEMO_SCRIPT_DETAILED.md`
- `docs/VIDEO_DEMO_CHECKLIST.md`
- `docs/VIDEO_DEMO_NARRATION_SHORT.md`
- `docs/VIDEO_DEMO_NARRATION_FULL.md`
- `app.py`
- `requirements.txt`
- `src/mermaid_generate/`
- `scripts/`
- `configs/`
- important documentation and reports

## Files Excluded From ZIP

- `.git/`
- virtual environments
- `__pycache__/`
- `.pytest_cache/`
- notebook checkpoints
- model weights and checkpoints
- adapter folders
- generated adapter ZIP files
- `.safetensors`, `.bin`, `.pt`, `.pth`, `.gguf`

## Submission Note

The generated final ZIP is a local artifact under:

```text
dist/MermaidGenerate_Final_Submission.zip
```

If the ZIP is not committed, regenerate it with:

```bash
python3 scripts/build_submission_package.py
python3 scripts/verify_submission_package.py
```
