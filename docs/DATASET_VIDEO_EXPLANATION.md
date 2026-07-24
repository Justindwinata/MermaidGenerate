# Penjelasan Dataset untuk Video Demo MermaidGenerate

## Tujuan Dataset

Dataset digunakan untuk mengajarkan model agar menghasilkan Mermaid code untuk dua jenis diagram:

- Mind Map
- Venn Diagram

Semakin bervariasi prompt dan completion yang digunakan, semakin baik peluang model memahami pola permintaan pengguna dan format output Mermaid yang benar.

## Mengapa Ada Dataset 150, 500, dan 1000?

### Dataset 150

File:

```text
datasets/curated/mixed_mindmap_venn_curated.jsonl
```

Isi:

- 75 Mind Map
- 75 Venn Diagram
- total 150 contoh

Kegunaan:

- Smoke test cepat di Colab.
- Cocok untuk membuktikan upload dataset, validasi, dan LoRA training pipeline.
- Training lebih cepat, tetapi coverage lebih kecil.

Yang disampaikan di video:

"Dataset 150 digunakan untuk demo cepat jika waktu Colab terbatas. Dataset ini sudah valid dan seimbang, tetapi bukan dataset paling besar."

### Dataset 500

File:

```text
datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl
```

Isi:

- 250 Mind Map
- 250 Venn Diagram
- total 500 contoh

Kegunaan:

- Demo training yang lebih baik daripada 150, tetapi masih lebih praktis daripada 1000.
- Cocok untuk LoRA training jika waktu demo masih terbatas.

Yang disampaikan di video:

"Dataset 500 adalah pilihan demo training yang lebih seimbang antara kualitas dan waktu. Dataset ini berisi 250 Mind Map dan 250 Venn."

### Dataset 1000

File:

```text
datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl
```

Isi:

- 500 Mind Map
- 500 Venn Diagram
- total 1000 contoh

Kegunaan:

- Dataset utama untuk submission.
- Coverage paling besar dan paling bervariasi.
- Cocok untuk training lebih serius jika Colab runtime cukup.

Statement yang direkomendasikan:

"Dataset utama yang dikumpulkan adalah `mixed_mindmap_venn_expanded_1000.jsonl` karena berisi 1000 contoh seimbang, yaitu 500 Mind Map dan 500 Venn Diagram. Untuk demo training, dataset 500 dapat digunakan agar proses lebih cepat di Colab."

## Mengapa Menggunakan Mixed Dataset?

Proyek ini harus menangani dua tipe diagram. Jika dataset hanya berisi Mind Map, model dapat menjadi bias ke Mind Map. Jika dataset hanya berisi Venn, model dapat menjadi bias ke Venn.

Mixed dataset dipakai agar model belajar:

- kapan output harus dimulai dengan `mindmap`;
- kapan output harus dimulai dengan `venn`;
- bagaimana membuat hierarchy Mind Map;
- bagaimana membuat set dan union Venn;
- bagaimana membedakan permintaan hierarchical concept map dan comparison diagram.

Yang disampaikan di video:

"Dataset mixed dipakai agar model tidak hanya belajar satu diagram. Karena requirement aplikasi adalah Mind Map dan Venn, dataset dibuat seimbang."

## Mengapa Mind Map dan Venn Harus Balanced?

Balanced berarti jumlah Mind Map dan Venn dibuat mendekati 50/50.

Manfaat:

- Mengurangi bias model ke satu diagram.
- Membantu diagram type accuracy.
- Membuat fine-tuning lebih adil untuk dua target output.
- Memudahkan evaluasi karena jumlah prompt per diagram seimbang.

Distribusi final:

| Dataset | Mind Map | Venn | Total |
|---|---:|---:|---:|
| Curated mixed | 75 | 75 | 150 |
| Expanded mixed 500 | 250 | 250 | 500 |
| Expanded mixed 1000 | 500 | 500 | 1000 |

## Format Dataset

Dataset utama menggunakan format prompt-completion:

