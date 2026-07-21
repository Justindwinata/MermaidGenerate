# Product Requirements

## Goal

MermaidGenerate provides a local AI workflow for generating and fine-tuning Mermaid Mind Map and Venn Diagram outputs in Google Colab.

## Required User Workflows

- Generate Mermaid code from a prompt.
- Select Mind Map, Venn Diagram, or Auto Detect.
- Preview rendered Mermaid diagrams in the browser.
- Upload JSON/JSONL datasets.
- Validate dataset quality before training.
- Fine-tune using LoRA, QLoRA 4-bit, or Full Fine-Tuning.
- View real progress, loss logs, status, and errors.
- Cancel training when possible.
- Activate completed adapter/model output.
- Download LoRA/QLoRA adapter ZIP files.

## Non-Goals

- Flowchart generation as the final target.
- Paid API inference.
- Fake training progress.
- llama.cpp/GGUF as the primary runtime.
