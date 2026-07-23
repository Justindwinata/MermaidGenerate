"""Build deterministic expanded MermaidGenerate datasets."""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
EXPANDED_DIR = ROOT / "datasets" / "expanded"
EVAL_DIR = ROOT / "datasets" / "evaluation"
SEED = 20260723


@dataclass(frozen=True)
class MindmapTopic:
    slug: str
    title_id: str
    title_en: str
    domain: str
    branches_id: tuple[tuple[str, tuple[str, ...]], ...]
    branches_en: tuple[tuple[str, tuple[str, ...]], ...]


@dataclass(frozen=True)
class VennTopic:
    slug: str
    domain: str
    labels: tuple[str, str, str]
    overlaps: tuple[str, str, str, str]
    labels_id: tuple[str, str, str] | None = None
    overlaps_id: tuple[str, str, str, str] | None = None


MINDMAP_TOPICS: tuple[MindmapTopic, ...] = (
    MindmapTopic(
        "ai-learning",
        "Strategi Belajar AI",
        "AI Learning Strategy",
        "education",
        (
            ("Dasar AI", ("Machine Learning", "Deep Learning", "Data")),
            ("Praktik", ("Proyek Kecil", "Eksperimen Model", "Evaluasi")),
            ("Tools", ("Python", "Notebook", "Library AI")),
            ("Portofolio", ("Dokumentasi", "GitHub", "Presentasi")),
            ("Etika", ("Bias", "Privasi", "Transparansi")),
        ),
        (
            ("AI Basics", ("Machine Learning", "Deep Learning", "Data")),
            ("Practice", ("Small Projects", "Model Experiments", "Evaluation")),
            ("Tools", ("Python", "Notebooks", "AI Libraries")),
            ("Portfolio", ("Documentation", "GitHub", "Presentation")),
            ("Ethics", ("Bias", "Privacy", "Transparency")),
        ),
    ),
    MindmapTopic(
        "software-engineering",
        "Rekayasa Perangkat Lunak",
        "Software Engineering",
        "technology",
        (
            ("Analisis", ("Kebutuhan", "User Story", "Prioritas")),
            ("Desain", ("Arsitektur", "API", "Database")),
            ("Implementasi", ("Coding", "Review", "Version Control")),
            ("Pengujian", ("Unit Test", "Integrasi", "Regression")),
            ("Rilis", ("CI/CD", "Monitoring", "Rollback")),
        ),
        (
            ("Analysis", ("Requirements", "User Stories", "Priorities")),
            ("Design", ("Architecture", "APIs", "Database")),
            ("Implementation", ("Coding", "Review", "Version Control")),
            ("Testing", ("Unit Tests", "Integration", "Regression")),
            ("Release", ("CI/CD", "Monitoring", "Rollback")),
        ),
    ),
    MindmapTopic(
        "data-science",
        "Proyek Data Science",
        "Data Science Project",
        "data",
        (
            ("Data", ("Sumber", "Cleaning", "Label")),
            ("Analisis", ("EDA", "Statistik", "Visualisasi")),
            ("Model", ("Training", "Validasi", "Tuning")),
            ("Evaluasi", ("Akurasi", "Error", "Interpretasi")),
            ("Deployment", ("API", "Dashboard", "Monitoring")),
        ),
        (
            ("Data", ("Sources", "Cleaning", "Labels")),
            ("Analysis", ("EDA", "Statistics", "Visualization")),
            ("Model", ("Training", "Validation", "Tuning")),
            ("Evaluation", ("Accuracy", "Error", "Interpretation")),
            ("Deployment", ("API", "Dashboard", "Monitoring")),
        ),
    ),
    MindmapTopic(
        "digital-marketing",
        "Digital Marketing UMKM",
        "Small Business Digital Marketing",
        "business",
        (
            ("Channel", ("Instagram", "TikTok", "WhatsApp")),
            ("Konten", ("Edukasi", "Testimoni", "Promo")),
            ("Audiens", ("Segmentasi", "Persona", "Komunitas")),
            ("Metrik", ("Reach", "Engagement", "Konversi")),
            ("Optimasi", ("A/B Test", "Jadwal", "Retargeting")),
        ),
        (
            ("Channels", ("Instagram", "TikTok", "WhatsApp")),
            ("Content", ("Education", "Testimonials", "Promos")),
            ("Audience", ("Segmentation", "Personas", "Community")),
            ("Metrics", ("Reach", "Engagement", "Conversion")),
            ("Optimization", ("A/B Tests", "Schedule", "Retargeting")),
        ),
    ),
    MindmapTopic(
        "cybersecurity",
        "Dasar Cybersecurity",
        "Cybersecurity Fundamentals",
        "security",
        (
            ("Ancaman", ("Phishing", "Malware", "Social Engineering")),
            ("Proteksi", ("Password", "MFA", "Backup")),
            ("Jaringan", ("Firewall", "VPN", "Monitoring")),
            ("Respons", ("Deteksi", "Isolasi", "Pemulihan")),
            ("Kebijakan", ("Akses", "Audit", "Pelatihan")),
        ),
        (
            ("Threats", ("Phishing", "Malware", "Social Engineering")),
            ("Protection", ("Passwords", "MFA", "Backups")),
            ("Network", ("Firewall", "VPN", "Monitoring")),
            ("Response", ("Detection", "Isolation", "Recovery")),
            ("Policy", ("Access", "Audit", "Training")),
        ),
    ),
    MindmapTopic(
        "cloud-devops",
        "Cloud dan DevOps",
        "Cloud and DevOps",
        "technology",
        (
            ("Cloud", ("Compute", "Storage", "Network")),
            ("Container", ("Docker", "Image", "Registry")),
            ("CI/CD", ("Build", "Test", "Deploy")),
            ("Observability", ("Log", "Metric", "Tracing")),
            ("Reliability", ("Scaling", "Backup", "Incident")),
        ),
        (
            ("Cloud", ("Compute", "Storage", "Network")),
            ("Containers", ("Docker", "Images", "Registry")),
            ("CI/CD", ("Build", "Test", "Deploy")),
            ("Observability", ("Logs", "Metrics", "Tracing")),
            ("Reliability", ("Scaling", "Backups", "Incidents")),
        ),
    ),
    MindmapTopic(
        "final-project",
        "Perencanaan Tugas Akhir",
        "Final Project Planning",
        "academic",
        (
            ("Topik", ("Masalah", "Tujuan", "Batasan")),
            ("Metode", ("Studi Literatur", "Eksperimen", "Evaluasi")),
            ("Implementasi", ("Prototype", "Dataset", "Testing")),
            ("Dokumen", ("Bab", "Referensi", "Lampiran")),
            ("Presentasi", ("Demo", "Slide", "Tanya Jawab")),
        ),
        (
            ("Topic", ("Problem", "Objectives", "Scope")),
            ("Method", ("Literature Review", "Experiment", "Evaluation")),
            ("Implementation", ("Prototype", "Dataset", "Testing")),
            ("Document", ("Chapters", "References", "Appendix")),
            ("Presentation", ("Demo", "Slides", "Q&A")),
        ),
    ),
    MindmapTopic(
        "research-paper",
        "Rencana Paper Riset",
        "Research Paper Plan",
        "academic",
        (
            ("Pertanyaan", ("Gap", "Hipotesis", "Kontribusi")),
            ("Metode", ("Dataset", "Model", "Baseline")),
            ("Eksperimen", ("Setup", "Metric", "Ablation")),
            ("Analisis", ("Hasil", "Error", "Diskusi")),
            ("Publikasi", ("Format", "Review", "Revisi")),
        ),
        (
            ("Question", ("Gap", "Hypothesis", "Contribution")),
            ("Method", ("Dataset", "Model", "Baseline")),
            ("Experiments", ("Setup", "Metrics", "Ablation")),
            ("Analysis", ("Results", "Errors", "Discussion")),
            ("Publication", ("Format", "Review", "Revision")),
        ),
    ),
    MindmapTopic(
        "presentation",
        "Persiapan Presentasi Kelas",
        "Class Presentation Planning",
        "education",
        (
            ("Tujuan", ("Pesan Utama", "Audiens", "Durasi")),
            ("Materi", ("Pembuka", "Isi", "Penutup")),
            ("Visual", ("Slide", "Diagram", "Contoh")),
            ("Latihan", ("Timing", "Suara", "Transisi")),
            ("Evaluasi", ("Pertanyaan", "Feedback", "Perbaikan")),
        ),
        (
            ("Goals", ("Key Message", "Audience", "Duration")),
            ("Content", ("Opening", "Body", "Closing")),
            ("Visuals", ("Slides", "Diagrams", "Examples")),
            ("Practice", ("Timing", "Voice", "Transitions")),
            ("Evaluation", ("Questions", "Feedback", "Improvement")),
        ),
    ),
    MindmapTopic(
        "productivity",
        "Produktivitas Mahasiswa",
        "Student Productivity",
        "general",
        (
            ("Prioritas", ("Matriks Tugas", "Deadline", "Dampak")),
            ("Waktu", ("Pomodoro", "Jadwal", "Istirahat")),
            ("Fokus", ("Notifikasi", "Lingkungan", "Target")),
            ("Tools", ("Kalender", "Task Board", "Catatan")),
            ("Refleksi", ("Review", "Kebiasaan", "Perbaikan")),
        ),
        (
            ("Priorities", ("Task Matrix", "Deadlines", "Impact")),
            ("Time", ("Pomodoro", "Schedule", "Breaks")),
            ("Focus", ("Notifications", "Environment", "Goals")),
            ("Tools", ("Calendar", "Task Board", "Notes")),
            ("Reflection", ("Review", "Habits", "Improvement")),
        ),
    ),
)


