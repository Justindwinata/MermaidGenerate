# Walkthrough Source Code MermaidGenerate

Dokumen ini menjelaskan file source code penting yang dapat disebutkan dalam video demo.

## `app.py`

Purpose:

- Entry point aplikasi Gradio.
- Menyediakan local mode, share mode, dan Colab mode.

Important functions/classes:

- `LaunchConfig`: menyimpan mode launch, host, port, dan share.
- `resolve_launch_config`: menentukan mode local/share/Colab.
- `print_launch_banner`: menampilkan URL dan mode launch di terminal.
- `readable_model_status`: menampilkan status base model atau adapter aktif.
- `normalize_ui_diagram_type`: mengubah label UI menjadi `mindmap`, `venn`, atau `auto`.
- `generate_from_ui`: callback inference dari tab Generator Mermaid.
- `validate_upload`: callback upload dan validasi dataset.
- `start_training_from_ui`: memulai fine-tuning dari browser.
- `refresh_training_status`: membaca progress, logs, result, adapter ZIP, dan aktivasi adapter.
- `cancel_training`: meminta pembatalan training.
- `clear_training_state`: membersihkan state training UI.
- `build_app`: membangun Gradio Blocks UI.
- `build_parser` dan `main`: menjalankan CLI local/share/Colab.

Connection to app:

- Semua tombol UI Gradio terhubung ke function di file ini.

Lecturer requirement:

- Menyediakan tab Generator Mermaid, Dataset & Fine-Tuning, training UI, logs, cancel, adapter ZIP, dan launch mode.

What to mention:

"`app.py` adalah penghubung antara UI dan backend inference, dataset validation, serta training."

## `src/mermaid_generate/dataset_loader.py`

Purpose:

- Membaca dan menormalisasi dataset JSON/JSONL.

Important functions/classes:

- `DatasetLoadError`
- `load_raw_records`
- `extract_messages_sample`
- `normalize_record`
- `load_and_normalize_dataset`

Connection to app:

- Dipakai saat user upload dataset.

Lecturer requirement:

- Mendukung upload dataset dengan format messages, prompt-completion, dan instruction-output.

What to mention:

"Loader memastikan format dataset berbeda bisa masuk ke schema internal yang sama."

## `src/mermaid_generate/dataset_validator.py`

Purpose:

- Membuat validation report dataset.

Important functions/classes:

- `RowIssue`
- `DatasetValidationReport`
- `target_prefix`
- `validate_normalized_sample`
- `validate_samples`
- `validate_dataset_file`

Connection to app:

- Dipanggil oleh `validate_upload` di `app.py`.

Lecturer requirement:

- Dataset upload harus divalidasi sebelum training.

What to mention:

"Validator mengecek prompt kosong, target kosong, prefix diagram, markdown fence, duplicate, distribution, dan train readiness."

## `src/mermaid_generate/mermaid_validator.py`

Purpose:

- Membersihkan, mengekstrak, dan memvalidasi Mermaid code.

Important functions/classes:

- `MermaidValidationResult`
- `strip_markdown_fences`
- `extract_first_mermaid_diagram`
- `infer_diagram_type`
- `normalize_venn_for_renderer`
- `normalize_for_assignment`
- `postprocess_mermaid_output`
- `validate_mindmap`
- `validate_venn`
- `validate_mermaid_code`

Connection to app:

- Dipakai sebelum preview render.

Lecturer requirement:

- Memastikan output Mind Map dan Venn valid.

What to mention:

"Validator mencegah raw output invalid langsung dikirim ke renderer."

## `src/mermaid_generate/diagram_repair.py`

Purpose:

- Memperbaiki output model atau membuat fallback valid.

Important functions/classes:

- `RepairResult`
- `repair_or_compile_venn`
- `compile_safe_venn`
- `repair_venn_candidate`
- `repair_or_compile_mindmap`
- `compile_safe_mindmap`
- `repair_mindmap_candidate`
- `extract_venn_labels`
- `extract_mindmap_topic`

Connection to app:

- Dipakai dalam pipeline `generate_mermaid`.

Lecturer requirement:

- Membuat demo diagram tetap reliable meskipun model kecil menghasilkan output kurang rapi.

What to mention:

"Fallback repair adalah syntax-safety guard, bukan klaim bahwa model selalu sempurna."

## `src/mermaid_generate/mermaid_preview.py`

Purpose:

- Membuat HTML preview Mermaid.

Important functions:

- `_preview_iframe_srcdoc`
- `build_mermaid_preview_html`

Connection to app:

- Output HTML dipasang di `gr.HTML`.

Lecturer requirement:

- Preview harus merender diagram, bukan hanya teks.

What to mention:

"Venn code `venn` dikonversi ke `venn-beta` di renderer iframe."

## `src/mermaid_generate/model_loader.py`

Purpose:

- Memuat model dan tokenizer Transformers/PyTorch.

Important functions/classes:

- `ActiveModelState`
- `resolve_torch_dtype`
- `load_base_model`
- `load_adapter`
- `load_full_model`

Connection to app:

- Dipakai oleh inference dan adapter activation.

Lecturer requirement:

- Inference memakai Transformers dan PyTorch.

What to mention:

"Model loader menjaga active model state agar adapter hasil training dapat dipakai."

## `src/mermaid_generate/inference.py`

Purpose:

- Menjalankan pipeline generation.

Important functions/classes:

- `GenerationSettings`
- `InferenceResult`
- `normalize_diagram_type`
- `detect_diagram_type_from_prompt`
- `build_generation_prompt`
- `apply_chat_template`
- `ensure_model_loaded`
- `generate_mermaid`

Connection to app:

- Dipanggil oleh `generate_from_ui`.

