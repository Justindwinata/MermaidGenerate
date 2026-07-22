# Generator Runtime Evidence

Evidence date: 2026-07-22 Asia/Jakarta

## Fix Smoke Test

The fixed runtime was smoke-tested without relying on perfect model output by invoking deterministic repair/compile fallback directly.

## Mind Map Prompt

Prompt:

`Buat mind map tentang strategi belajar AI untuk mahasiswa.`

Final valid code:

```mermaid
mindmap
  root((Strategi Belajar AI))
    Dasar AI
      Machine Learning
      Deep Learning
      Data
    Praktik
      Proyek Kecil
      Eksperimen Model
      Evaluasi
    Tools
      Python
      Notebook
      Library AI
    Portofolio
      Dokumentasi
      GitHub
      Presentasi
```

Validation: valid Mind Map Mermaid code.

## Venn Prompt

Prompt:

`Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.`

Final valid code:

```mermaid
venn
  set A["Instagram"]
  set B["TikTok"]
  set C["WhatsApp"]
  union A,B
    text "Audience Engagement"
  union A,C
    text "Customer Communication"
  union B,C
    text "Short Content Sharing"
  union A,B,C
    text "Digital Marketing"
```

Validation: valid Venn Mermaid code.

Renderer alignment: the preview converts the first line from `venn` to `venn-beta` internally.

## Screenshot Evidence

- `docs/evidence/screenshots/fix/01_mindmap_render_success.png`
- `docs/evidence/screenshots/fix/02_venn_render_success.png`
- `docs/evidence/screenshots/fix/03_validation_success.png`
- `docs/evidence/screenshots/fix/05_iframe_preview_render_success.png`

The latest iframe screenshot is from a local HTML preview page using the same project Mermaid preview renderer. It shows both a rendered Mind Map SVG and a rendered Venn SVG after the preview was changed from direct dynamic script injection to an isolated `<iframe srcdoc="...">` renderer.

## Interpretation

The fix does not claim that the LoRA model is perfect. It guarantees that invalid model output is extracted, repaired, or replaced by deterministic valid Mermaid before rendering.

## Follow-Up Render Fix

Manual Gradio retesting showed that final valid Mermaid code could still appear without a visible SVG diagram. The cause was Gradio/browser handling of script tags inserted dynamically through `gr.HTML`.

The preview now renders inside an iframe document:

- parent `gr.HTML` returns stable iframe markup;
- iframe `srcdoc` loads pinned Mermaid.js `11.13.0`;
- assignment-facing `venn` is rendered internally as `venn-beta`;
- render errors appear inside the iframe instead of silently failing;
- final code and renderer-facing code remain visible below the iframe.
