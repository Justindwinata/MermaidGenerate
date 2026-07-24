# Narasi Video Demo Full MermaidGenerate

Target durasi: 15 sampai 20 menit  
Bahasa: Indonesia  
Fokus: penjelasan detail aplikasi, notebook, dataset, source code, training, dan packaging final.

## 1. Pembukaan

"Halo, pada video ini saya akan menjelaskan dan mendemonstrasikan MermaidGenerate. MermaidGenerate adalah aplikasi AI lokal untuk menghasilkan kode Mermaid dan preview visual untuk dua jenis diagram, yaitu Mind Map dan Venn Diagram. Aplikasi ini dibangun dengan Google Colab, Gradio, Transformers, PyTorch, dan PEFT. Proyek ini tidak menggunakan paid API."

## 2. Kebutuhan Dosen

"Kebutuhan dosen untuk submission adalah tiga hal. Pertama, harus ada notebook yang berisi inference, upload dataset, dan training atau fine-tuning. Kedua, harus ada dataset, dan semakin bervariasi prompt yang bisa ditangani, semakin baik. Ketiga, harus ada video yang membuktikan aplikasi bekerja. Proyek ini menyiapkan ketiga hal tersebut."

## 3. Nama dan Tujuan Proyek

"Tujuan MermaidGenerate adalah membantu pengguna membuat Mind Map dan Venn Diagram dalam format Mermaid. Pengguna cukup memasukkan prompt, memilih tipe diagram, lalu aplikasi menghasilkan kode Mermaid yang valid dan menampilkan preview diagram. Selain itu, pengguna juga dapat meng-upload dataset sendiri dan melakukan fine-tuning dari browser."

## 4. Struktur Repository

"Saya akan menunjukkan struktur repository. File notebook utama adalah `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`. File `app.py` adalah entrypoint aplikasi Gradio. Folder `src/mermaid_generate` berisi modul inti seperti dataset loader, validator, inference, training, adapter manager, dan renderer. Folder `datasets` berisi dataset contoh, curated dataset, expanded dataset, dan evaluation prompts. Folder `scripts` berisi script untuk build dataset, validasi dataset, evaluasi final, dan packaging ZIP. Folder `configs` berisi konfigurasi LoRA. Folder `docs` berisi panduan final, QA audit, dan script video."

## 5. Notebook Utama

"Notebook ini adalah file utama yang dikumpulkan. Di dalamnya ada section Project Overview, Install Dependencies, GPU Check, Dataset Upload and Validation, Mermaid Validator and Preview Renderer, Model Loading with Transformers and PyTorch, Mermaid Inference, LoRA/QLoRA/Full Fine-Tuning, Training Manager, Adapter ZIP Download, Gradio Web App, Evaluation Utilities, Notes, Limitations, dan Submission Guide. Jadi notebook ini secara eksplisit mencakup inference, upload dataset, dan fine-tuning."

## 6. Runtime dan Dependency

"Saya membuka notebook di Google Colab dan memilih runtime GPU. GPU penting untuk training LoRA atau QLoRA. Cell install dependency memasang library seperti torch, transformers, datasets, peft, accelerate, bitsandbytes jika compatible, dan gradio. Setelah itu cell import memuat library yang digunakan oleh notebook dan helper modules."

## 7. GPU Check

"Cell GPU check mencetak apakah CUDA tersedia dan nama GPU. Ini penting untuk transparansi. Jika CUDA tidak tersedia, training tidak boleh diklaim sukses. Dalam kondisi tersebut, kita tetap bisa menunjukkan dataset validation dan UI, tetapi training harus dijelaskan sebagai belum dijalankan."

## 8. Launch Gradio

"Setelah semua setup selesai, saya menjalankan cell Gradio. Di Google Colab, link yang digunakan adalah `gradio.live`, karena aplikasi berjalan di server Colab. Alamat `0.0.0.0:7860` bukan URL yang dibuka di browser. Kalau dijalankan di laptop lokal, command-nya adalah `python app.py --local`, kemudian buka `http://127.0.0.1:7860`."

