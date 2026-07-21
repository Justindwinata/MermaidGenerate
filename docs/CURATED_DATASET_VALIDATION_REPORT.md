# Curated Dataset Validation Report

Validation date: 2026-07-22 Asia/Jakarta

Validator: `mermaid_generate.dataset_validator.validate_dataset_file`.

## `datasets/curated/mindmap_curated.jsonl`

- Total samples: 75
- Valid samples: 75
- Invalid samples: 0
- Warning samples: 0
- Diagram type distribution: `{'mindmap': 75}`
- Source format distribution: `{'prompt_completion': 75}`
- Language distribution: `{'id': 24, 'en': 51}`
- Domain distribution: `{'education': 15, 'business': 20, 'technology': 15, 'health': 10, 'social science': 10, 'general': 5}`
- Complexity distribution: `{'simple': 15, 'medium': 35, 'complex': 25}`
- Duplicate count: 0
- Train ready: True
- Error: `None`

## `datasets/curated/venn_curated.jsonl`

- Total samples: 75
- Valid samples: 75
- Invalid samples: 0
- Warning samples: 0
- Diagram type distribution: `{'venn': 75}`
- Source format distribution: `{'prompt_completion': 75}`
- Language distribution: `{'en': 40, 'id': 35}`
- Domain distribution: `{'education': 20, 'technology': 15, 'business': 15, 'health': 10, 'social science': 10, 'general': 5}`
- Complexity distribution: `{'medium': 50, 'complex': 15, 'simple': 10}`
- Duplicate count: 0
- Train ready: True
- Error: `None`

## `datasets/curated/mixed_mindmap_venn_curated.jsonl`

- Total samples: 150
- Valid samples: 150
- Invalid samples: 0
- Warning samples: 0
- Diagram type distribution: `{'mindmap': 75, 'venn': 75}`
- Source format distribution: `{'prompt_completion': 150}`
- Language distribution: `{'id': 59, 'en': 91}`
- Domain distribution: `{'education': 35, 'business': 35, 'technology': 30, 'health': 20, 'social science': 20, 'general': 10}`
- Complexity distribution: `{'simple': 25, 'medium': 85, 'complex': 40}`
- Duplicate count: 0
- Train ready: True
- Error: `None`

## Notes

- All curated datasets validate successfully with zero invalid samples.
- The mixed dataset is balanced: 75 Mind Map and 75 Venn examples.
- The curated dataset is improved for demo and smoke testing, but human review is still recommended before claiming high model quality.
