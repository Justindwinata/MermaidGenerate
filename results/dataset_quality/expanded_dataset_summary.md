# Expanded Dataset Quality Summary

Generated on: 2026-07-23
Overall status: PASS

## Dataset Results

| File | Total | Mind Map | Venn | Invalid | Warnings | Prompt Dupes | Completion Dupes | Balanced |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| datasets/expanded/mindmap_expanded.jsonl | 500 | 500 | 0 | 0 | 0 | 0 | 0 | False |
| datasets/expanded/venn_expanded.jsonl | 500 | 0 | 500 | 0 | 0 | 0 | 0 | False |
| datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl | 500 | 250 | 250 | 0 | 0 | 0 | 0 | True |
| datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl | 1000 | 500 | 500 | 0 | 0 | 0 | 0 | True |

## Recommended Use

- Quick Colab smoke test: `datasets/curated/mixed_mindmap_venn_curated.jsonl`.
- Medium LoRA training: `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`.
- Larger LoRA training: `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`.

The expanded datasets are deterministic and validated against the project Mermaid validator. The mixed datasets are balanced 50/50, while the mindmap-only and Venn-only files are intentionally single-diagram-type datasets. They improve coverage, but final model quality still depends on GPU resources, training time, and model capacity.
