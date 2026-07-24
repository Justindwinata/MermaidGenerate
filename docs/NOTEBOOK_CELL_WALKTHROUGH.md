# Walkthrough Cell Notebook MermaidGenerate

Dokumen ini menjelaskan section utama di `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` untuk membantu rekaman video demo.

## 1. Project Overview

Purpose:

- Memperkenalkan MermaidGenerate sebagai notebook-first project.
- Menjelaskan target diagram: Mind Map dan Venn Diagram.

What the code/markdown does:

- Menjelaskan bahwa runtime utama adalah Transformers, PyTorch, dan PEFT.
- Menjelaskan bahwa Gradio dipakai sebagai web UI.

Why needed:

- Membuktikan scope proyek sesuai requirement.

What to say:

"Section ini menjelaskan tujuan proyek, yaitu membuat generator Mermaid untuk Mind Map dan Venn Diagram dengan runtime Transformers dan PyTorch."

Expected output:

- Tidak ada output kode; reviewer memahami overview proyek.

## 2. Install Dependencies

Purpose:

- Menginstal library yang dibutuhkan di Colab.

What the code does:

- Menginstal Gradio, Transformers, Datasets, PEFT, Accelerate, bitsandbytes jika kompatibel, dan dependency pendukung.

Why needed:

- Aplikasi membutuhkan dependency untuk inference, dataset processing, dan training.

What to say:

"Cell ini menyiapkan environment agar notebook bisa menjalankan model, dataset validation, fine-tuning, dan Gradio UI."

Expected output:

- Install selesai tanpa error kritis.

## 3. Restart Runtime Note

Purpose:

- Memberi instruksi restart runtime jika dependency Colab memerlukannya.

What it does:

- Memberikan catatan agar user menjalankan ulang cell setelah restart.

Why needed:

- Colab kadang membutuhkan restart setelah instalasi paket tertentu.

What to say:

"Jika Colab meminta restart runtime, lakukan restart lalu lanjutkan dari import library."

Expected output:

- Runtime siap melanjutkan eksekusi.

## 4. Import Libraries

Purpose:

- Mengimpor library Python dan helper module proyek.

What the code does:

- Mengatur path project.
- Mengimpor Torch, Transformers helper, dataset utilities, Mermaid validator, dan Gradio app support.

Why needed:

- Semua function utama notebook membutuhkan import ini.

What to say:

"Cell import ini menghubungkan notebook dengan source code helper di `src/mermaid_generate`."

Expected output:

- Import sukses tanpa `ModuleNotFoundError`.

## 5. GPU Check

Purpose:

- Mengecek CUDA dan GPU.

What the code does:

- Memanggil `torch.cuda.is_available()`.
- Menampilkan nama GPU jika tersedia.

Why needed:

- Training LoRA/QLoRA membutuhkan GPU agar praktis.

What to say:

"GPU check penting untuk membuktikan environment training. Jika CUDA tidak tersedia, training tidak boleh diklaim berhasil."

Expected output:

- `CUDA available: True` jika GPU tersedia.

## 6. Configuration

Purpose:

- Menentukan konfigurasi default project.

What the code does:

- Menetapkan base model default.
- Menetapkan path dataset, outputs, adapter, dan parameter generation.

Why needed:

- Inference dan training perlu config konsisten.

What to say:

"Default model proyek ini adalah TinyLlama karena relatif ringan untuk eksperimen lokal dan Colab."

Expected output:

- Config variable siap digunakan.

## 7. Reference Notebook Notes

Purpose:

- Menjelaskan bahwa notebook referensi sudah diinspeksi.

What it does:

- Mengarahkan reviewer ke `docs/REFERENCE_NOTEBOOK_INSPECTION.md`.

Why needed:

- Menunjukkan proyek tidak menyalin buta notebook referensi.

What to say:

"Reference notebook dipakai sebagai acuan workflow, tetapi target final proyek adalah Mind Map dan Venn, bukan flowchart."

Expected output:

- Reviewer memahami dasar desain.

## 8. Dataset Upload and Validation

Purpose:

- Menangani upload dan validasi dataset.

What the code does:

- Memakai dataset loader dan validator.
- Mendukung format messages, prompt-completion, dan instruction-output.
- Menampilkan valid/invalid/warning/duplicate counts.

Why needed:

- Ini memenuhi requirement upload dataset.

What to say:

"Bagian ini membuktikan dataset bisa di-upload, dinormalisasi, dan divalidasi sebelum training."

Expected output:

- Dataset valid menunjukkan invalid 0 dan train ready true.

## 9. Mermaid Validation and Preview

Purpose:

- Memvalidasi syntax Mermaid dan membuat preview.

What the code does:

- Mengecek `mindmap`.
- Mengecek `venn`.
- Mengubah `venn` menjadi `venn-beta` untuk renderer.
- Membuat HTML preview.

Why needed:

- Output tidak cukup berupa teks; harus bisa dirender.

What to say:

"Validator memastikan final code valid sebelum dikirim ke renderer."

Expected output:

- Preview HTML dapat menampilkan diagram.

## 10. Model Loading