VENN_TOPICS: tuple[VennTopic, ...] = (
    VennTopic("social-marketing", "business", ("Instagram", "TikTok", "WhatsApp"), ("Audience Engagement", "Customer Communication", "Short Content Sharing", "Digital Marketing"), ("Instagram", "TikTok", "WhatsApp"), ("Interaksi Audiens", "Komunikasi Pelanggan", "Konten Pendek", "Marketing Digital")),
    VennTopic("students-workers-entrepreneurs", "social", ("Students", "Workers", "Entrepreneurs"), ("Working Students", "Student Founders", "Side Business", "Career Growth"), ("Mahasiswa", "Pekerja", "Wirausaha"), ("Mahasiswa Bekerja", "Founder Muda", "Bisnis Sampingan", "Pengembangan Karier")),
    VennTopic("ai-ml-ds", "ai", ("AI", "Machine Learning", "Data Science"), ("Intelligent Models", "Data Driven AI", "Predictive Analytics", "Applied AI"), ("AI", "Machine Learning", "Data Science"), ("Model Cerdas", "AI Berbasis Data", "Analitik Prediktif", "AI Terapan")),
    VennTopic("python-js-java", "programming", ("Python", "JavaScript", "Java"), ("Web APIs", "Backend Services", "Enterprise Apps", "Full Stack Systems"), ("Python", "JavaScript", "Java"), ("API Web", "Layanan Backend", "Aplikasi Enterprise", "Sistem Full Stack")),
    VennTopic("aws-gcp-azure", "cloud", ("AWS", "Google Cloud", "Azure"), ("Cloud Infrastructure", "Data Platforms", "Enterprise Cloud", "Multi Cloud"), ("AWS", "Google Cloud", "Azure"), ("Infrastruktur Cloud", "Platform Data", "Cloud Enterprise", "Multi Cloud")),
    VennTopic("sql-nosql-graph", "data", ("SQL", "NoSQL", "Graph Database"), ("Flexible Queries", "Connected Records", "Schema Design", "Data Modeling"), ("SQL", "NoSQL", "Graph Database"), ("Query Fleksibel", "Relasi Data", "Desain Skema", "Pemodelan Data")),
    VennTopic("scrum-kanban-waterfall", "software", ("Scrum", "Kanban", "Waterfall"), ("Agile Delivery", "Visual Workflow", "Structured Planning", "Project Management"), ("Scrum", "Kanban", "Waterfall"), ("Delivery Agile", "Alur Visual", "Perencanaan Terstruktur", "Manajemen Proyek")),
    VennTopic("online-offline-hybrid", "education", ("Online Learning", "Offline Learning", "Hybrid Learning"), ("Guided Practice", "Flexible Access", "Blended Class", "Learning Experience"), ("Belajar Online", "Belajar Tatap Muka", "Belajar Hybrid"), ("Latihan Terarah", "Akses Fleksibel", "Kelas Campuran", "Pengalaman Belajar")),
    VennTopic("seo-ads-content", "marketing", ("SEO", "Paid Ads", "Content Marketing"), ("Landing Traffic", "Search Demand", "Audience Education", "Growth Strategy"), ("SEO", "Iklan Berbayar", "Content Marketing"), ("Trafik Landing", "Permintaan Pencarian", "Edukasi Audiens", "Strategi Growth")),
    VennTopic("figma-canva-powerpoint", "presentation", ("Figma", "Canva", "PowerPoint"), ("Design Templates", "Presentation Assets", "Slide Design", "Visual Communication"), ("Figma", "Canva", "PowerPoint"), ("Template Desain", "Aset Presentasi", "Desain Slide", "Komunikasi Visual")),
    VennTopic("leadership-communication-teamwork", "skills", ("Leadership", "Communication", "Teamwork"), ("Direction Sharing", "Team Alignment", "Collaboration", "Student Soft Skills"), ("Leadership", "Komunikasi", "Kerja Tim"), ("Arah Bersama", "Keselarasan Tim", "Kolaborasi", "Soft Skill Mahasiswa")),
    VennTopic("react-vue-svelte", "frontend", ("React", "Vue", "Svelte"), ("Component UI", "Reactive State", "Modern Frontend", "Web Apps"), ("React", "Vue", "Svelte"), ("Komponen UI", "State Reaktif", "Frontend Modern", "Aplikasi Web")),
    VennTopic("mobile-web-desktop", "software", ("Mobile App", "Web App", "Desktop App"), ("Responsive UX", "Local Features", "Cross Platform", "User Application"), ("Aplikasi Mobile", "Aplikasi Web", "Aplikasi Desktop"), ("UX Responsif", "Fitur Lokal", "Lintas Platform", "Aplikasi Pengguna")),
    VennTopic("prevention-exercise-nutrition", "health", ("Prevention", "Exercise", "Nutrition"), ("Healthy Habits", "Body Wellness", "Balanced Lifestyle", "Personal Health"), ("Pencegahan", "Olahraga", "Nutrisi"), ("Kebiasaan Sehat", "Kebugaran", "Gaya Hidup Seimbang", "Kesehatan Pribadi")),
    VennTopic("github-gitlab-bitbucket", "devops", ("GitHub", "GitLab", "Bitbucket"), ("Repository Hosting", "CI/CD Pipelines", "Team Workflow", "Version Control"), ("GitHub", "GitLab", "Bitbucket"), ("Hosting Repo", "Pipeline CI/CD", "Workflow Tim", "Version Control")),
)


