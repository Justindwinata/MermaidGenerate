# Final Demo Script

Use this script for a lecturer demo or video walkthrough.

## 1. Open Notebook in Google Colab

Open `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`.

Say: "This is the primary deliverable. The project is notebook-first and runs the local Transformers/PyTorch Mermaid generator."

## 2. Select GPU Runtime

Go to **Runtime > Change runtime type > GPU**.

Say: "GPU is needed for practical LoRA or QLoRA training. CPU can validate datasets but training will be slow."

## 3. Run Install Cells

Run dependency installation.

Say: "The notebook installs Transformers, PyTorch, Datasets, PEFT, bitsandbytes where compatible, and Gradio."

## 4. Check GPU

Run the GPU check cell.

Show:

- CUDA availability
- GPU name
- PyTorch version

## 5. Launch Gradio App

Run the Gradio app cell and open the public/local URL.

Say: "The app has two main tabs: Generator Mermaid and Dataset & Fine-Tuning."

## 6. Open Generator Mermaid Tab

Show the model/adaptor status and generation controls.

Say: "This generator uses Transformers and PyTorch. Venn preview uses Mermaid's `venn-beta` renderer internally, while copyable assignment code starts with `venn`."

## 7. Generate Mind Map

Prompt:

`Buat mind map tentang strategi belajar AI untuk mahasiswa informatika.`

Show:

- Mermaid code starts with `mindmap`
- validation result
- rendered preview

## 8. Generate Venn Diagram

Prompt:

`Create a Venn diagram comparing students, employees, and entrepreneurs.`

Show:

- Mermaid code starts with `venn`
- validation result
- rendered preview

## 9. Open Dataset & Fine-Tuning Tab

Show upload component and validation panel.

## 10. Upload Curated Dataset

Upload:

`datasets/curated/mixed_mindmap_venn_curated.jsonl`

## 11. Validate Dataset

Click **Validate Dataset**.

Show:

- Total: 150
- Valid: 150
- Invalid: 0
- Mind Map: 75
- Venn: 75

## 12. Select LoRA Mode

Use `configs/lora_smoke_config.json` values:

- Mode: LoRA
- Epochs: 1
- Batch size: 1
- Gradient accumulation: 4
- Max sequence length: 512
- Learning rate: `2e-4`
- Validation split: `0.1`

## 13. Run Smoke Training

Only start training if GPU is available.

Say: "Training progress is real. I will not claim success unless the job completes."

## 14. Show Progress, Logs, and Loss

Use **Refresh Status**.

Show:

- training status
- progress
- loss logs
- result summary

## 15. Show Active Adapter/Model Status

After successful training, show active adapter status changed from base/unloaded to adapter.

## 16. Download Adapter ZIP

Show the ZIP download component if LoRA/QLoRA completed.

Say: "The adapter ZIP is generated for download but not committed to Git because outputs are gitignored."

## 17. Generate After Training

Run one Mind Map and one Venn prompt again with the active adapter.

## 18. Show Limitations Honestly

State:

- model quality depends on dataset and training
- one-epoch smoke training proves pipeline readiness, not strong quality
- Full Fine-Tuning may fail on limited GPU
- QLoRA needs compatible CUDA/bitsandbytes
- Venn rendering depends on Mermaid.js support
- llama.cpp/GGUF is future optional compatibility
- no paid API is used
