# Dataset Usage Guide

Guide date: 2026-07-23 Asia/Jakarta

## Which Dataset Should I Use?

| Scenario | Recommended Dataset | Why |
|---|---|---|
| Quick Colab smoke test | `datasets/curated/mixed_mindmap_venn_curated.jsonl` | Small, fast, already balanced at 75 Mind Map and 75 Venn. |
| Balanced LoRA demo | `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl` | More coverage while still practical for short LoRA runs. |
| Larger final experiment | `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl` | Highest coverage, but takes longer to train. |
| Manual evaluation | `datasets/evaluation/final_eval_prompts_100.jsonl` | Prompt-only final evaluation set with 50 Mind Map and 50 Venn prompts. |

## Local Validation

Run:

```bash
python scripts/validate_expanded_dataset.py
python scripts/summarize_dataset_quality.py
```

Expected:

- invalid rows: `0`
- duplicate rows: `0`
- Venn undefined union references: `0`
- Mind Map malformed root: `0`

## Colab Training Recommendation

For a fast demo:

```text
Dataset: datasets/curated/mixed_mindmap_venn_curated.jsonl
Config: configs/lora_smoke_config.json
```

For a better LoRA demo:

```text
Dataset: datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl
Config: configs/lora_medium_dataset_config.json
```

For a longer run:

```text
Dataset: datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl
Config: configs/lora_expanded_dataset_config.json
```

## Demo Notes

- Always validate the dataset in the **Dataset & Fine-Tuning** tab before training.
- Start with LoRA unless the lecturer specifically asks for QLoRA or Full Fine-Tuning.
- QLoRA requires compatible CUDA/bitsandbytes.
- Full Fine-Tuning may exceed free Colab GPU memory.
- Adapter ZIP files are generated during training and should not be committed if large.

## Access Notes

Local laptop:

```bash
python app.py --local
```

Open:

```text
http://127.0.0.1:7860
```

Google Colab:

- run the notebook launch cell with `share=True`;
- open the generated `https://xxxxx.gradio.live` URL;
- do not open `0.0.0.0:7860` in the browser.
