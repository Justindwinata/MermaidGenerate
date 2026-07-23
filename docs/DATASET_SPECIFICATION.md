# Dataset Specification

## Supported Formats

### Messages

```json
{"messages":[{"role":"user","content":"Create a mind map."},{"role":"assistant","content":"mindmap\n  root((Topic))"}]}
```

### Prompt Completion

```json
{"prompt":"Create a Venn diagram.","completion":"venn\n  set A[\"A\"]\n  set B[\"B\"]\n  union A,B\n    text \"AB\""}
```

### Instruction Output

```json
{"instruction":"Create a Mermaid mind map.","input":"Topic: UMKM","output":"mindmap\n  root((UMKM))"}
```

## Internal Schema

Every valid sample is normalized to:

```json
{
  "id": "...",
  "diagram_type": "mindmap|venn",
  "prompt": "...",
  "target": "...",
  "source_format": "messages|prompt_completion|instruction_output",
  "language": "id|en|unknown",
  "domain": "...",
  "complexity": "simple|medium|complex"
}
```

## Validation Checks

The validator checks file format, required fields, empty prompt/target, target prefix, markdown fences, type mismatch, target length, duplicates, distributions, invalid rows, and train readiness.

The final curated mixed dataset is:

```text
datasets/curated/mixed_mindmap_venn_curated.jsonl
```

Expected distribution:

- 75 Mind Map samples
- 75 Venn samples
- 150 total valid samples
- 0 duplicates

Training should not start if validation reports zero valid samples or unresolved invalid rows.

## Expanded Datasets

MG-0007 adds larger deterministic training datasets:

| File | Rows | Purpose |
|---|---:|---|
| `datasets/expanded/mindmap_expanded.jsonl` | 500 | Mind Map-only training coverage. |
| `datasets/expanded/venn_expanded.jsonl` | 500 | Venn-only training coverage. |
| `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl` | 500 | Medium balanced LoRA dataset. |
| `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl` | 1000 | Larger balanced LoRA dataset. |
| `datasets/evaluation/final_eval_prompts_100.jsonl` | 100 | Prompt-only final evaluation set. |

Validation artifacts:

- `scripts/validate_expanded_dataset.py`
- `scripts/summarize_dataset_quality.py`
- `results/dataset_quality/expanded_dataset_summary.json`
- `results/dataset_quality/expanded_dataset_summary.md`

Final expanded validation status:

- invalid completions: `0`
- warning rows: `0`
- duplicate prompts: `0`
- duplicate completions: `0`
- Venn undefined union references: `0`
- Mind Map missing root count: `0`
- mixed 500 distribution: 250 Mind Map / 250 Venn
- mixed 1000 distribution: 500 Mind Map / 500 Venn

## Venn Syntax Alignment

Assignment-facing Venn targets start with `venn`, but must use renderer-safe union text blocks:

```mermaid
venn
  set A["Instagram"]
  set B["TikTok"]
  set C["WhatsApp"]
  union A,B
    text "Audience Engagement"
  union A,C
    text "Customer Communication"
  union B,C
    text "Short Content Sharing"
  union A,B,C
    text "Digital Marketing"
```

The preview renderer converts the first line to `venn-beta` internally.
