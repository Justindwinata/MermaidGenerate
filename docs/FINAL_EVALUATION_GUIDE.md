# Final Evaluation Guide

MermaidGenerate uses two evaluation paths so the report stays honest.

## Validator-Only Evaluation

Run this on any local machine:

```bash
python scripts/run_final_quality_evaluation.py --validator-only
```

This mode validates the expanded dataset completions and checks the final 100 prompt evaluation set. It does not download a model and does not claim model quality.

Output:

- `results/evaluation/final_eval_baseline.json`

Expected result:

- 1,000 reference completions in the expanded mixed dataset
- 100 final evaluation prompts
- 50 Mind Map prompts
- 50 Venn prompts
- 0 invalid Mermaid completions
- 0 duplicate evaluation prompts

## Optional Model Evaluation

Run this in Google Colab or another GPU runtime:

```bash
python scripts/run_final_quality_evaluation.py --model --max-samples 20
```

This mode loads the Transformers/PyTorch model, generates Mermaid code, applies the extraction and repair pipeline, and records real syntax validity and fallback usage.

Do not report model-mode metrics unless the command actually completed.

## Interpretation

Validator-only results prove syntax safety and dataset quality. Model-mode results measure actual generation behavior. Small LoRA runs can improve format following, but fallback repair remains the runtime guard that ensures final Mermaid code is valid.
