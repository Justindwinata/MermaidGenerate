# Evaluation Baseline Report

Validation date: 2026-07-22 Asia/Jakarta

- Mode: `validator-only`
- Model inference executed: `False`
- Output artifact: `/Users/justindwinata/Documents/MermaidGenerate/outputs/evaluation/manual_evaluation_validator-only.json`
- Metrics: `{'total': 20, 'syntax_validity_rate': 1.0, 'diagram_type_accuracy': 1.0, 'prefix_accuracy': 1.0, 'exact_match_rate': 1.0, 'invalid_output_count': 0, 'markdown_fence_violation_count': 0}`

## Notes

Reference targets were validated locally; model quality was not measured.

Local MG-0002 baseline ran validator-only because full model inference and before/after LoRA evaluation should be executed in Colab/GPU for honest timing and memory behavior.

Before/after LoRA results must be added only after a real LoRA smoke training run completes.
