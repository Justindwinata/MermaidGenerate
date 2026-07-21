# Dataset Specification

## Supported Formats

### Messages

```json
{"messages":[{"role":"user","content":"Create a mind map."},{"role":"assistant","content":"mindmap\n  root((Topic))"}]}
```

### Prompt Completion

```json
{"prompt":"Create a Venn diagram.","completion":"venn\n  set A[\"A\"]\n  set B[\"B\"]\n  union A,B[\"AB\"]"}
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