Lecturer requirement:

- Menyediakan inference Mind Map dan Venn.

What to mention:

"`generate_mermaid` menjalankan prompt template, generation, repair, validation, dan final code output."

## `src/mermaid_generate/training.py`

Purpose:

- Menjalankan fine-tuning.

Important functions/classes:

- `FineTuningConfig`
- `TrainingResult`
- `build_training_text`
- `split_train_eval`
- `make_output_dir`
- `create_zip`
- `CancelTrainingCallback`
- `ProgressLoggingCallback`
- `tokenize_training_dataset`
- `load_model_for_training`
- `apply_peft_if_needed`
- `run_fine_tuning`

Connection to app:

- Dipakai oleh `TrainingManager`.

Lecturer requirement:

- LoRA, QLoRA 4-bit, dan Full Fine-Tuning tersedia.

What to mention:

"Training real dijalankan di backend; UI hanya menampilkan status dan log."

## `src/mermaid_generate/training_manager.py`

Purpose:

- Mengatur background training job.

Important classes:

- `TrainingJobState`
- `TrainingManager`

Connection to app:

- `TRAINING_MANAGER` dipakai oleh start, refresh, cancel, clear.

Lecturer requirement:

- UI harus menampilkan progress, loss, logs, cancellation, dan result.

What to mention:

"Training manager membuat browser UI tetap responsif saat training berjalan."

## `src/mermaid_generate/adapter_manager.py`

Purpose:

- Mengelola adapter dan full model activation.

Important functions/classes:

- `AdapterMetadata`
- `current_adapter_metadata`
- `ensure_adapter_zip`
- `activate_adapter_output`
- `activate_full_model_output`
- `activate_training_result`

Connection to app:

- Dipakai setelah training selesai.

Lecturer requirement:

- Adapter otomatis aktif dan ZIP adapter dapat di-download.

What to mention:

"Adapter manager mengubah hasil training menjadi model aktif untuk inference."

## `src/mermaid_generate/evaluation.py`

Purpose:

- Menghitung metrik evaluasi output Mermaid.

Important functions/classes:

- `EvaluationMetrics`
- `normalize_exact`
- `evaluate_predictions`
- `run_manual_test_set`

Connection to app:

- Dipakai oleh script evaluasi.

Lecturer requirement:

- Evaluasi tidak hanya melihat training loss.

What to mention:

"Metrik mengecek syntax validity, diagram type accuracy, prefix accuracy, exact match, dan markdown fence violation."

## `src/mermaid_generate/notebook_utils.py`

Purpose:

- Helper khusus notebook.

Important functions:

- `ensure_src_path`
- `in_colab`

Connection to app:

- Membantu notebook menemukan source code.

Lecturer requirement:

- Notebook tetap Colab-compatible.

## `src/mermaid_generate/utils.py`

Purpose:

- Utility text dan metadata.

Important functions:

- `stable_id`
- `read_text`
- `compact_text`
- `infer_language`
- `infer_complexity`
- `infer_domain`

Connection to app:

- Dipakai loader dan dataset builder.

## Scripts

### `scripts/build_expanded_dataset.py`

Purpose:

- Membuat dataset expanded 500/1000 dan final evaluation prompts secara deterministic.

Important functions/classes:

- `MindmapTopic`
- `VennTopic`
- `mindmap_code`
- `mindmap_prompt`
- `build_mindmap_rows`
- `venn_code`
- `venn_prompt`
- `build_venn_rows`
- `interleave`
- `build_eval_prompts`

Lecturer requirement:

- Menyediakan dataset variatif.

### `scripts/validate_expanded_dataset.py`

Purpose:

- Validasi ketat dataset expanded.

Important functions:

- `analyze_dataset`
- `validate_all`
- `main`

Lecturer requirement:

- Membuktikan dataset valid, duplicate 0, invalid 0.

### `scripts/summarize_dataset_quality.py`

Purpose:

- Membuat report kualitas dataset.

Important functions:

- `build_summary`
- `write_markdown`
- `main`

Lecturer requirement:

- Menyediakan evidence dataset quality.

### `scripts/run_final_quality_evaluation.py`

Purpose:

- Menjalankan validator-only atau model-mode evaluation.

Important functions:

- `validator_only`
- `model_mode`
- `write_result`
- `main`

Lecturer requirement:

- Membantu evaluasi final secara jujur.

### `scripts/build_submission_package.py`

Purpose:

- Membuat staging folder dan final ZIP package.

Important functions:

- `copy_file`
- `copy_dir`
- `build_generated_manifest`
- `build_generated_readme`
- `create_zip`
- `verify_staging_required_files`
- `main`

Lecturer requirement:

- Mempermudah submit notebook, dataset, source, docs, dan script video.

### `scripts/verify_submission_package.py`

Purpose:

- Memverifikasi ZIP final.

Important functions:

- `strip_prefix`
- `forbidden_reason`
- `main`

Lecturer requirement:

- Memastikan package berisi file wajib dan tidak berisi checkpoint/adapters besar.

## Configs

Purpose:

- Menyimpan rekomendasi hyperparameter training.

Files:

- `configs/lora_smoke_config.json`
- `configs/lora_medium_dataset_config.json`
- `configs/lora_expanded_dataset_config.json`

What to mention:

"Config membantu memilih dataset dan hyperparameter sesuai waktu demo."

## Datasets

Purpose:

- Menyediakan data training dan evaluasi.

Important files:

- `datasets/curated/mixed_mindmap_venn_curated.jsonl`
- `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`
- `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`
- `datasets/evaluation/final_eval_prompts_100.jsonl`

What to mention:

"Dataset utama yang dikumpulkan adalah expanded 1000 karena paling variatif dan balanced."
