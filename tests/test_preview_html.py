from mermaid_generate.config import MERMAID_JS_VERSION
from mermaid_generate.mermaid_preview import build_mermaid_preview_html


def test_preview_html_includes_pinned_mermaid_and_code() -> None:
    html = build_mermaid_preview_html(
        'venn\n  set A["A"]\n  set B["B"]\n  union A,B\n    text "AB"'
    )

    assert f"mermaid@{MERMAID_JS_VERSION}" in html
    assert "venn-beta" in html
    assert "<script type=\"module\">" in html
