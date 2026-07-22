"""HTML preview generation for Mermaid diagrams in Gradio."""

from __future__ import annotations

import html
import json

from .config import MERMAID_JS_VERSION
from .mermaid_validator import validate_mermaid_code


def _preview_iframe_srcdoc(renderer_code: str, diagram_type: str | None) -> str:
    renderer_code_json = json.dumps(renderer_code)
    diagram_type_json = json.dumps(diagram_type or "mermaid")
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{
      color-scheme: light;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    body {{
      margin: 0;
      background: #ffffff;
      color: #0f172a;
    }}
    .wrap {{
      box-sizing: border-box;
      min-height: 500px;
      padding: 18px;
      overflow: auto;
    }}
    .status {{
      margin: 0 0 14px;
      color: #475569;
      font-size: 13px;
      font-weight: 600;
    }}
    .status.error {{
      color: #b42318;
    }}
    #diagram {{
      min-height: 420px;
      display: flex;
      align-items: flex-start;
      justify-content: center;
    }}
    #diagram svg {{
      max-width: 100%;
      height: auto;
    }}
    pre {{
      white-space: pre-wrap;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 12px;
      background: #f8fafc;
      color: #0f172a;
      font-size: 12px;
      line-height: 1.45;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div id="status" class="status">Rendering Mermaid diagram...</div>
    <div id="diagram" aria-label="Rendered Mermaid diagram"></div>
  </div>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_JS_VERSION}/dist/mermaid.esm.min.mjs";

    const code = {renderer_code_json};
    const diagramType = {diagram_type_json};
    const status = document.getElementById("status");
    const diagram = document.getElementById("diagram");

    mermaid.initialize({{
      startOnLoad: false,
      securityLevel: "strict",
      theme: "default"
    }});

    try {{
      const renderId = "mg-preview-" + Date.now().toString(36);
      const result = await mermaid.render(renderId, code);
      diagram.innerHTML = result.svg;
      if (typeof result.bindFunctions === "function") {{
        result.bindFunctions(diagram);
      }}
      status.textContent = "Rendered " + diagramType + " diagram.";
    }} catch (error) {{
      const message = error && error.message ? error.message : String(error);
      status.textContent = "Render error: " + message;
      status.classList.add("error");
      const pre = document.createElement("pre");
      pre.textContent = code;
      diagram.replaceChildren(pre);
    }}
  </script>
</body>
</html>"""


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

    iframe_srcdoc = html.escape(
        _preview_iframe_srcdoc(result.renderer_code, result.diagram_type),
        quote=True,
    )
    escaped_id = html.escape(element_id)
    escaped_code = html.escape(result.normalized_code)
    escaped_renderer_code = html.escape(result.renderer_code)
    return f"""
<div class="mg-preview">
  <iframe
    id="{escaped_id}"
    class="mg-preview-frame"
    title="Rendered Mermaid preview"
    sandbox="allow-scripts"
    loading="lazy"
    srcdoc="{iframe_srcdoc}"
    style="width: 100%; min-height: 560px; border: 1px solid #d8dee8; border-radius: 8px; background: #ffffff;"
  ></iframe>
  <details class="mg-render-details">
    <summary>Final Mermaid code</summary>
    <pre>{escaped_code}</pre>
  </details>
  <details class="mg-render-details">
    <summary>Renderer-facing Mermaid code</summary>
    <pre>{escaped_renderer_code}</pre>
  </details>
</div>
""".strip()