PROMPT_PATTERNS_ID = (
    "Buat mind map tentang {topic}.",
    "Tolong buatkan diagram mindmap mengenai {topic}.",
    "Gambarkan peta konsep untuk {topic} dengan {branches} cabang utama.",
    "Susun mind map untuk presentasi tentang {topic}.",
    "Buat peta konsep sederhana untuk mahasiswa tentang {topic}.",
    "Buat mind map yang lebih detail mengenai {topic}.",
    "Saya butuh mindmap ringkas tentang {topic} untuk kelas informatika.",
    "Rancang peta konsep {topic} dengan istilah sederhana.",
)

PROMPT_PATTERNS_EN = (
    "Create a mind map about {topic}.",
    "Generate a Mermaid mindmap for {topic}.",
    "Build a concept map about {topic} with {branches} main branches.",
    "Create a concise mind map for a class presentation about {topic}.",
    "Make a beginner-friendly mind map about {topic}.",
    "Create a more detailed mind map about {topic}.",
    "Prepare a study mindmap for computer science students about {topic}.",
    "Design a structured concept map for {topic}.",
)

AUDIENCES_ID = (
    "mahasiswa baru",
    "mahasiswa informatika",
    "tim proyek",
    "presentasi kelas",
    "demo portofolio",
    "pemilik UMKM",
    "peneliti pemula",
    "mentor praktikum",
    "kelompok belajar",
    "final project",
)

