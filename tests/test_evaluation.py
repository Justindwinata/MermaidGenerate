from mermaid_generate.evaluation import evaluate_predictions, normalize_exact


def test_evaluate_predictions_metrics() -> None:
    references = [
        {
            "diagram_type": "mindmap",
            "target": "mindmap\n  root((AI))\n    Data",
        },
        {
            "diagram_type": "venn",
            "target": 'venn\n  set A["A"]\n  set B["B"]\n  union A,B["AB"]',
        },
    ]
    predictions = [
        "mindmap\n  root((AI))\n    Data",
        '```mermaid\nvenn\n  set A["A"]\n```',
    ]

    metrics = evaluate_predictions(references, predictions)

    assert metrics.total == 2
    assert metrics.diagram_type_accuracy == 1.0
    assert metrics.markdown_fence_violation_count == 1
    assert metrics.invalid_output_count == 1


def test_normalize_exact_collapses_spacing() -> None:
    assert normalize_exact("mindmap\n    root((AI))") == "mindmap\nroot((AI))"
