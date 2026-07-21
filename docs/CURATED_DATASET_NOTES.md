# Curated Dataset Notes

Validation date target: generated for MG-0002 on 2026-07-22.

## Files

- `datasets/curated/mindmap_curated.jsonl`: 75 Mind Map examples.
- `datasets/curated/venn_curated.jsonl`: 75 Venn examples.
- `datasets/curated/mixed_mindmap_venn_curated.jsonl`: 150 balanced examples.

## Coverage

The curated dataset expands the starter examples with Indonesian and English prompts across education, business/UMKM, technology, health/general, and social science topics.

Mind Map examples focus on hierarchical topics such as digital marketing, small business planning, machine learning workflow, environmental awareness, healthy lifestyle, project management, education planning, customer service, finance tracking, and content strategy.

Venn examples focus on realistic comparisons such as students/employees/entrepreneurs, AI/machine learning/data science, online marketing channels, healthy habits, learning styles, business roles, software development concepts, school subjects, social media/public transport style comparisons, and social science comparisons.

## Format

The files use prompt-completion JSONL because it is simple for supervised fine-tuning and already supported by the project validator.

Each row includes:

- `prompt`
- `completion`
- `language`
- `domain`
- `complexity`

## Constraints

- Every target starts with `mindmap` or `venn`.
- No markdown code fences are used.
- Prompt-target pairs are generated to avoid exact duplicates.
- The dataset is larger than the starter examples but still needs human review before serious model-quality claims.