AUDIENCES_EN = (
    "first-year students",
    "computer science students",
    "project teams",
    "class presentations",
    "portfolio demos",
    "small business owners",
    "beginner researchers",
    "lab mentors",
    "study groups",
    "final projects",
)

FOCUS_ID = (
    "pemahaman dasar",
    "praktik mandiri",
    "diskusi kelas",
    "demo aplikasi",
    "rencana belajar",
    "evaluasi mingguan",
    "presentasi singkat",
    "studi kasus",
    "portofolio",
    "kolaborasi tim",
    "riset kecil",
    "pengambilan keputusan",
    "optimasi proses",
    "monitoring hasil",
    "perencanaan tugas",
    "strategi implementasi",
    "analisis kebutuhan",
    "validasi ide",
    "dokumentasi proyek",
    "persiapan demo",
)

FOCUS_EN = (
    "basic understanding",
    "independent practice",
    "class discussion",
    "application demo",
    "study planning",
    "weekly evaluation",
    "short presentation",
    "case study",
    "portfolio work",
    "team collaboration",
    "small research",
    "decision making",
    "process optimization",
    "result monitoring",
    "assignment planning",
    "implementation strategy",
    "requirements analysis",
    "idea validation",
    "project documentation",
    "demo preparation",
)

VENN_PROMPTS_ID = (
    "Buat diagram Venn tentang {items}.",
    "Saya ingin diagram Venn yang membandingkan {items}.",
    "Buat diagram Venn tentang persamaan dan perbedaan {items}.",
    "Bandingkan {items} dalam bentuk Venn.",
    "Susun Mermaid Venn dengan label ringkas untuk {items}.",
    "Buat Venn sederhana untuk presentasi tentang {items}.",
)

