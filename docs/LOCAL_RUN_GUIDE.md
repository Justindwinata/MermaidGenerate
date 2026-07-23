# Local Run Guide

Guide date: 2026-07-23 Asia/Jakarta

## Local Laptop Mode

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python app.py --local
```

Expected console output includes:

```text
MermaidGenerate starting...
Mode: local
Host: 127.0.0.1
Port: 7860
Local URL: http://127.0.0.1:7860
Gradio share/public link: disabled
```

Default local URL:

```text
http://127.0.0.1:7860
```

Local laptop mode does not require Gradio Live or a public share URL. The app runs on your machine and opens through localhost.

## Custom Local Port

```bash
python app.py --local --port 7861
```

Open:

```text
http://127.0.0.1:7861
```

## Colab or Public Demo Mode

Google Colab usually needs a public Gradio share link because Colab localhost is not directly accessible from the user's browser.

Use:

```bash
python app.py --colab
```

or:

```bash
python app.py --share
```

The notebook can also call the app launch function with `share=True`.

Open the generated `https://xxxxx.gradio.live` URL in your browser. Do not open `0.0.0.0:7860`; `0.0.0.0` is only a server bind address.

## Smoke Test Prompts

Mind Map:

```text
Buat mind map tentang strategi belajar AI untuk mahasiswa informatika.
```

Expected:

- final code starts with `mindmap`
- validation says valid
- rendered SVG preview appears

Venn:

```text
Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.
```

Expected:

- final code starts with `venn`
- renderer internally uses `venn-beta`
- validation says valid
- rendered SVG preview appears

## Limitations

- Local mode requires dependencies installed on the machine.
- Model loading may require enough RAM or VRAM.
- CPU inference can be slow.
- Model quality depends on dataset and training.
- Runtime repair may be used to guarantee valid Mermaid syntax.
- QLoRA requires compatible CUDA and bitsandbytes.
- llama.cpp/GGUF remains future optional compatibility.
- No paid API is used.

## More Troubleshooting

See `docs/TROUBLESHOOTING.md` for:

- `0.0.0.0` vs `127.0.0.1` vs `gradio.live`;
- Mermaid preview issues;
- CUDA/QLoRA/Full Fine-Tuning errors;
- missing adapter ZIP output.
