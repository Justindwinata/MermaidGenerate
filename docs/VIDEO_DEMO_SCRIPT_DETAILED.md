# Script Video Demo Detail MermaidGenerate

Bahasa: Indonesia  
Target durasi: 15 sampai 20 menit  
Tujuan: membuktikan notebook, dataset, inference, upload dataset, dan fine-tuning bekerja untuk kebutuhan tugas akhir mata kuliah.

## Step 1 - Opening

Estimasi waktu: 30 detik

Yang ditampilkan di layar:

- Judul repository atau README.
- Nama proyek MermaidGenerate.

Aksi:

- Buka repository atau folder proyek.

Narasi:

"Halo, pada video ini saya mendemonstrasikan proyek MermaidGenerate, yaitu aplikasi AI lokal untuk membuat diagram Mermaid berbentuk Mind Map dan Venn Diagram. Proyek ini berjalan melalui Google Colab dan Gradio, menggunakan Transformers, PyTorch, dan PEFT untuk inference serta fine-tuning. Fitur utama yang akan saya tunjukkan adalah inference diagram, upload dan validasi dataset, serta fine-tuning LoRA dari browser."

Expected result:

- Penonton memahami nama, tujuan, dan scope proyek.

Jika error:

- Jika repository belum terbuka, buka folder proyek atau halaman GitHub terlebih dahulu.

## Step 2 - Jelaskan Kebutuhan Tugas

Estimasi waktu: 30 detik

Yang ditampilkan di layar:

- README bagian assignment checklist atau `SUBMISSION_README.md`.

Aksi:

- Scroll ke mapping kebutuhan dosen.

Narasi:

"Kebutuhan dosen ada tiga. Pertama, notebook harus berisi inference, upload dataset, dan training atau fine-tuning. Kedua, harus ada dataset yang bervariasi. Ketiga, harus ada video demonstrasi bahwa aplikasi bekerja. Di proyek ini notebook utama adalah `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`, dataset utama berisi 1000 contoh seimbang, dan video ini menjadi bukti demonstrasi aplikasi."

Expected result:

- Kebutuhan dosen terlihat jelas.

Jika error:

- Jika README tidak terbuka, buka `SUBMISSION_README.md`.

## Step 3 - Tampilkan Struktur Repository

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- File explorer atau tree repository.

Aksi:

- Tunjukkan file dan folder penting.

Narasi:

"Struktur proyek terdiri dari notebook utama, `app.py` sebagai aplikasi Gradio, folder `src/mermaid_generate` untuk logic aplikasi, folder `datasets` untuk data training dan evaluasi, folder `scripts` untuk build dataset, validasi, evaluasi, dan packaging, folder `configs` untuk konfigurasi LoRA, serta folder `docs` untuk dokumentasi final dan script video."

Expected result:

- Penonton melihat semua komponen submission.

Jika error:

- Jika file explorer sulit dibaca, zoom in browser atau terminal.

