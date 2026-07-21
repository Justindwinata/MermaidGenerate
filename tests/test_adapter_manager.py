from pathlib import Path

from mermaid_generate.adapter_manager import ensure_adapter_zip


def test_ensure_adapter_zip_creates_archive(tmp_path: Path) -> None:
    adapter_dir = tmp_path / "adapter"
    adapter_dir.mkdir()
    (adapter_dir / "adapter_config.json").write_text("{}", encoding="utf-8")

    zip_path = ensure_adapter_zip(adapter_dir)

    assert zip_path.endswith(".zip")
    assert Path(zip_path).exists()
