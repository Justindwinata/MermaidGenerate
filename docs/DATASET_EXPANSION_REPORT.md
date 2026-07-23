# Dataset Expansion Report

Report date: 2026-07-23 Asia/Jakarta

## Objective

MG-0007 expands MermaidGenerate beyond the original 150 curated examples so the final project has stronger prompt coverage for Mind Map and Venn Diagram generation while preserving all assignment requirements.

The expanded data is designed for local/Colab LoRA experimentation. It is not generated to fake model quality. Training results still depend on model capacity, GPU availability, epochs, and runtime duration.

## Dataset Targets

| Dataset | Target Size | Purpose |
|---|---:|---|
| `datasets/curated/mixed_mindmap_venn_curated.jsonl` | 150 | Fast smoke demo and quick Colab validation. |
| `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl` | 500 | Medium balanced LoRA training dataset. |
| `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl` | 1000 | Larger final balanced training dataset. |
| `datasets/evaluation/final_eval_prompts_100.jsonl` | 100 | Final manual/validator/model evaluation prompts. |

The expanded training target is balanced:

- 500 Mind Map examples
- 500 Venn examples

## Quality Strategy

The expanded dataset is generated deterministically from structured templates rather than hand-written repetition. The generator uses:

- fixed seed;
- domain templates;
- language-specific prompt templates;
- simple, medium, and complex prompt styles;
- two-set and three-set Venn formats;
- Mind Map outputs with varied branch counts and hierarchy depth;
- validation through project Mermaid syntax validators;
- duplicate checks for prompt/target pairs.

## Covered Domains

Mind Map coverage includes:

- student learning
- software engineering
- AI and machine learning
- data science
- digital marketing
- UMKM/business
- cybersecurity
- cloud and DevOps
- productivity
- research paper planning
- presentation planning
- final project planning

Venn coverage includes:

- social media platforms
- programming languages
- cloud platforms
- databases
- AI models
- software development methods
- learning methods
- business strategies
- student skills
- presentation topics
- UMKM marketing channels

## Syntax Standards

Mind Map completions start with:

```text
mindmap
```

Venn completions use assignment-facing syntax:

```text
venn
  set A["..."]
  set B["..."]
  union A,B
    text "..."
```

The preview renderer converts `venn` to Mermaid `venn-beta` internally.

## Validation Criteria

Expanded datasets must satisfy:

- JSONL parse success;
- no invalid Mermaid completions;
- no markdown fences in completions;
- no duplicate prompt/target pairs;
- no undefined Venn union references;
- Mind Map root exists;
- approximately balanced diagram types;
- summary reports generated under `results/dataset_quality/`.

## Recommended Use

- Quick classroom demo: use the 150-row curated mixed dataset.
- Balanced LoRA demo: use the 500-row expanded mixed dataset.
- Better coverage experiment: use the 1000-row expanded mixed dataset if Colab time allows.