## Step 4 - Tampilkan Notebook Utama

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`.

Aksi:

- Buka notebook di Google Colab.

Narasi:

"Notebook ini adalah deliverable utama. Di dalamnya ada setup environment, import library, GPU check, dataset upload dan validation, Mermaid validation dan preview, model loading, inference, fine-tuning mode LoRA, QLoRA, Full Fine-Tuning, Gradio web app, troubleshooting, dan submission guide. Jadi notebook ini memenuhi syarat inference, upload dataset, dan training."

Expected result:

- Notebook terbuka di Colab.

Jika error:

- Jika notebook tidak terbuka, upload file `.ipynb` ke Colab atau buka dari GitHub.

## Step 5 - Set Runtime GPU

Estimasi waktu: 30 detik

Yang ditampilkan di layar:

- Menu Colab runtime.

Aksi:

- Klik **Runtime > Change runtime type > GPU**.

Narasi:

"Untuk inference dan terutama fine-tuning, saya memilih runtime GPU. CPU masih bisa dipakai untuk validasi dataset, tetapi training LoRA atau QLoRA akan jauh lebih praktis dengan GPU."

Expected result:

- Runtime GPU aktif.

Jika error:

- Jika GPU tidak tersedia, jelaskan bahwa training tidak dijalankan dan gunakan validasi dataset serta inference ringan saja.

## Step 6 - Install Dependencies

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Cell install dependencies.

Aksi:

- Jalankan cell install.

Narasi:

"Cell ini menginstal dependency utama, yaitu PyTorch, Transformers, Datasets, PEFT, Accelerate, bitsandbytes jika kompatibel, dan Gradio. Dependency ini dibutuhkan karena runtime utama proyek adalah Transformers dan PyTorch, bukan paid API."

Expected result:

- Install selesai tanpa error kritis.

Jika error:

- Jika ada konflik dependency, restart runtime lalu jalankan lagi cell import.
- Jika bitsandbytes gagal, tetap bisa memakai LoRA biasa dan hindari QLoRA.

## Step 7 - GPU Check dan Import

Estimasi waktu: 45 detik

Yang ditampilkan di layar:

- Cell GPU check.

Aksi:

- Jalankan cell GPU check dan import.

Narasi:

"Cell ini mengecek apakah CUDA tersedia, nama GPU, dan versi PyTorch. Informasi ini penting agar training dijelaskan secara jujur. Jika GPU tidak tersedia, saya tidak akan mengklaim training GPU berhasil."

Expected result:

- Muncul `CUDA available: True` jika GPU tersedia.

Jika error:

- Jika CUDA false, gunakan mode validasi dan demo UI tanpa menjalankan training berat.

## Step 8 - Launch Gradio App

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Cell launch Gradio dan link `gradio.live`.

Aksi:

- Jalankan cell Gradio.
- Klik link publik `https://xxxxx.gradio.live`.

Narasi:

"Di Google Colab, aplikasi berjalan di server Colab, sehingga saya membuka link `gradio.live`. Jangan membuka `0.0.0.0:7860` di browser karena itu hanya alamat bind server. Kalau dijalankan di laptop lokal, perintahnya adalah `python app.py --local` dan browser membuka `http://127.0.0.1:7860`."

Expected result:

- UI Gradio terbuka.

Jika error:

- Jika link tidak muncul, jalankan ulang cell launch.
- Jika port sibuk, restart runtime atau gunakan port berbeda.

## Step 9 - Jelaskan Tab Generator Mermaid

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Tab **Generator Mermaid**.

Aksi:

- Tunjukkan active model/adaptor status, diagram type, prompt, parameter generation, code output, preview, validation status.

Narasi:

"Tab Generator Mermaid adalah bagian inference. Di sini pengguna memilih tipe diagram, memasukkan prompt, mengatur parameter generation, lalu menekan Generate. Output utama adalah final valid Mermaid code dan rendered preview. Raw model output disembunyikan di advanced debug supaya output mentah yang invalid tidak membingungkan pengguna."

Expected result:

- Komponen generator terlihat.

Jika error:

- Jika UI belum memuat, refresh halaman Gradio.

## Step 10 - Demo Mind Map

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Prompt textbox dan preview.

Aksi:

- Pilih **Mind Map**.
- Ketik:

```text
Buat mind map tentang strategi belajar AI untuk mahasiswa informatika.
```

- Klik **Generate**.

Narasi:

"Saya membuat Mind Map tentang strategi belajar AI. Aplikasi akan menghasilkan kode Mermaid yang dimulai dengan `mindmap`, melakukan validasi, lalu merender diagram visual. Jika raw output model kurang rapi, sistem melakukan repair fallback agar syntax tetap valid."

Expected result:

- Final code dimulai dengan `mindmap`.
- Preview menampilkan diagram Mind Map.
- Validation status valid.

Jika error:

- Jika inference gagal karena model belum dimuat, jalankan cell model loading.
- Jika preview tidak muncul, cek validation status dan reload Gradio.

## Step 11 - Demo Venn Diagram

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Prompt textbox, Mermaid code, dan preview.

Aksi:

