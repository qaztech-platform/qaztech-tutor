# Training data

All dialogues are synthetic. A teacher model (Qwen3-30B-A3B-Instruct-2507, Apache-2.0) wrote one
student turn and one tutor turn from a 2,500-character excerpt of Microsoft Azure documentation
(CC BY 4.0). The student never sees the excerpt, so the tutor must not refer to it.

## Source

| Area | Repository path |
|---|---|
| Role-based access control | `articles/role-based-access-control` |
| Virtual networks | `articles/virtual-network` |
| Azure Resource Manager | `articles/azure-resource-manager` |
| App Service | `articles/app-service` |

1,194 Markdown files, 6,554 excerpts after front-matter removal.

## Composition (v0.2, 5,107 dialogues)

| Mode | Count | Source |
|---|---|---|
| Explanation and summary | 1,804 | generation v1 |
| Misconception correction | 1,613 | generation v2 |
| Certification-style practice question | 1,690 | generation v2 |

| Language | Count | Practice questions |
|---|---|---|
| Russian | 1,149 | 389 |
| Kazakh | 1,023 | 220 |
| Spanish | 1,011 | 361 |
| English | 980 | 334 |
| Arabic | 944 | 386 |

Split: 4,907 train, 200 held out (random, seed 7).

## Filters (stage 05)

| Rule | Removed |
|---|---|
| v1 dialogues from the superseded practice-question and misconception modes | 2,009 |
| Question and answer in different languages (word-based detection) | 91 |
| Practice question without a question stem before options A-D | 66 |
| Reference to unseen source text ("in the material above") | 37 |
| Duplicate answers (first 120 normalised characters) | 14 |
| Arabic mixed with Cyrillic | 5 |
| CJK characters | 2 |

## Known issues

- Kazakh and Arabic dialogues have not yet been reviewed by native speakers.
- The teacher sometimes translates Azure role names into Kazakh; Microsoft exams use English names.
- Facts are only as reliable as the teacher's reading of the excerpt; no automatic fact check yet.
