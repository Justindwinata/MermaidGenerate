# Before/After LoRA Evaluation Evidence

Report date: 2026-07-22 Asia/Jakarta

## Execution Status

Before/after LoRA evaluation was **not executed**.

## Reason

Real LoRA smoke training was not executed in this local environment because CUDA is unavailable. Therefore there is no trained adapter to compare against the base model.

## Evaluation Dataset

- Prompt file: `datasets/evaluation/manual_eval_prompts.jsonl`
- Total prompts: 20
- Mind Map prompts: 10
- Venn prompts: 10
- Language mix: Indonesian and English

## Metrics Availability

| Metric | Base Model | LoRA Adapter |
| --- | --- | --- |
| Syntax validity rate | Not run | Not available |
| Diagram type accuracy | Not run | Not available |
| Prefix accuracy | Not run | Not available |
| Markdown fence violations | Not run | Not available |

## Validator-Only Baseline

The local validator-only baseline in `docs/EVALUATION_BASELINE_REPORT.md` confirms the reference targets are valid. It does **not** measure model quality.

## Planned Real Evaluation Procedure

After a successful Colab GPU LoRA smoke training run:

1. Run baseline model inference:
   ```bash
   python scripts/run_manual_evaluation.py --mode model --max-samples 20
   ```
2. Load the trained adapter in the notebook or app.
3. Run the same 20 prompts again through the active adapter.
4. Record:
   - base model outputs
   - trained adapter outputs
   - syntax validity before/after
   - diagram type accuracy before/after
   - markdown fence violations before/after
   - qualitative notes
5. Interpret results honestly. A one-epoch smoke LoRA run may prove the pipeline works without improving output quality.

## Honest Interpretation

No before/after improvement is claimed. The current project is prepared for real evaluation, but the final metrics require a real Colab GPU run and a completed adapter.