## 9. Generator Mermaid Tab

"Tab pertama adalah Generator Mermaid. Komponen utamanya adalah status model atau adapter aktif, dropdown tipe diagram, prompt textbox, parameter generation seperti max_new_tokens, temperature, top_p, repetition_penalty, tombol Generate dan Clear, final Mermaid code, rendered preview, validation status, inference time, dan advanced debug raw output."

## 10. Inference Mind Map

"Saya memilih Mind Map dan memasukkan prompt: `Buat mind map tentang strategi belajar AI untuk mahasiswa informatika.` Setelah klik Generate, aplikasi menjalankan inference menggunakan model Transformers/PyTorch. Output final harus dimulai dengan `mindmap`, memiliki root, dan memakai indentasi hierarchy yang valid. Di preview terlihat diagram Mind Map berhasil dirender."

## 11. Inference Venn Diagram

"Selanjutnya saya memilih Venn Diagram dan memasukkan prompt: `Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.` Output assignment-facing dimulai dengan `venn`. Untuk renderer, aplikasi mengubah first line menjadi `venn-beta` secara internal. Ini karena Mermaid Venn rendering menggunakan syntax `venn-beta`. Validator memastikan set A, B, C didefinisikan sebelum union, sehingga tidak ada undefined set."

## 12. Mermaid Preview dan Validation

"Preview Mermaid dibuat melalui HTML iframe yang memuat Mermaid.js versi pinned. Jika kode valid, diagram dirender sebagai SVG. Jika kode tidak valid, renderer tidak menerima raw output langsung. Sistem menampilkan error yang terbaca, tetapi main output tetap berisi final code hasil validasi atau fallback."

## 13. Repair/Fallback Mechanism

"Fitur penting proyek ini adalah output reliability. Raw output dari LLM bisa berisi teks tambahan atau syntax yang tidak valid. Karena itu pipeline inference adalah: raw model output, extract first Mermaid diagram, repair atau deterministic compiler fallback, validate, convert untuk renderer, lalu render. Dengan cara ini, aplikasi tetap menghasilkan final Mermaid code yang valid tanpa mengklaim bahwa raw model selalu sempurna."

## 14. Dataset Files

"Dataset utama berada di folder `datasets`. Ada dataset curated 150 untuk smoke test, dataset expanded 500 untuk demo training yang lebih cepat, dan dataset expanded 1000 untuk submission final. Dataset final `mixed_mindmap_venn_expanded_1000.jsonl` berisi 500 Mind Map dan 500 Venn, invalid 0, duplicate 0. Ini meningkatkan variasi prompt dan target yang bisa dipelajari model."

## 15. Dataset Format

"Dataset mendukung tiga format: messages, prompt-completion, dan instruction-output. Dataset expanded memakai prompt-completion. Prompt adalah instruksi pengguna, completion adalah target Mermaid code yang benar. Setiap target hanya berisi satu diagram, tidak ada markdown fence, dan tidak memakai flowchart karena proyek hanya fokus pada Mind Map dan Venn."

## 16. Dataset Upload dan Validation

"Di tab Dataset & Fine-Tuning, saya upload dataset. Setelah klik Validate Dataset, sistem menampilkan preview data, total samples, valid samples, invalid samples, warnings, duplicates, diagram type distribution, dan source format distribution. Training hanya boleh dilanjutkan jika ada valid samples dan tidak ada invalid rows yang bermasalah."

## 17. Fine-Tuning UI

"Bagian fine-tuning menyediakan mode LoRA, QLoRA 4-bit, dan Full Fine-Tuning. Untuk demo, LoRA adalah pilihan paling aman karena melatih adapter kecil. Kontrol hyperparameter yang tersedia adalah epochs, learning rate, batch size, gradient accumulation, max sequence length, dan validation split ratio."

## 18. LoRA Training

