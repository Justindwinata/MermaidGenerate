"""Gradio entry point for MermaidGenerate.

The full web UI is implemented in a later project step. This placeholder keeps
the project importable during the foundation commit.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MermaidGenerate local Gradio web UI."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface for the web app.",
    )
    parser.add_argument(
        "--port",
        default=7860,
        type=int,
        help="Port for the web app.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    print(
        "MermaidGenerate foundation is ready. "
        f"Future Gradio app will launch on {args.host}:{args.port}."
    )


if __name__ == "__main__":
    main()
