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