- Pilih **Venn Diagram**.
- Ketik:

```text
Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.
```

- Klik **Generate**.

Narasi:

"Sekarang saya membuat Venn Diagram. Output assignment-facing dimulai dengan `venn`. Untuk renderer Mermaid, aplikasi mengubahnya secara internal menjadi `venn-beta`. Set A, B, dan C didefinisikan terlebih dahulu, lalu union hanya mereferensikan set yang sudah ada. Ini mencegah error undefined union."

Expected result:

- Final code dimulai dengan `venn`.
- Preview menampilkan Venn Diagram.
- Tidak ada error undefined set.

Jika error:

- Jika muncul error Venn, gunakan prompt yang lebih jelas dan cek raw debug.
- Jika renderer bermasalah, jelaskan bahwa preview memakai Mermaid `venn-beta`.

## Step 12 - Jelaskan Repair/Fallback Mechanism

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Validation status dan advanced debug.

Aksi:

- Buka accordion raw output jika perlu.

Narasi:

"Karena model kecil atau LoRA singkat masih bisa mengeluarkan teks mentah yang tidak valid, aplikasi tidak langsung mengirim raw output ke renderer. Alurnya adalah raw model output, extraction, repair atau compile fallback, validation, conversion untuk renderer, lalu preview. Jadi keberhasilan demo ditentukan oleh final valid Mermaid code dan rendered diagram."

Expected result:

- Penonton memahami kenapa fallback bukan fake output, tetapi syntax-safety guard.

Jika error:

- Jika fallback digunakan, jelaskan bahwa raw model output tidak sempurna tetapi final code tetap valid.

## Step 13 - Tampilkan Dataset & Fine-Tuning Tab

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Tab **Dataset & Fine-Tuning**.

Aksi:

- Klik tab Dataset & Fine-Tuning.

Narasi:

"Tab kedua adalah Dataset & Fine-Tuning. Di sini pengguna bisa upload dataset JSON atau JSONL, memvalidasi format, melihat preview data, diagram distribution, source format distribution, lalu menjalankan fine-tuning dari browser."

Expected result:

- Tab dataset terlihat lengkap.

Jika error:

- Jika tab tidak berpindah, refresh halaman Gradio.

## Step 14 - Upload Dataset

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- File upload component.

Aksi:

- Upload salah satu:

```text
datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl
```

atau untuk smoke test cepat:

```text
datasets/curated/mixed_mindmap_venn_curated.jsonl
```

Narasi:

"Dataset utama yang dikumpulkan adalah 1000 contoh, tetapi untuk demo training agar lebih cepat saya dapat memakai dataset 500 atau curated 150. Dataset mixed dipakai karena proyek harus menangani dua jenis diagram, Mind Map dan Venn, secara seimbang."

Expected result:

- File dataset ter-upload.

Jika error:

- Jika upload gagal, pastikan file berekstensi `.jsonl` atau `.json`.

## Step 15 - Validate Dataset

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Validation summary, preview table, distributions.

Aksi:

- Klik **Validate Dataset**.

Narasi:

"Validasi dataset mengecek format, prompt kosong, target kosong, prefix `mindmap` atau `venn`, markdown fence, duplicate, diagram type distribution, dan kesiapan training. Dataset expanded sudah divalidasi dengan invalid 0 dan duplicate 0."

Expected result:

- Untuk dataset 500: total 500, valid 500, invalid 0, duplicate 0, Mind Map 250, Venn 250.
- Untuk dataset 150: total 150, valid 150, invalid 0, duplicate 0, Mind Map 75, Venn 75.

Jika error:

- Jika invalid rows muncul, jangan training; perbaiki dataset terlebih dahulu.

## Step 16 - Jelaskan Dataset Format

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Dataset preview table atau `docs/DATASET_SPECIFICATION.md`.

Aksi:

- Tunjukkan kolom prompt dan target.

Narasi:

