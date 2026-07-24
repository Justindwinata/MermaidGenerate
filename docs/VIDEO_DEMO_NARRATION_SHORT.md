# Narasi Video Demo Pendek MermaidGenerate

Target durasi: 8 sampai 10 menit  
Bahasa: Indonesia  
Fokus: menunjukkan aplikasi bekerja dan memenuhi kebutuhan dosen.

## 1. Opening

"Halo, pada video ini saya mendemonstrasikan proyek MermaidGenerate, yaitu aplikasi AI lokal untuk membuat diagram Mermaid dalam bentuk Mind Map dan Venn Diagram. Proyek ini menggunakan Google Colab, Gradio, Transformers, PyTorch, dan PEFT. Tidak ada paid API yang digunakan."

## 2. Kebutuhan Tugas

"Kebutuhan tugas dari dosen adalah notebook yang berisi inference, upload dataset, dan training atau fine-tuning; dataset yang bervariasi; serta video yang menunjukkan aplikasi bekerja. Di sini notebook utama adalah `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`, dataset final berisi 1000 contoh, dan video ini menunjukkan alur aplikasinya."

## 3. Struktur Proyek

"Di repository ini ada notebook utama, `app.py` untuk Gradio web app, folder `src/mermaid_generate` untuk logic aplikasi, folder `datasets` untuk data, folder `scripts` untuk validasi dan packaging, folder `configs` untuk LoRA config, dan folder `docs` untuk dokumentasi."

## 4. Notebook dan Runtime

"Saya membuka notebook di Google Colab. Notebook ini memuat dependency installation, import library, GPU check, dataset validation, model loading, inference, fine-tuning, dan launch Gradio app. Untuk training, saya menggunakan runtime GPU. Jika GPU tidak tersedia, training tidak boleh diklaim berhasil."

## 5. Launch Gradio

"Setelah cell Gradio dijalankan, Colab memberikan link `gradio.live`. Link inilah yang dibuka di browser. `0.0.0.0:7860` bukan URL browser untuk Colab. Kalau dijalankan lokal, aplikasinya dibuka lewat `http://127.0.0.1:7860`."

## 6. Generator Mermaid

"Ini tab Generator Mermaid. Di sini pengguna memilih tipe diagram, memasukkan prompt, mengatur parameter generation, lalu menekan Generate. Output utama adalah final Mermaid code dan rendered preview."

## 7. Demo Mind Map

"Saya memilih Mind Map dan memasukkan prompt: `Buat mind map tentang strategi belajar AI untuk mahasiswa informatika.` Setelah Generate, output dimulai dengan `mindmap`, validation status valid, dan preview menampilkan diagram. Ini membuktikan inference Mind Map berjalan."

## 8. Demo Venn

"Sekarang saya memilih Venn Diagram dengan prompt: `Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.` Output dimulai dengan `venn`. Untuk preview, aplikasi mengubahnya secara internal menjadi `venn-beta`, sesuai dukungan Mermaid renderer. Set dan union divalidasi agar tidak ada undefined union."

## 9. Dataset dan Validasi

"Selanjutnya saya membuka tab Dataset & Fine-Tuning. Di sini dataset JSON atau JSONL bisa di-upload. Dataset final yang dikumpulkan adalah `mixed_mindmap_venn_expanded_1000.jsonl`, berisi 1000 contoh seimbang: 500 Mind Map dan 500 Venn. Untuk demo training yang lebih cepat, bisa memakai dataset 500 atau curated 150. Setelah klik Validate Dataset, sistem menampilkan total, valid, invalid, warnings, duplicate, dan distribusi diagram."

## 10. Fine-Tuning

"Untuk demo fine-tuning saya memilih LoRA, karena paling praktis di Colab. Parameter demo adalah 1 epoch, batch size 1, gradient accumulation 4, max sequence length 512, learning rate 2e-4, dan validation split 0.1. Training dijalankan dari browser UI, dan logs, loss, progress, result summary, serta tombol cancel tersedia."

## 11. Adapter

"Jika training selesai, adapter disimpan di `outputs/adapters`, otomatis diaktifkan untuk inference, dan ZIP adapter muncul untuk download. Adapter ZIP tidak dikomit ke Git karena merupakan output training."

## 12. Repair/Fallback

"Karena model kecil atau training singkat bisa menghasilkan raw output yang kurang valid, aplikasi tidak langsung merender raw output. Sistem melakukan extraction, repair atau fallback compiler, validation, lalu render. Jadi yang ditampilkan di code box utama adalah final valid Mermaid code."

## 13. Limitasi

"Limitasinya, kualitas model tetap bergantung pada dataset, durasi training, dan kapasitas model. QLoRA membutuhkan CUDA dan bitsandbytes yang kompatibel. Full Fine-Tuning membutuhkan GPU lebih kuat. Venn preview memakai Mermaid `venn-beta` secara internal. llama.cpp atau GGUF hanya kompatibilitas masa depan, bukan runtime utama."

## 14. Closing

"Kesimpulannya, proyek ini memenuhi kebutuhan tugas: notebook berisi inference, upload dataset, dan training; dataset sudah diperluas dan bervariasi; dan aplikasi terbukti bisa menghasilkan serta merender Mind Map dan Venn Diagram. MermaidGenerate siap dikumpulkan bersama notebook, dataset, dan video demo."
