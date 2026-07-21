# Decision Log

## Transformers and PyTorch

The assignment explicitly requires Transformers and PyTorch inference. MermaidGenerate therefore does not use llama.cpp as the primary runtime.

## TinyLlama Default

TinyLlama is local-friendly, LLaMA-family, and practical for Colab LoRA/QLoRA experiments.

## Mermaid Venn Rendering

User-facing Venn outputs may start with `venn`. Mermaid.js renders the current Venn syntax as `venn-beta`, so preview code is safely normalized while the copyable assignment code remains `venn`.

## Gradio

Gradio Blocks is used for the web UI because the contract requires browser-based generator and fine-tuning tabs.
