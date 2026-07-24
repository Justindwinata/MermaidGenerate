"""Verify the final MermaidGenerate submission ZIP package."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "MermaidGenerate_Final_Submission"
ZIP_PATH = ROOT / "dist" / f"{PACKAGE_NAME}.zip"

REQUIRED_MEMBERS = [
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
    "src/mermaid_generate/__init__.py",
    "scripts/build_submission_package.py",
    "scripts/verify_submission_package.py",
    "configs/lora_smoke_config.json",
    "README.md",
    "CHANGELOG.md",
    "SUBMISSION_README.md",
    "SUBMISSION_MANIFEST.md",
    "docs/FINAL_SUBMISSION_PACKAGE.md",
    "docs/FINAL_SUBMISSION_CHECKLIST.md",
    "docs/FINAL_DEMO_SCRIPT.md",
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
    ".safetensors",
    ".bin",
    ".pt",
    ".pth",
    ".gguf",
    ".pyc",
}


def strip_prefix(member: str) -> str:
    prefix = f"{PACKAGE_NAME}/"
    return member[len(prefix) :] if member.startswith(prefix) else member


def forbidden_reason(member: str) -> str | None:
    rel = Path(strip_prefix(member))
    if any(part in FORBIDDEN_PARTS for part in rel.parts):
        return "forbidden directory"
    if rel.suffix.lower() in FORBIDDEN_SUFFIXES:
        return "forbidden model/cache suffix"
    if rel.suffix.lower() == ".zip":
        return "nested ZIP file"
    return None


def main() -> int:
    if not ZIP_PATH.exists():
        print(f"FAIL: ZIP not found: {ZIP_PATH}")
        return 1
    if ZIP_PATH.stat().st_size == 0:
        print(f"FAIL: ZIP is empty: {ZIP_PATH}")
        return 1

    failures: list[str] = []
    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = archive.namelist()
        normalized = {strip_prefix(name) for name in names}

        for required in REQUIRED_MEMBERS:
            if required not in normalized:
                failures.append(f"Missing required file: {required}")

        for name in names:
            reason = forbidden_reason(name)
            if reason:
                failures.append(f"Forbidden member ({reason}): {name}")

    if failures:
        print("FAIL: submission package verification failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: submission package verification succeeded.")
    print(f"ZIP path: {ZIP_PATH.relative_to(ROOT)}")
    print(f"ZIP size: {ZIP_PATH.stat().st_size} bytes")
    print(f"Required files checked: {len(REQUIRED_MEMBERS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
