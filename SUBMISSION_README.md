# MermaidGenerate Final Submission README

## Judul Proyek

MermaidGenerate - Local AI Mermaid Diagram Generator for Mind Map and Venn Diagram.

Proyek ini adalah aplikasi AI lokal berbasis Google Colab dan Gradio untuk membuat kode Mermaid dan preview visual untuk:

- Mind Map
- Venn Diagram

Runtime utama yang digunakan adalah Hugging Face Transformers, PyTorch, dan PEFT. Tidak ada paid API.

## Isi Submission

Paket submission berisi:

- notebook utama;
- dataset final dan dataset demo;
- source code aplikasi;
- script validasi, evaluasi, dan packaging;
- konfigurasi LoRA;
- dokumentasi teknis;
- script video demo.

## Mapping Kebutuhan Dosen

| Kebutuhan Dosen | File Utama | Status |
|---|---|---|
| Notebook berisi inference, upload dataset, dan fine-tuning | `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` | Ada |
| Dataset yang variatif | `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl` | Ada, 1000 contoh |
| Video demonstrasi aplikasi bekerja | `docs/VIDEO_DEMO_SCRIPT_DETAILED.md` dan checklist/narasi | Siap untuk rekaman |

## Cara Membuka Notebook

1. Buka Google Colab.
2. Upload atau buka `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`.
3. Pilih **Runtime > Change runtime type > GPU** jika ingin menjalankan training.
4. Jalankan cell dari atas ke bawah.

## Cara Menjalankan di Colab

Di Colab, jalankan cell launch Gradio dengan mode share. Setelah itu buka link:

```text
https://xxxxx.gradio.live
```

Jangan membuka `0.0.0.0:7860` di browser. Alamat itu hanya bind address server, bukan URL browser untuk Colab.

## Dataset yang Digunakan

Dataset utama untuk submission:

```text
datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl
```

Dataset ini berisi 1000 contoh seimbang:

- 500 Mind Map
- 500 Venn Diagram

Dataset demo yang lebih cepat:

```text
datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl
```

Dataset smoke test tercepat:

```text
datasets/curated/mixed_mindmap_venn_curated.jsonl
```

## Cara Validasi Dataset

Di UI, buka tab **Dataset & Fine-Tuning**, upload dataset JSONL, lalu klik **Validate Dataset**.

Secara terminal:

```bash
python3 scripts/validate_expanded_dataset.py
```

Expected result:

- invalid: 0
- warnings: 0
- duplicate: 0

## Cara Menjalankan Inference

1. Buka tab **Generator Mermaid**.
2. Pilih diagram type: Mind Map, Venn Diagram, atau Auto Detect.
3. Tulis prompt.
4. Klik **Generate**.
5. Lihat final Mermaid code dan preview diagram.

Contoh Mind Map:

```text
Buat mind map tentang strategi belajar AI untuk mahasiswa informatika.
```

Contoh Venn:

```text
Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.
```

## Cara Fine-Tuning

1. Buka tab **Dataset & Fine-Tuning**.
2. Upload dan validasi dataset.
3. Pilih mode **LoRA** untuk demo.
4. Gunakan 1 epoch, batch size 1, gradient accumulation 4, max sequence length 512.
5. Klik **Start Fine-Tuning**.
6. Klik **Refresh Status** untuk melihat progress, loss, dan hasil training.

QLoRA dan Full Fine-Tuning tersedia, tetapi lebih berat dan membutuhkan environment GPU/CUDA yang sesuai.

## Adapter ZIP

Jika LoRA atau QLoRA selesai, adapter akan disimpan di:

```text
outputs/adapters/<timestamp>/
```

UI menyediakan ZIP download. ZIP adapter dibuat saat demo dan tidak perlu dikomit ke repository.

## Video Demo

Gunakan dokumen berikut:

- `docs/VIDEO_DEMO_SCRIPT_DETAILED.md`
- `docs/VIDEO_DEMO_CHECKLIST.md`
- `docs/VIDEO_DEMO_NARRATION_SHORT.md`
- `docs/VIDEO_DEMO_NARRATION_FULL.md`

## Repository

```text
https://github.com/Justindwinata/MermaidGenerate
```

## Limitasi

- Kualitas model bergantung pada dataset, durasi training, dan kapasitas model.
- Fallback repair digunakan untuk memastikan syntax Mermaid valid.
- QLoRA membutuhkan CUDA dan bitsandbytes yang kompatibel.
- Full Fine-Tuning dapat gagal pada GPU terbatas.
- Colab memakai `gradio.live`; lokal memakai `http://127.0.0.1:7860`.
- llama.cpp/GGUF hanya kompatibilitas masa depan, bukan runtime utama.
