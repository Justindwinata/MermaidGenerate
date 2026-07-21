# MermaidGenerate

MermaidGenerate is a Google Colab-first local AI project for generating Mermaid Mind Map and Venn Diagram code with a Transformers/PyTorch language model.

Primary deliverable:

`MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`

The notebook and helper modules provide:

- Mind Map and Venn Diagram Mermaid generation.
- Dataset upload and validation for JSON/JSONL datasets.
- LoRA, QLoRA 4-bit, and full fine-tuning paths using Transformers, PyTorch, PEFT, and Datasets.
- Gradio web UI with generator and dataset/fine-tuning tabs.
- Adapter activation and ZIP download for LoRA/QLoRA output.

Default model:

`TinyLlama/TinyLlama-1.1B-Chat-v1.0`

The project intentionally uses Transformers and PyTorch as the primary runtime. llama.cpp/GGUF support is documented only as future optional compatibility unless implemented later.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

In Google Colab, open and run `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` from top to bottom.

## Example Datasets

Starter datasets are included:

- `datasets/examples/mindmap_examples.jsonl`
- `datasets/examples/venn_examples.jsonl`

They are intentionally small and useful for validation demos only. Real fine-tuning needs a larger, higher-quality dataset.

## Documentation

- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/DATASET_SPECIFICATION.md`
- `docs/TRAINING_GUIDE.md`
- `docs/NOTEBOOK_GUIDE.md`
- `docs/EVALUATION_PLAN.md`
- `docs/REFERENCE_NOTEBOOK_INSPECTION.md`
- `docs/DECISION_LOG.md`
