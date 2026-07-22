# Local UI Revision Evidence

Evidence date: 2026-07-23 Asia/Jakarta

## Scope

MG-0005 revised MermaidGenerate into a local-first Gradio web app with a navy, orange, and black/dark UI theme while preserving the existing Transformers/PyTorch/PEFT runtime and all core assignment functions.

## Local Launch Smoke Test

Command:

```bash
python3 app.py --local --port 7860
```

Observed startup banner:

```text
MermaidGenerate starting...
Mode: local
Host: 127.0.0.1
Port: 7860
Local URL: http://127.0.0.1:7860
Gradio share/public link: disabled
Use --share or --colab for a public Gradio link.
```

HTTP check:

```bash
curl -I http://127.0.0.1:7860
```

Result:

```text
HTTP/1.1 200 OK
server: uvicorn
content-type: text/html; charset=utf-8
```

Interpretation: local-first launch works at `http://127.0.0.1:7860` when the server process is allowed to bind localhost.

## Colab/Share Mode

CLI options now support:

```bash
python app.py --share
python app.py --colab
```

The notebook launch cell still uses `share=True`, which is appropriate for Google Colab because Colab localhost is not directly accessible from the user's laptop browser.

## UI Theme Evidence

The Gradio app now uses a dark navy/black base with orange primary actions, subtle slate cards, readable code blocks, and a prominent iframe Mermaid preview panel.

The UI still keeps:

- **Generator Mermaid**
- **Dataset & Fine-Tuning**

## Preserved Functions

The following were preserved:

- dataset upload
- dataset validation
- curated dataset compatibility
- Mermaid validation
- Mind Map repair fallback
- Venn repair fallback
- iframe Mermaid preview renderer
- Transformers/PyTorch inference
- LoRA, QLoRA 4-bit, and Full Fine-Tuning controls
- training status/log/result callbacks
- cancellation
- adapter activation
- adapter ZIP download
- Colab notebook flow

## Notes

No paid API is used. llama.cpp/GGUF remains future optional compatibility only. Model quality still depends on dataset quality and training duration, and the runtime repair layer may be used to guarantee valid Mermaid syntax.