"Dataset mendukung tiga format: messages, prompt-completion, dan instruction-output. Untuk dataset expanded, format utama adalah prompt-completion. Prompt berisi permintaan pengguna, completion berisi target Mermaid code yang valid. Ini dipakai untuk supervised fine-tuning agar model belajar pola output diagram."

Expected result:

- Penonton memahami bentuk dataset.

Jika error:

- Jika table terlalu lebar, zoom out atau gunakan dokumentasi dataset.

## Step 17 - Fine-Tuning Controls

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Fine-tuning controls.

Aksi:

- Pilih **LoRA**.
- Set:
  - epochs: 1
  - learning rate: 0.0002
  - batch size: 1
  - gradient accumulation: 4
  - max sequence length: 512
  - validation split: 0.1

Narasi:

"Untuk demo saya memilih LoRA karena paling praktis di Colab. LoRA melatih adapter kecil tanpa mengubah semua bobot model. QLoRA 4-bit juga tersedia jika CUDA dan bitsandbytes kompatibel. Full Fine-Tuning tersedia, tetapi jauh lebih berat dan bisa kehabisan GPU memory."

Expected result:

- Parameter training siap.

Jika error:

- Jika GPU memory terbatas, kurangi max sequence length atau jumlah sample.

## Step 18 - Start Fine-Tuning

Estimasi waktu: 1 sampai 3 menit untuk penjelasan, training bisa lebih lama.

Yang ditampilkan di layar:

- Start Fine-Tuning button, status, logs.

Aksi:

- Klik **Start Fine-Tuning** jika GPU tersedia.
- Klik **Refresh Status** berkala.

Narasi:

"Sekarang training dijalankan langsung dari browser UI. Progress, loss, log, dan result summary akan tampil di halaman ini. Tombol Cancel Training tersedia untuk menghentikan proses pada checkpoint aman."

Expected result:

- Status berubah menjadi training.
- Logs dan loss mulai muncul.

Jika error:

- Jika CUDA unavailable, jangan klaim training berhasil.
- Jika OOM, kurangi sample atau pakai dataset 150.

## Step 19 - Training Result

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Result summary.

Aksi:

- Setelah selesai, klik **Refresh Status**.

Narasi:

"Jika training selesai, status berubah menjadi completed. Result summary menampilkan mode training, output path, train loss, eval loss jika ada, dan message. Ini adalah log real dari training, bukan simulasi."

Expected result:

- Status completed.
- Train/eval loss terlihat jika training berhasil.

Jika error:

- Jika failed, tampilkan error dan jelaskan penyebabnya secara jujur.

## Step 20 - Adapter Activation dan ZIP Download

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Active adapter/model status dan download ZIP.

Aksi:

- Tunjukkan adapter path dan ZIP download component.

Narasi:

"Setelah LoRA atau QLoRA selesai, adapter disimpan di `outputs/adapters/<timestamp>/`, dibuat ZIP, lalu otomatis diaktifkan sebagai model aktif untuk inference. ZIP adapter bisa di-download dari UI, tetapi tidak dikomit ke Git karena termasuk output training."

Expected result:

- Active adapter status berubah.
- ZIP download terlihat.

Jika error:

- Jika ZIP tidak muncul, klik Refresh Status.
- Jika tetap tidak muncul, cek output path di result summary.

## Step 21 - Generate Setelah Adapter Aktif

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- Kembali ke Generator Mermaid.

Aksi:

- Generate ulang Mind Map dan Venn.

Narasi:

"Setelah adapter aktif, inference memakai adapter hasil training. Fallback repair tetap aktif sebagai pengaman syntax, karena model kecil dan training singkat belum menjamin output selalu sempurna."

Expected result:

- Diagram tetap valid dan preview tetap render.

Jika error:

- Jika raw output buruk, final fallback tetap menghasilkan Mermaid valid.

## Step 22 - Jelaskan Source Code

Estimasi waktu: 2 menit

Yang ditampilkan di layar:

- `app.py`
- `src/mermaid_generate/`
- `scripts/`
- `configs/`

Aksi:

- Scroll file penting atau buka `docs/SOURCE_CODE_WALKTHROUGH.md`.

