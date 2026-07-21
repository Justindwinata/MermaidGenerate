# System Architecture

```mermaid
flowchart TD
  A[Gradio UI] --> B[Dataset Validator]
  A --> C[Inference Service]
  A --> D[Training Manager]
  B --> E[Normalized Dataset]
  C --> F[Transformers + PyTorch Model]
  D --> G[PEFT LoRA/QLoRA/Full FT]
  G --> H[outputs/adapters or outputs/full_models]
  H --> I[Adapter Manager]
  I --> F
  C --> J[Mermaid Validator]
  J --> K[Mermaid.js Preview]
```

## Runtime

The default model is `TinyLlama/TinyLlama-1.1B-Chat-v1.0`. Inference and training use Transformers and PyTorch. PEFT powers LoRA/QLoRA. bitsandbytes is optional for QLoRA and depends on CUDA compatibility.

## Storage

Training outputs are written to `outputs/`, which is gitignored except for `.gitkeep`.
