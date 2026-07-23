# Final Evidence Summary

Summary date: 2026-07-23 Asia/Jakarta

## What Was Proven

- Notebook file exists: `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`.
- Web app exists: `app.py`.
- Source package exists: `src/mermaid_generate/`.
- Example datasets exist under `datasets/examples/`.
- Curated datasets exist under `datasets/curated/`, including `mixed_mindmap_venn_curated.jsonl`.
- Dataset upload and validation were previously verified by user-side Colab testing.
- LoRA training completed in user-side Colab testing and adapter ZIP was generated.
- Initial post-training generation failed because raw model output was invalid.
- The fix adds strict prompts, robust diagram extraction, deterministic Venn and Mind Map compilers, stricter validation, and renderer alignment.
- Local smoke tests now produce valid Mind Map and Venn code through fallback repair.
- Render-fix screenshots exist under `docs/evidence/screenshots/fix/`.
- A follow-up local browser smoke test confirmed that the iframe-based preview renders visible Mind Map and Venn SVG diagrams.
- MG-0005 local-first launch smoke test returned `HTTP/1.1 200 OK` from `http://127.0.0.1:7860`.
- MG-0007 expanded dataset validation passed with 500 Mind Map examples, 500 Venn examples, balanced 500/1000 mixed datasets, and 100 final evaluation prompts.

## Assignment Evidence Map

| Area | Status | Evidence/Notes |
|---|---:|---|
| Notebook exists | Verified | `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`. |
| `app.py` exists | Verified | Local-first Gradio app entrypoint. |
| Example datasets exist | Verified | `datasets/examples/mindmap_examples.jsonl`, `datasets/examples/venn_examples.jsonl`. |
| Curated mixed dataset exists | Verified | `datasets/curated/mixed_mindmap_venn_curated.jsonl`. |
| Expanded mixed datasets exist | Verified | `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`, `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`. |
| Expanded dataset quality report exists | Verified | `results/dataset_quality/expanded_dataset_summary.json` and `.md`. |
| Final validator-only evaluation exists | Verified | `results/evaluation/final_eval_baseline.json`; model inference was not executed in this validator-only report. |
| Generator tab evidence | Verified locally | Render-fix screenshots and code tests. |
| Dataset validation evidence | Verified by screenshots/user Colab | 150 valid, 0 invalid/warnings/duplicates reported in manual test. |
| Training evidence | Verified by user Colab screenshots | LoRA training completed with train/eval loss shown. |
| Adapter ZIP evidence | Verified by user Colab screenshots | Adapter ZIP path shown in UI; ZIP should not be committed if large. |
| Local mode evidence | Verified locally | `curl -I http://127.0.0.1:7860` returned `HTTP/1.1 200 OK`. |
| Colab/share mode evidence | Ready/partially user-verified | Notebook uses `share=True`; user previously tested a `gradio.live` URL. Capture fresh final screenshots during demo. |

## What Was Fixed

- Raw model output is no longer passed directly to the renderer.
- Venn unions now use defined set IDs only.
- Venn union labels now use indented `text "..."` lines.
- Assignment-facing `venn` is converted to renderer-facing `venn-beta` for preview.
- Mind Map fallback creates one root and safe hierarchy.
- UI main code box shows final valid Mermaid code.
- Raw model output is available only in the advanced debug section.
- Gradio preview no longer depends on direct dynamic `<script>` execution in the parent `gr.HTML`; it uses an iframe `srcdoc` document that loads Mermaid.js and renders SVG.
- Local launch now defaults to `python app.py --local` at `http://127.0.0.1:7860`, with optional `--share` and `--colab` modes.
- The Gradio UI now uses a navy/orange/black theme while keeping the existing two-tab workflow.

## Latest Render Evidence

`docs/evidence/screenshots/fix/05_iframe_preview_render_success.png` shows:

- rendered Mind Map diagram for the AI study strategy prompt;
- rendered Venn diagram for Instagram, TikTok, and WhatsApp marketing;
- Venn renderer conversion through `venn-beta`;
- final code and renderer-facing code details available below each preview.

## Local UI Revision Evidence

`docs/evidence/LOCAL_UI_REVISION_EVIDENCE.md` records:

- local launch command;
- local startup banner;
- `curl -I` response showing `HTTP/1.1 200 OK`;
- preserved feature checklist;
- local vs Colab/share mode behavior.

## Remaining Truth

LoRA smoke training can complete and still produce imperfect syntax. The repair fallback is the runtime guard that guarantees valid Mermaid syntax for demo rendering. Fresh final Colab screenshots should be captured during the actual submission demo if the lecturer requires current runtime proof.

The expanded dataset improves training coverage but does not prove model improvement by itself. Model-mode evaluation should be run in Colab/GPU only when real inference can be executed and recorded.