```json
{
  "prompt": "Buat mind map tentang strategi belajar AI.",
  "completion": "mindmap\n  root((Strategi Belajar AI))\n    Dasar AI\n      Machine Learning\n      Deep Learning"
}
```

Untuk Venn:

```json
{
  "prompt": "Buat diagram Venn tentang Instagram, TikTok, dan WhatsApp marketing.",
  "completion": "venn\n  set A[\"Instagram\"]\n  set B[\"TikTok\"]\n  set C[\"WhatsApp\"]\n  union A,B\n    text \"Interaksi Audiens\""
}
```

## Variasi Prompt

Dataset expanded berisi variasi:

- Bahasa Indonesia
- Bahasa Inggris
- prompt pendek
- prompt panjang
- gaya formal
- gaya casual
- prompt untuk mahasiswa
- prompt untuk presentasi
- prompt untuk UMKM
- prompt teknologi
- prompt AI/ML
- prompt cybersecurity
- prompt cloud/devops
- prompt business dan marketing

Contoh pola prompt Indonesia:

- "Buat mind map tentang ..."
- "Tolong buatkan diagram mindmap mengenai ..."
- "Gambarkan peta konsep untuk ..."
- "Buat diagram Venn tentang ..."
- "Bandingkan A, B, dan C dalam bentuk Venn ..."

Contoh pola prompt English:

- "Create a mind map about ..."
- "Generate a Mermaid mindmap for ..."
- "Create a Venn diagram comparing ..."
- "Compare A, B, and C using a Venn diagram ..."

Yang disampaikan di video:

"Prompt dibuat bervariasi supaya model tidak hanya menghafal satu gaya kalimat. Ini penting karena user bisa menulis permintaan dengan banyak gaya bahasa."

## Validasi Dataset

Dataset expanded sudah divalidasi dengan script:

```bash
python3 scripts/validate_expanded_dataset.py
```

Hasil final:

- invalid rows: 0
- warning rows: 0
- duplicate prompts: 0
- duplicate completions: 0
- Venn undefined union references: 0
- Mind Map missing root: 0

Report:

```text
results/dataset_quality/expanded_dataset_summary.json
results/dataset_quality/expanded_dataset_summary.md
```

Yang disampaikan di video:

"Sebelum training, dataset divalidasi agar tidak ada target kosong, syntax salah, markdown fence, duplicate, atau Venn union yang merujuk set tidak terdefinisi."

## Mengapa Evaluation Prompts Dipisah?

File:

```text
datasets/evaluation/final_eval_prompts_100.jsonl
```

Isi:

- 50 Mind Map prompts
- 50 Venn prompts
- tidak berisi completion training

Alasan dipisah:

- Prompt evaluasi digunakan untuk mengetes kemampuan model pada input yang tidak langsung dipakai sebagai target training.
- Evaluasi bisa dilakukan validator-only atau model-mode.
- Validator-only mengecek coverage prompt dan dataset syntax tanpa download model.
- Model-mode hanya boleh diklaim jika inference real dijalankan.

Yang disampaikan di video:

"Evaluation prompts dipisah dari dataset training agar evaluasi tidak hanya mengulang contoh training."

## Dataset yang Dikumpulkan

File utama yang dikumpulkan:

```text
datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl
```

File pendukung demo:

```text
datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl
datasets/curated/mixed_mindmap_venn_curated.jsonl
datasets/evaluation/final_eval_prompts_100.jsonl
```

Kalimat final untuk video:

"Dataset utama yang dikumpulkan adalah `mixed_mindmap_venn_expanded_1000.jsonl` karena berisi 1000 contoh seimbang, yaitu 500 Mind Map dan 500 Venn Diagram. Untuk demo training, dataset 500 dapat digunakan agar proses lebih cepat di Colab."

## Limitasi Dataset

- Dataset expanded meningkatkan coverage, tetapi tidak menjamin model selalu sempurna.
- Kualitas model tetap bergantung pada GPU, jumlah epoch, learning rate, dan kapasitas model.
- Fallback repair tetap digunakan untuk menjamin final syntax Mermaid valid.
- Dataset sebaiknya tetap direview manusia sebelum training serius.
