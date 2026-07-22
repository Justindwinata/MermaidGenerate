# Final Evidence Summary

Summary date: 2026-07-22 Asia/Jakarta

## What Was Proven

- Dataset upload and validation were previously verified by user-side Colab testing.
- LoRA training completed in user-side Colab testing and adapter ZIP was generated.
- Initial post-training generation failed because raw model output was invalid.
- The fix adds strict prompts, robust diagram extraction, deterministic Venn and Mind Map compilers, stricter validation, and renderer alignment.
- Local smoke tests now produce valid Mind Map and Venn code through fallback repair.
- Render-fix screenshots exist under `docs/evidence/screenshots/fix/`.
- A follow-up local browser smoke test confirmed that the iframe-based preview renders visible Mind Map and Venn SVG diagrams.
- MG-0005 local-first launch smoke test returned `HTTP/1.1 200 OK` from `http://127.0.0.1:7860`.

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

LoRA smoke training can complete and still produce imperfect syntax. The repair fallback is the runtime guard that guarantees valid Mermaid syntax for demo rendering.
