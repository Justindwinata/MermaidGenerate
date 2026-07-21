"""HTML preview generation for Mermaid diagrams in Gradio."""

from __future__ import annotations

import html
import json

from .config import MERMAID_JS_VERSION
from .mermaid_validator import validate_mermaid_code


def build_mermaid_preview_html(code: str, element_id: str = "mermaid-preview") -> str:
    result = validate_mermaid_code(code)
    safe_message = html.escape(result.message())
    if not result.valid:
        safe_code = html.escape(result.normalized_code or code)
        return f"""
<div class="mg-preview mg-preview-error">
  <div class="mg-preview-status">Render skipped: {safe_message}</div>
  <pre>{safe_code}</pre>
</div>
""".strip()

    renderer_code_json = json.dumps(result.renderer_code)
    element_id_json = json.dumps(element_id)
    escaped_code = html.escape(result.normalized_code)
    return f"""
<div class="mg-preview">
  <div id="{html.escape(element_id)}" class="mg-mermaid-canvas"></div>
  <details class="mg-render-details">
    <summary>Mermaid code used for preview</summary>
    <pre>{escaped_code}</pre>
  </details>
</div>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_JS_VERSION}/dist/mermaid.esm.min.mjs";
  mermaid.initialize({{ startOnLoad: false, securityLevel: "strict", theme: "default" }});
  const code = {renderer_code_json};
  const targetId = {element_id_json};
  const target = document.getElementById(targetId);
  try {{
    const renderId = targetId + "-" + Date.now();
    const result = await mermaid.render(renderId, code);
    target.innerHTML = result.svg;
    if (typeof result.bindFunctions === "function") {{
      result.bindFunctions(target);
    }}
  }} catch (error) {{
    target.innerHTML = `<div class="mg-preview-status">Render error: ${{error.message || String(error)}}</div>`;
  }}
</script>
""".strip()
