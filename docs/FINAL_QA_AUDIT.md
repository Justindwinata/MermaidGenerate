# Final QA Audit

Audit date: 2026-07-23 Asia/Jakarta

## Summary

MermaidGenerate is ready for final academic submission with the required notebook, Gradio UI, local-first launch mode, Colab/share mode, dataset validation, Mermaid generation/repair, preview rendering, and fine-tuning UI/back end preserved.

This audit distinguishes between locally verified checks, user-side Colab evidence, and checks that should be demonstrated live during final presentation.

## Requirement Audit

| Requirement | Status | Evidence/Notes |
|---|---:|---|
| Notebook deliverable exists | Verified | `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` exists and is valid JSON. |
| `app.py` web app exists | Verified | `app.py` exists and exposes Gradio Blocks UI. |
| Mermaid inference uses Transformers + PyTorch | Verified by code/docs | `src/mermaid_generate/model_loader.py`, `src/mermaid_generate/inference.py`; no paid API runtime. |
| PEFT LoRA/QLoRA/Full FT paths exist | Verified by code/tests | `src/mermaid_generate/training.py`; UI exposes all three modes. |
| Tab `Generator Mermaid` exists | Verified by code/local UI smoke | Defined in `app.py`. |
| Tab `Dataset & Fine-Tuning` exists | Verified by code/local UI smoke | Defined in `app.py`. |
| Mind Map generation produces valid final code | Verified by tests/evidence | Repair fallback and validator tests pass; screenshot evidence exists. |
| Mind Map preview renders as diagram | Verified locally | `docs/evidence/screenshots/fix/05_iframe_preview_render_success.png`. |
| Venn generation produces valid final code | Verified by tests/evidence | Venn repair/compiler and validator tests pass. |
| Venn preview renders as diagram | Verified locally | `docs/evidence/screenshots/fix/05_iframe_preview_render_success.png`; renderer uses `venn-beta`. |
| Final code output is copyable | Verified by code | `gr.Code(label="Final valid Mermaid code")` remains in Generator tab. |
| Raw model output is secondary/debug | Verified by code | Advanced accordion remains collapsed by default. |
| Inference time is shown | Verified by code | `inference_time` textbox remains wired. |
| JSON/JSONL dataset upload works | Verified by code/local screenshots | File upload and validation callback remain wired. |
| Dataset validation works | Verified by tests/user evidence | Curated mixed dataset previously validated 150 valid, 0 invalid. |
| Dataset preview appears | Verified by code/screenshots | `gr.Dataframe` output remains wired. |
| Diagram/source distribution appears | Verified by code/screenshots | Distribution textboxes remain wired. |
| LoRA mode selectable | Verified by code | Fine-tuning dropdown includes `LoRA`. |
| QLoRA 4-bit selectable | Verified by code | Fine-tuning dropdown includes `QLoRA 4-bit`. |
| Full Fine-Tuning selectable | Verified by code | Fine-tuning dropdown includes `Full Fine-Tuning`. |
| Start Fine-Tuning button wired | Verified by code | Calls `start_training_from_ui`. |
| Cancel Training button wired | Verified by code | Calls `cancel_training`. |
| Refresh Status button wired | Verified by code | Calls `refresh_training_status`. |
| Clear Training State button wired | Verified by code | Calls `clear_training_state`. |
| Training logs/loss/progress/result UI visible | Verified by code/screenshots | Result summary and training logs textboxes remain present. |
| Adapter becomes active after training | Verified by code/user Colab evidence | `TRAINING_MANAGER.activate_completed_result` path remains intact; user-side LoRA evidence showed active adapter. |
| Adapter ZIP download visible | Verified by code/user Colab evidence | `gr.File(label="Download ZIP for LoRA/QLoRA adapter")` remains present. |
| Local mode works | Verified locally | `python3 app.py --local --port 7860`; `curl -I` returned `HTTP/1.1 200 OK`. |
| Custom local port supported | Verified by tests | Launch config tests cover custom port. |
| Share/Colab mode supported | Verified by tests/docs | `--share`, `--colab`, notebook `share=True`. |
| `python app.py --help` works | Verified locally | Validation command succeeds. |
| Mermaid preview renderer uses iframe | Verified by tests/evidence | `build_mermaid_preview_html` returns iframe and Venn `venn-beta`. |
| Outputs/checkpoints are not committed | Verified by Git hygiene | `outputs/` remains gitignored except `.gitkeep`. |

## Known Limitations

| Limitation | Status | Evidence/Notes |
|---|---:|---|
| Model quality depends on dataset and training duration | Active limitation | Repair fallback guarantees valid syntax, not semantic perfection. |
| Small LoRA smoke training may not make model perfectly reliable | Active limitation | User-side training completed, but raw model output can still be imperfect. |
| Full Fine-Tuning may require stronger GPU | Active limitation | Documented in README/training guide. |
| QLoRA requires compatible CUDA/bitsandbytes | Active limitation | Documented in README/training guide. |
| Colab needs Gradio Live/public link for easy browser access | Active limitation | Localhost/`0.0.0.0` is not a Colab browser URL. |
| Local mode requires dependencies and sufficient RAM/VRAM | Active limitation | Documented in local run guide. |
| llama.cpp/GGUF is future optional compatibility | Active limitation | Not implemented as main runtime. |

## Final Readiness Conclusion

The repository is ready for final submission after MG-0006 validation:

- notebook JSON is valid;
- final regression tests pass;
- local-first launch is documented and previously smoke-tested;
- Colab/share behavior is documented correctly;
- curated dataset exists and validates in regression tests;
- only `outputs/.gitkeep` is tracked under runtime outputs;
- no adapter ZIP, checkpoint, or model weight artifacts are committed.

During the live demo, the student should capture fresh Colab screenshots for GPU runtime, training logs, completed adapter status, and adapter ZIP download if required by the lecturer.
