# Evaluation Plan

MermaidGenerate evaluates output quality with:

- Syntax validity rate.
- Diagram type accuracy.
- Prefix accuracy.
- Exact match after normalization.
- Invalid output count.
- Markdown fence violation count.

Training loss is useful but not sufficient. Always run a small manual test set after fine-tuning.