VENN_PROMPTS_EN = (
    "Create a Venn diagram comparing {items}.",
    "Compare {items} using a Venn diagram.",
    "Make a Mermaid Venn diagram about {items}.",
    "Create concise overlap labels for {items} in a Venn diagram.",
    "Build a simple Venn diagram for a presentation about {items}.",
    "Generate a Venn comparison of {items}.",
)


def stable_id(prefix: str, prompt: str, completion: str) -> str:
    digest = hashlib.sha1(f"{prompt}\n{completion}".encode("utf-8")).hexdigest()[:14]
    return f"{prefix}-{digest}"


def write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def mindmap_code(topic: MindmapTopic, language: str, variant: int) -> str:
    title = topic.title_id if language == "id" else topic.title_en
    branches = topic.branches_id if language == "id" else topic.branches_en
    audiences = AUDIENCES_ID if language == "id" else AUDIENCES_EN
    focus_terms = FOCUS_ID if language == "id" else FOCUS_EN
    audience = audiences[(variant // len(MINDMAP_TOPICS)) % len(audiences)]
    focus = focus_terms[(variant // (len(MINDMAP_TOPICS) * 2)) % len(focus_terms)]
    branch_count = 3 + (variant % 3)
    rotated = branches[variant % len(branches) :] + branches[: variant % len(branches)]
    selected = rotated[:branch_count]
    lines = ["mindmap", f"  root(({title}))"]
    for branch_index, (branch, children) in enumerate(selected):
        lines.append(f"    {branch}")
        child_offset = (variant + branch_index) % len(children)
        rotated_children = children[child_offset:] + children[:child_offset]
        child_count = 2 + ((variant + branch_index) % 2)
        for child in rotated_children[:child_count]:
            lines.append(f"      {child}")
        if variant % 5 == 0 and branch_index == 0 and len(children) >= 3:
            detail = "Contoh" if language == "id" else "Example"
            lines.append(f"        {detail}")
    context_branch = "Konteks" if language == "id" else "Context"
    focus_label = "Fokus" if language == "id" else "Focus"
    audience_label = "Audiens" if language == "id" else "Audience"
    lines.extend(
        [
            f"    {context_branch}",
            f"      {audience_label} {audience.title()}",
            f"      {focus_label} {focus.title()}",
        ]
    )
    return "\n".join(lines)


def mindmap_prompt(topic: MindmapTopic, language: str, variant: int) -> str:
    branches = 3 + (variant % 3)
    patterns = PROMPT_PATTERNS_ID if language == "id" else PROMPT_PATTERNS_EN
    selected_topic = topic.title_id if language == "id" else topic.title_en
    prompt = patterns[variant % len(patterns)].format(topic=selected_topic, branches=branches)
    audiences = AUDIENCES_ID if language == "id" else AUDIENCES_EN
    audience = audiences[(variant // len(MINDMAP_TOPICS)) % len(audiences)]
    focus_terms = FOCUS_ID if language == "id" else FOCUS_EN
    focus = focus_terms[(variant // (len(MINDMAP_TOPICS) * 2)) % len(focus_terms)]
    prompt += f" Untuk {audience}." if language == "id" else f" For {audience}."
    prompt += f" Fokus pada {focus}." if language == "id" else f" Focus on {focus}."
    if variant % 7 == 0:
        prompt += " Gunakan struktur ringkas." if language == "id" else " Use concise labels."
    if variant % 11 == 0:
        prompt += " Buat untuk demo tugas akhir." if language == "id" else " Make it suitable for a final project demo."
    return prompt


def build_mindmap_rows(count: int = 500) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen_prompts: set[str] = set()
    seen_completions: set[str] = set()
    for variant in range(count * 20):
        topic = MINDMAP_TOPICS[variant % len(MINDMAP_TOPICS)]
        language = "id" if variant % 2 == 0 else "en"
        prompt = mindmap_prompt(topic, language, variant)
        completion = mindmap_code(topic, language, variant)
        prompt_key = prompt.casefold()
        if prompt_key not in seen_prompts and completion not in seen_completions:
            seen_prompts.add(prompt_key)
            seen_completions.add(completion)
            rows.append(
                {
                    "id": stable_id("mindmap", prompt, completion),
                    "prompt": prompt,
                    "completion": completion,
                    "language": language,
                    "domain": topic.domain,
                    "complexity": ("simple", "medium", "complex")[variant % 3],
                }
            )
        if len(rows) == count:
            return rows
    raise RuntimeError(f"Could only build {len(rows)} unique Mind Map rows.")
    return rows


def venn_code(topic: VennTopic, language: str, variant: int) -> str:
    labels = topic.labels_id if language == "id" and topic.labels_id else topic.labels
    overlaps = topic.overlaps_id if language == "id" and topic.overlaps_id else topic.overlaps
    audiences = AUDIENCES_ID if language == "id" else AUDIENCES_EN
    focus_terms = FOCUS_ID if language == "id" else FOCUS_EN
    audience = audiences[(variant // len(VENN_TOPICS)) % len(audiences)].title()
    focus = focus_terms[(variant // (len(VENN_TOPICS) * 2)) % len(focus_terms)].title()
    overlap_offset = variant % len(overlaps)
    overlaps = overlaps[overlap_offset:] + overlaps[:overlap_offset]
    use_three_sets = variant % 4 != 0
    lines = ["venn", f'  set A["{labels[0]}"]', f'  set B["{labels[1]}"]']
    if use_three_sets:
        lines.append(f'  set C["{labels[2]}"]')
    lines.extend(["  union A,B", f'    text "{overlaps[0]} for {focus}"'])
    if use_three_sets:
        lines.extend(
            [
                "  union A,C",
                f'    text "{overlaps[1]} for {audience}"',
                "  union B,C",
                f'    text "{overlaps[2]} for {focus}"',
                "  union A,B,C",
                f'    text "{overlaps[3]} for {audience}"',
            ]
        )
    return "\n".join(lines)


def venn_prompt(topic: VennTopic, language: str, variant: int) -> str:
    labels = topic.labels_id if language == "id" and topic.labels_id else topic.labels
    selected = labels if variant % 4 != 0 else labels[:2]
    joiner = ", ".join(selected[:-1]) + (", dan " if language == "id" else ", and ") + selected[-1]
    patterns = VENN_PROMPTS_ID if language == "id" else VENN_PROMPTS_EN
    prompt = patterns[variant % len(patterns)].format(items=joiner)
    audiences = AUDIENCES_ID if language == "id" else AUDIENCES_EN
    audience = audiences[(variant // len(VENN_TOPICS)) % len(audiences)]
    focus_terms = FOCUS_ID if language == "id" else FOCUS_EN
    focus = focus_terms[(variant // (len(VENN_TOPICS) * 2)) % len(focus_terms)]
    prompt += f" Untuk {audience}." if language == "id" else f" For {audience}."
    prompt += f" Fokus pada {focus}." if language == "id" else f" Focus on {focus}."
    if variant % 9 == 0:
        prompt += " Gunakan label overlap singkat." if language == "id" else " Use concise overlap labels."
    if variant % 13 == 0:
        prompt += " Cocok untuk presentasi kelas." if language == "id" else " Make it suitable for a class presentation."
    return prompt


def build_venn_rows(count: int = 500) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen_prompts: set[str] = set()
    seen_completions: set[str] = set()
    for variant in range(count * 20):
        topic = VENN_TOPICS[variant % len(VENN_TOPICS)]
        language = "id" if variant % 2 == 0 else "en"
        prompt = venn_prompt(topic, language, variant)
        completion = venn_code(topic, language, variant)
        prompt_key = prompt.casefold()
        if prompt_key not in seen_prompts and completion not in seen_completions:
            seen_prompts.add(prompt_key)
            seen_completions.add(completion)
            rows.append(
                {
                    "id": stable_id("venn", prompt, completion),
                    "prompt": prompt,
                    "completion": completion,
                    "language": language,
                    "domain": topic.domain,
                    "complexity": ("simple", "medium", "complex")[variant % 3],
                }
            )
        if len(rows) == count:
            return rows
    raise RuntimeError(f"Could only build {len(rows)} unique Venn rows.")
    return rows


def interleave(left: list[dict[str, object]], right: list[dict[str, object]], total: int) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    each = total // 2
    for index in range(each):
        output.append(left[index])
        output.append(right[index])
    return output[:total]


def build_eval_prompts(mindmaps: list[dict[str, object]], venns: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, row in enumerate(mindmaps[:50]):
        rows.append(
            {
                "id": f"eval-mindmap-{index + 1:03d}",
                "diagram_type": "mindmap",
                "prompt": row["prompt"],
                "language": row["language"],
                "domain": row["domain"],
                "complexity": row["complexity"],
            }
        )
    for index, row in enumerate(venns[:50]):
        rows.append(
            {
                "id": f"eval-venn-{index + 1:03d}",
                "diagram_type": "venn",
                "prompt": row["prompt"],
                "language": row["language"],
                "domain": row["domain"],
                "complexity": row["complexity"],
            }
        )
    return rows


def main() -> None:
    random.seed(SEED)
    EXPANDED_DIR.mkdir(parents=True, exist_ok=True)
    EVAL_DIR.mkdir(parents=True, exist_ok=True)

    mindmaps = build_mindmap_rows(500)
    venns = build_venn_rows(500)
    mixed_500 = interleave(mindmaps, venns, 500)
    mixed_1000 = interleave(mindmaps, venns, 1000)
    eval_prompts = build_eval_prompts(mindmaps, venns)

    write_jsonl(EXPANDED_DIR / "mindmap_expanded.jsonl", mindmaps)
    write_jsonl(EXPANDED_DIR / "venn_expanded.jsonl", venns)
    write_jsonl(EXPANDED_DIR / "mixed_mindmap_venn_expanded_500.jsonl", mixed_500)
    write_jsonl(EXPANDED_DIR / "mixed_mindmap_venn_expanded_1000.jsonl", mixed_1000)
    write_jsonl(EVAL_DIR / "final_eval_prompts_100.jsonl", eval_prompts)

    print("Generated expanded datasets:")
    for path in [
        EXPANDED_DIR / "mindmap_expanded.jsonl",
        EXPANDED_DIR / "venn_expanded.jsonl",
        EXPANDED_DIR / "mixed_mindmap_venn_expanded_500.jsonl",
        EXPANDED_DIR / "mixed_mindmap_venn_expanded_1000.jsonl",
        EVAL_DIR / "final_eval_prompts_100.jsonl",
    ]:
        print(f"- {path.relative_to(ROOT)}: {sum(1 for _ in path.open(encoding='utf-8'))} rows")


if __name__ == "__main__":
    main()