Narasi:

"Secara teknis, `app.py` membangun UI Gradio dan callback. `dataset_loader.py` membaca JSON/JSONL dan menormalisasi format. `dataset_validator.py` membuat laporan validasi. `mermaid_validator.py` mengecek syntax Mind Map dan Venn. `diagram_repair.py` memperbaiki atau membuat fallback valid. `model_loader.py` memuat tokenizer dan model Transformers. `inference.py` menjalankan generation pipeline. `training.py` dan `training_manager.py` menjalankan LoRA, QLoRA, dan Full Fine-Tuning. `adapter_manager.py` mengaktifkan adapter dan membuat ZIP. Script di folder `scripts` dipakai untuk build dataset, validasi, evaluasi, dan packaging final."

Expected result:

- Penonton paham pembagian modul.

Jika error:

- Jika file terlalu panjang, gunakan walkthrough docs.

## Step 23 - Jelaskan Local vs Colab

Estimasi waktu: 45 detik

Yang ditampilkan di layar:

- README atau `docs/LOCAL_RUN_GUIDE.md`.

Aksi:

- Tunjukkan command lokal.

Narasi:

"Jika dijalankan di laptop sendiri, gunakan `python app.py --local` dan buka `http://127.0.0.1:7860`. Jika dijalankan di Colab, gunakan link `gradio.live` karena server berjalan di mesin Colab, bukan di laptop kita."

Expected result:

- Penonton memahami perbedaan URL.

Jika error:

- Jika lokal port sibuk, gunakan `python app.py --local --port 7861`.

## Step 24 - Jelaskan Limitasi

Estimasi waktu: 1 menit

Yang ditampilkan di layar:

- README limitation section.

Aksi:

- Scroll ke limitations.

Narasi:

"Limitasinya, kualitas model bergantung pada dataset, durasi training, dan kapasitas model. LoRA smoke training membuktikan pipeline, tetapi belum tentu membuat model sempurna. QLoRA membutuhkan CUDA dan bitsandbytes yang kompatibel. Full Fine-Tuning bisa membutuhkan GPU lebih besar. Venn memakai `venn-beta` secara internal untuk preview. llama.cpp atau GGUF hanya kompatibilitas masa depan, bukan runtime utama. Tidak ada paid API yang digunakan."

Expected result:

- Limitasi disampaikan jujur.

Jika error:

- Jika ada pertanyaan dosen, jawab berdasarkan log dan dokumentasi, bukan klaim yang belum diuji.

## Step 25 - Tampilkan Final Package

Estimasi waktu: 45 detik

Yang ditampilkan di layar:

- `dist/MermaidGenerate_Final_Submission.zip` atau script packaging.

Aksi:

- Jalankan atau tunjukkan:

```bash
python3 scripts/build_submission_package.py
python3 scripts/verify_submission_package.py
```

Narasi:

"Paket submission final dapat dibuat otomatis dengan script packaging. ZIP berisi notebook, dataset final, dataset demo, source code, dokumentasi, report, dan script video. ZIP tidak memasukkan checkpoint, adapter, atau model besar."

Expected result:

- Package verification PASS.

Jika error:

- Jika verify gagal, lihat file yang missing lalu rebuild package.

## Step 26 - Closing

Estimasi waktu: 30 detik

Yang ditampilkan di layar:

- Gradio app dengan diagram yang berhasil render atau README final.

Aksi:

- Tutup dengan summary.

Narasi:

"Kesimpulannya, MermaidGenerate memenuhi kebutuhan tugas: notebook berisi inference, upload dataset, dan fine-tuning; dataset sudah diperluas dan divalidasi; dan aplikasi bisa menghasilkan serta merender Mind Map dan Venn Diagram melalui Gradio. Proyek ini siap dikumpulkan bersama dataset dan video demo."

Expected result:

- Video selesai dengan bukti kerja aplikasi jelas.

Jika error:

- Jika waktu demo terbatas, fokus pada notebook, generator, dataset validation, dan LoRA UI.
