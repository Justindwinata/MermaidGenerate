"""Build the final MermaidGenerate lecturer submission ZIP package."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
PACKAGE_NAME = "MermaidGenerate_Final_Submission"
STAGING_DIR = DIST_DIR / PACKAGE_NAME
ZIP_PATH = DIST_DIR / f"{PACKAGE_NAME}.zip"
REPO_URL = "https://github.com/Justindwinata/MermaidGenerate"

REQUIRED_FILES = [
    "MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb",
    "datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl",
    "datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl",
    "datasets/curated/mixed_mindmap_venn_curated.jsonl",
    "datasets/evaluation/final_eval_prompts_100.jsonl",
    "docs/VIDEO_DEMO_SCRIPT_DETAILED.md",
    "docs/VIDEO_DEMO_CHECKLIST.md",
    "docs/VIDEO_DEMO_NARRATION_SHORT.md",
    "docs/VIDEO_DEMO_NARRATION_FULL.md",
    "docs/NOTEBOOK_CELL_WALKTHROUGH.md",
    "docs/SOURCE_CODE_WALKTHROUGH.md",
    "docs/DATASET_VIDEO_EXPLANATION.md",
    "app.py",
    "requirements.txt",
    "README.md",
    "CHANGELOG.md",
    "SUBMISSION_README.md",
    "SUBMISSION_MANIFEST.md",
    "docs/FINAL_SUBMISSION_PACKAGE.md",
    "docs/FINAL_SUBMISSION_CHECKLIST.md",
    "docs/FINAL_DEMO_SCRIPT.md",
    "docs/SUBMISSION_GUIDE.md",
    "docs/DATASET_SPECIFICATION.md",
    "docs/DATASET_USAGE_GUIDE.md",
    "docs/DATASET_EXPANSION_REPORT.md",
    "docs/TRAINING_GUIDE.md",
    "docs/LOCAL_RUN_GUIDE.md",
    "docs/TROUBLESHOOTING.md",
    "docs/FINAL_QA_AUDIT.md",
    "docs/FINAL_EVALUATION_GUIDE.md",
    "docs/SYSTEM_ARCHITECTURE.md",
    "docs/evidence/FINAL_EVIDENCE_SUMMARY.md",
    "results/dataset_quality/expanded_dataset_summary.json",
    "results/dataset_quality/expanded_dataset_summary.md",
    "results/evaluation/final_eval_baseline.json",
]

REQUIRED_DIRS = [
    "src/mermaid_generate",
    "scripts",
    "configs",
]

FORBIDDEN_PARTS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "outputs",
    "checkpoints",
    "adapters",
    "full_models",
}

FORBIDDEN_SUFFIXES = {
    ".zip",
    ".safetensors",
    ".bin",
    ".pt",
    ".pth",
    ".gguf",
    ".pyc",
}


def git_commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return "unknown"


def should_exclude(path: Path) -> bool:
    if any(part in FORBIDDEN_PARTS for part in path.parts):
        return True
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        return True
    return False


def copy_file(relative_path: str) -> None:
    source = ROOT / relative_path
    target = STAGING_DIR / relative_path
    if not source.exists():
        raise FileNotFoundError(f"Required file missing: {relative_path}")
    if should_exclude(Path(relative_path)):
        raise ValueError(f"Required file matches forbidden pattern: {relative_path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_dir(relative_path: str) -> None:
    source = ROOT / relative_path
    target = STAGING_DIR / relative_path
    if not source.exists():
        raise FileNotFoundError(f"Required directory missing: {relative_path}")
    for item in source.rglob("*"):
        rel = item.relative_to(ROOT)
        if should_exclude(rel):
            continue
        out = STAGING_DIR / rel
        if item.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, out)


def file_size(path: Path) -> str:
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} B"
        size /= 1024
    return f"{size:.1f} GB"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_generated_manifest() -> str:
    rows = []
    for path in sorted(item for item in STAGING_DIR.rglob("*") if item.is_file()):
        rel = path.relative_to(STAGING_DIR).as_posix()
        rows.append(f"| `{rel}` | {file_size(path)} | Included in final submission ZIP. |")

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    commit = git_commit_hash()
    return "\n".join(
        [
            "# MermaidGenerate Final Submission Manifest",
            "",
            f"Generated timestamp: `{generated_at}`",
            f"Git commit hash: `{commit}`",
            f"Repository URL: `{REPO_URL}`",
            "",
            "## Lecturer Requirement Mapping",
            "",
            "| Requirement | Included file(s) | Purpose | Status |",
            "|---|---|---|---|",
            "| Notebook with inference/upload/training | `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb` | Main Colab notebook | Included |",
            "| Dataset | `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl` | Final expanded dataset | Included |",
            "| Video demonstration | `docs/VIDEO_DEMO_SCRIPT_DETAILED.md` and narration/checklist docs | Guide for recording video | Included |",
            "| Source code | `app.py`, `src/mermaid_generate/`, `scripts/`, `configs/` | App, inference, validation, training, evaluation, packaging | Included |",
            "| Reports | `results/dataset_quality/`, `results/evaluation/` | Dataset quality and validator-only evaluation | Included |",
            "",
            "## Included Files",
            "",
            "| File | Size | Purpose |",
            "|---|---:|---|",
            *rows,
            "",
            "## Excluded Files",
            "",
            "The package excludes Git metadata, virtual environments, caches, model checkpoints, adapter outputs, generated adapter ZIPs, and large model weight formats.",
        ]
    ) + "\n"


def build_generated_readme() -> str:
    return "\n".join(
        [
            "# MermaidGenerate Final Submission Package",
            "",
            "This ZIP contains the notebook, datasets, source code, documentation, reports, and video demo scripts required for the final lecturer submission.",
            "",
            "Start with:",
            "",
            "1. `SUBMISSION_README.md`",
            "2. `MermaidGenerate_Mindmap_Venn_Finetuning_WebUI.ipynb`",
            "3. `docs/VIDEO_DEMO_SCRIPT_DETAILED.md`",
            "",
            "Main dataset:",
            "",
            "- `datasets/expanded/mixed_mindmap_venn_expanded_1000.jsonl`",
            "",
            "Demo dataset:",
            "",
            "- `datasets/expanded/mixed_mindmap_venn_expanded_500.jsonl`",
            "",
            "Quick smoke-test dataset:",
            "",
            "- `datasets/curated/mixed_mindmap_venn_curated.jsonl`",
            "",
            "No model checkpoints or adapter artifacts are included. Adapter ZIP files should be generated during the live demo if needed.",
        ]
    ) + "\n"


def create_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in sorted(STAGING_DIR.rglob("*")):
            if item.is_file():
                rel = item.relative_to(STAGING_DIR)
                if should_exclude(rel):
                    raise ValueError(f"Forbidden file reached ZIP stage: {rel}")
                archive.write(item, arcname=f"{PACKAGE_NAME}/{rel.as_posix()}")


def verify_staging_required_files() -> None:
    for relative_path in REQUIRED_FILES:
        target = STAGING_DIR / relative_path
        if not target.exists():
            raise FileNotFoundError(f"Required staged file missing: {relative_path}")
    for relative_path in REQUIRED_DIRS:
        target = STAGING_DIR / relative_path
        if not target.exists() or not any(target.rglob("*")):
            raise FileNotFoundError(f"Required staged directory missing or empty: {relative_path}")


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)

    for relative_path in REQUIRED_FILES:
        copy_file(relative_path)
    for relative_path in REQUIRED_DIRS:
        copy_dir(relative_path)

    (STAGING_DIR / "SUBMISSION_MANIFEST.md").write_text(build_generated_manifest(), encoding="utf-8")
    (STAGING_DIR / "SUBMISSION_README.md").write_text(build_generated_readme(), encoding="utf-8")

    verify_staging_required_files()
    create_zip()
    if not ZIP_PATH.exists() or ZIP_PATH.stat().st_size == 0:
        raise RuntimeError("Submission ZIP was not created or is empty.")

    print("Submission package built successfully.")
    print(f"Staging folder: {STAGING_DIR.relative_to(ROOT)}")
    print(f"ZIP path: {ZIP_PATH.relative_to(ROOT)}")
    print(f"ZIP size: {file_size(ZIP_PATH)}")
    print(f"ZIP sha256: {sha256(ZIP_PATH)}")


if __name__ == "__main__":
    main()