"Saat tombol Start Fine-Tuning diklik, training berjalan dari browser UI. Progress dan loss logs bukan simulasi. UI juga menyediakan Cancel Training, Refresh Status, dan Clear Training State. Jika training selesai, result summary menampilkan status completed, mode, output path, ZIP path, train loss, eval loss jika ada, dan message."

## 19. Adapter Activation

"Setelah LoRA atau QLoRA berhasil, adapter disimpan di `outputs/adapters/<timestamp>`, dibuat ZIP, dan otomatis diaktifkan sebagai model aktif. Artinya inference berikutnya dapat memakai adapter yang baru dilatih tanpa restart aplikasi jika aktivasi berhasil."

## 20. Adapter ZIP Download

"ZIP adapter ditampilkan di UI agar bisa di-download. ZIP ini adalah artifact training dan tidak dikomit ke repository karena bisa besar dan termasuk output runtime. Dalam video, jika training selesai, saya menunjukkan tombol download ZIP sebagai bukti fitur adapter download tersedia."

## 21. Source Code Walkthrough

"Secara source code, `app.py` membangun UI dan callback. `dataset_loader.py` membaca dan menormalisasi dataset. `dataset_validator.py` membuat validation report. `mermaid_validator.py` mengecek syntax Mermaid. `diagram_repair.py` membuat repair atau fallback valid untuk Mind Map dan Venn. `mermaid_preview.py` membuat HTML preview. `model_loader.py` memuat tokenizer dan model. `inference.py` menjalankan prompt template, generation, validation, dan repair. `training.py` memuat logic LoRA, QLoRA, dan Full Fine-Tuning. `training_manager.py` mengatur background training job. `adapter_manager.py` mengelola aktivasi adapter dan ZIP. `evaluation.py` menghitung metrik validitas output."

## 22. Dataset Scripts

"Script `build_expanded_dataset.py` membangun dataset 500 dan 1000 secara deterministic. `validate_expanded_dataset.py` memastikan semua completion valid, tidak duplikat, dan Venn tidak punya undefined union. `summarize_dataset_quality.py` membuat report JSON dan Markdown. `run_final_quality_evaluation.py` menjalankan validator-only evaluation tanpa download model, atau model mode jika dijalankan di Colab/GPU."

## 23. Packaging Scripts

"Untuk submission final, `build_submission_package.py` membuat folder staging dan ZIP final di `dist/MermaidGenerate_Final_Submission.zip`. Script ini memasukkan notebook, dataset, source code, docs, report, dan video script. `verify_submission_package.py` membuka ZIP dan memastikan file wajib ada serta file terlarang seperti checkpoint, adapter, model weight, cache, dan nested ZIP tidak ikut masuk."

## 24. Local vs Colab

"Mode lokal menggunakan `python app.py --local` dan URL `http://127.0.0.1:7860`. Mode Colab menggunakan public `gradio.live` link. Ini penting karena `127.0.0.1` hanya berlaku pada mesin yang menjalankan server, sedangkan Colab berjalan di mesin remote."

## 25. Limitasi

"Limitasi proyek ini adalah kualitas model masih bergantung pada dataset, durasi training, dan kapasitas model. TinyLlama dan LoRA singkat mungkin belum menghasilkan output sempurna, sehingga fallback repair tetap diperlukan sebagai syntax-safety guard. QLoRA membutuhkan CUDA dan bitsandbytes yang kompatibel. Full Fine-Tuning bisa memerlukan GPU lebih kuat. llama.cpp atau GGUF hanya rencana kompatibilitas masa depan, bukan runtime utama."

## 26. Closing

"Kesimpulannya, MermaidGenerate sudah memenuhi requirement dosen. Notebook utama berisi inference, upload dataset, dan fine-tuning. Dataset final sudah diperluas menjadi 1000 contoh seimbang dan tervalidasi. Aplikasi web Gradio dapat menghasilkan dan merender Mind Map serta Venn Diagram. Video ini menunjukkan alur kerja aplikasi dari notebook, generator, dataset validation, fine-tuning UI, adapter, sampai packaging final."