Purpose:

- Memuat tokenizer dan model.

What the code does:

- Menggunakan Transformers dan PyTorch.
- Mendukung base model dan adapter.

Why needed:

- Ini memenuhi requirement inference memakai Transformers/PyTorch.

What to say:

"Model loading memakai Hugging Face Transformers dan PyTorch, sesuai requirement tugas."

Expected output:

- Model/tokenizer berhasil dimuat jika resource cukup.

## 11. Inference

Purpose:

- Menghasilkan Mermaid code dari prompt.

What the code does:

- Membuat strict prompt template.
- Menjalankan generation.
- Membersihkan raw output.
- Memvalidasi dan memperbaiki hasil jika perlu.

Why needed:

- Ini bagian inference utama.

What to say:

"Inference menghasilkan final valid Mermaid code, bukan raw output langsung."

Expected output:

- Code dimulai dengan `mindmap` atau `venn`.

## 12. Fine-Tuning Modes

Purpose:

- Menjelaskan mode training.

What the code does:

- Menyiapkan LoRA, QLoRA 4-bit, dan Full Fine-Tuning.

Why needed:

- Tugas mensyaratkan training/fine-tuning dari browser UI.

What to say:

"LoRA adalah mode demo paling praktis. QLoRA dan Full FT tersedia tetapi lebih bergantung pada GPU."

Expected output:

- Config training siap.

## 13. LoRA / QLoRA / Full Fine-Tuning

Purpose:

- Menjalankan pipeline training.

What the code does:

- Membuat training text.
- Split train/eval.
- Load model untuk training.
- Apply PEFT jika mode LoRA/QLoRA.
- Save output.

Why needed:

- Ini memenuhi komponen fine-tuning.

What to say:

"Training dilakukan secara real, jadi status berhasil hanya diklaim jika proses benar-benar selesai."

Expected output:

- Training result dan loss muncul jika training berhasil.

## 14. Training Manager, Logs, Cancel, and Adapter Activation

Purpose:

- Mengelola job training dari UI.

What the code does:

- Menjalankan training di background.
- Menampilkan progress dan logs.
- Mendukung cancel.
- Mengaktifkan adapter setelah training selesai.

Why needed:

- UI harus menampilkan progress, loss, logs, cancellation, dan result.

What to say:

"Training manager membuat fine-tuning bisa dikontrol dari browser."

Expected output:

- Status training berubah dari idle ke training lalu completed/failed.

## 15. Adapter ZIP Download

Purpose:

- Menghasilkan ZIP adapter LoRA/QLoRA.

What the code does:

- Membuat ZIP dari folder adapter.
- Menyediakan path untuk download di UI.

Why needed:

- Requirement meminta adapter LoRA/QLoRA dapat di-download sebagai ZIP.

What to say:

"ZIP adapter muncul setelah training berhasil dan tidak dikomit ke Git."

Expected output:

- File ZIP tersedia jika LoRA/QLoRA sukses.

## 16. Gradio Web App

Purpose:

- Meluncurkan aplikasi web.

What the code does:

- Membuat tab Generator Mermaid.
- Membuat tab Dataset & Fine-Tuning.
- Menghubungkan callback inference, validation, training, refresh, cancel, dan download.

Why needed:

- Semua fitur harus bisa dipakai dari browser.

What to say:

"Gradio adalah interface utama untuk demo dan penggunaan aplikasi."

Expected output:

- Link Gradio muncul.

## 17. Demo Steps

Purpose:

- Memberikan urutan demo.

What it does:

- Menjelaskan prompt demo, dataset yang dipakai, dan flow training.

Why needed:

- Memudahkan reviewer menjalankan notebook.

What to say:

"Notebook sudah menyertakan urutan demo agar dosen dapat mereplikasi."

Expected output:

- Demo bisa diikuti step-by-step.

## 18. Evaluation Utilities

Purpose:

- Menyediakan evaluasi dasar.

What the code does:

- Mengukur syntax validity, diagram type accuracy, prefix accuracy, exact match, dan markdown fence violation.

Why needed:

- Evaluasi tidak hanya berdasarkan training loss.

What to say:

"Evaluasi validator-only membuktikan dataset dan prompt coverage; model-mode harus dijalankan hanya jika inference real dilakukan."

Expected output:

- Report evaluasi tersedia.

## 19. Troubleshooting

Purpose:

- Menjelaskan error umum.

What it does:

- Menjelaskan Colab link, CUDA unavailable, QLoRA bitsandbytes, Full FT OOM, Mermaid preview, dan adapter ZIP.

Why needed:

- Membantu demo berjalan lancar.

What to say:

"Troubleshooting disediakan agar error umum bisa dijelaskan secara jujur."

Expected output:

- User tahu langkah pemulihan.

## Komponen Wajib Dosen

| Komponen | Section Notebook | Status |
|---|---|---|
| Inference | Model Loading, Inference, Generator Mermaid | Ada |
| Upload dataset | Dataset Upload and Validation | Ada |
| Training/fine-tuning | Fine-Tuning Modes, Training Manager, Adapter ZIP | Ada |
