# Notebook Guide

Open `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` in Google Colab.

Run the notebook in order:

1. Install dependencies.
2. Import libraries.
3. Review configuration.
4. Validate a dataset.
5. Load the model.
6. Test inference.
7. Launch Gradio.
8. Fine-tune only after valid dataset samples exist.
9. Download adapter ZIP outputs when training completes.

If the notebook is opened without repo files, it clones the GitHub repository automatically.

## Local Laptop Mode

For local laptop usage, the notebook is not required. Run:

```bash
python app.py --local
```

Then open:

```text
http://127.0.0.1:7860
```

Local mode does not require Gradio Live or a public share URL.

## Colab Mode

In Colab, use the notebook launch cell with `share=True` or run:

```bash
python app.py --colab
```

Colab usually needs a temporary public Gradio link because the Colab localhost server is not directly exposed to your laptop browser.

Do not open `0.0.0.0:7860` in your browser. Open the generated `gradio.live` link in Colab, or use `http://127.0.0.1:7860` only for local laptop mode.

For common runtime issues, see `docs/TROUBLESHOOTING.md`.
