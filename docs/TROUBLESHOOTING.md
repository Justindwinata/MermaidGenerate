# Troubleshooting

Use this guide when the local app, Colab app, Mermaid preview, or training workflow does not behave as expected.

## Do Not Open `0.0.0.0:7860` in a Browser

`0.0.0.0` is a server bind address. It tells the server to listen on available network interfaces. It is not a browser URL.

Use these browser URLs instead:

- Local laptop: `http://127.0.0.1:7860`
- Colab: the generated `https://xxxxx.gradio.live` URL

## When to Use `127.0.0.1`

Use `127.0.0.1` only when the app is running on the same machine as your browser.

Example:

```bash
python app.py --local
```

Open:

```text
http://127.0.0.1:7860
```

If port `7860` is busy:

```bash
python app.py --local --port 7861
```

Open:

```text
http://127.0.0.1:7861
```

## When to Use `gradio.live`

Use the Gradio public share link when the app runs inside Google Colab:

```text
https://xxxxx.gradio.live
```

Colab runs on a remote machine, so your laptop browser cannot open Colab's `127.0.0.1`.

## Mermaid Preview Shows Text Instead of Diagram

Likely causes:

- old code is running;
- runtime did not restart after pulling updates;
- browser cached an older Gradio session;
- invalid raw model output bypassed the fixed runtime.

Fix:

1. Pull the latest repository.
2. Restart the Colab runtime or local Python process.
3. Relaunch Gradio.
4. Generate again and check the **Final valid Mermaid code** box.
5. Confirm the preview panel shows an iframe-rendered SVG diagram.

The fixed renderer uses iframe `srcdoc` and Mermaid.js. Venn assignment code starts with `venn`, but the preview renderer internally converts it to `venn-beta`.

## Model Output Is Invalid

Short LoRA smoke training can still produce imperfect raw text. This is expected.

Use the main output:

- **Final valid Mermaid code**
- **Mermaid validation and repair status**
- **Rendered Mermaid preview**

The raw model output is only for debugging and should not be treated as the final answer.

## CUDA Is Unavailable

If Colab reports no CUDA GPU:

1. Go to **Runtime > Change runtime type**.
2. Select **GPU**.
3. Restart and rerun cells.

CPU can validate datasets, but LoRA/QLoRA/Full Fine-Tuning will be slow or impractical.

## QLoRA Fails Because bitsandbytes/CUDA Is Unavailable

QLoRA requires a compatible CUDA and bitsandbytes environment.

Fix:

- switch to LoRA;
- reduce max sequence length;
- restart runtime after dependency install;
- use a Colab GPU runtime with compatible CUDA.

## Full Fine-Tuning Causes OOM

Full Fine-Tuning updates all model weights and can exceed Colab GPU memory.

Fix:

- use LoRA for demo;
- use QLoRA if bitsandbytes/CUDA works;
- reduce batch size to `1`;
- reduce max sequence length to `512`;
- use gradient accumulation instead of larger batch size.

## Adapter ZIP Does Not Appear

Check:

1. Dataset validation has at least one valid sample.
2. Training status is `completed`.
3. You clicked **Refresh Status** after completion.
4. Mode is LoRA or QLoRA for adapter ZIP output.
5. The result summary contains a ZIP path under `outputs/adapters/`.

Full Fine-Tuning saves a full model path instead of a LoRA/QLoRA adapter ZIP.

## Dataset Validation Fails

Common causes:

- target does not start with `mindmap` or `venn`;
- target contains markdown fences;
- Venn union references undefined sets;
- Venn union uses bracket labels instead of indented `text "..."`;
- prompt or target is empty;
- duplicate prompt/target pairs exist.

Use `datasets/curated/mixed_mindmap_venn_curated.jsonl` for the final demo baseline.

## Local Dependencies Fail to Install

Use a clean virtual environment, then run:

```bash
pip install -r requirements.txt
```

On macOS, bitsandbytes is skipped by the requirement marker. QLoRA should be demonstrated in a compatible CUDA environment such as Colab.
