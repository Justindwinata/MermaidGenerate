import json
from collections import Counter
from pathlib import Path

from mermaid_generate.dataset_loader import load_and_normalize_dataset, load_raw_records
from mermaid_generate.mermaid_validator import validate_mermaid_code


ROOT_DIR = Path(__file__).resolve().parents[1]
EXPANDED_DIR = ROOT_DIR / "datasets" / "expanded"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def duplicate_count(values: list[str]) -> int:
    counts = Counter(values)
    return sum(count - 1 for count in counts.values() if count > 1)


def test_expanded_dataset_files_exist_with_expected_counts() -> None:
    expected_counts = {
        "mindmap_expanded.jsonl": 500,
        "venn_expanded.jsonl": 500,
        "mixed_mindmap_venn_expanded_500.jsonl": 500,
        "mixed_mindmap_venn_expanded_1000.jsonl": 1000,
    }

    for filename, expected_count in expected_counts.items():
        path = EXPANDED_DIR / filename
        assert path.exists()
        assert len(read_jsonl(path)) == expected_count


def test_mixed_expanded_datasets_are_balanced() -> None:
    for filename, expected_each in [
        ("mixed_mindmap_venn_expanded_500.jsonl", 250),
        ("mixed_mindmap_venn_expanded_1000.jsonl", 500),
    ]:
        samples = load_and_normalize_dataset(EXPANDED_DIR / filename)
        counts = Counter(sample["diagram_type"] for sample in samples)

        assert counts["mindmap"] == expected_each
        assert counts["venn"] == expected_each


def test_expanded_datasets_have_no_prompt_or_completion_duplicates() -> None:
    for filename in [
        "mindmap_expanded.jsonl",
        "venn_expanded.jsonl",
        "mixed_mindmap_venn_expanded_500.jsonl",
        "mixed_mindmap_venn_expanded_1000.jsonl",
    ]:
        records = load_raw_records(EXPANDED_DIR / filename)

        assert duplicate_count([record["prompt"].casefold() for record in records]) == 0
        assert duplicate_count([record["completion"] for record in records]) == 0


def test_expanded_completions_validate_as_mermaid() -> None:
    for filename in ["mindmap_expanded.jsonl", "venn_expanded.jsonl"]:
        samples = load_and_normalize_dataset(EXPANDED_DIR / filename)
        for sample in samples:
            result = validate_mermaid_code(sample["target"], sample["diagram_type"])
            assert result.valid, (filename, sample["id"], result.errors)


def test_venn_set_references_are_defined_and_mindmaps_have_root() -> None:
    venn_samples = load_and_normalize_dataset(EXPANDED_DIR / "venn_expanded.jsonl")
    for sample in venn_samples:
        result = validate_mermaid_code(sample["target"], "venn")
        assert result.valid
        assert "undefined set" not in " ".join(result.errors).lower()

    mindmap_samples = load_and_normalize_dataset(EXPANDED_DIR / "mindmap_expanded.jsonl")
    for sample in mindmap_samples:
        assert "root((" in sample["target"]
