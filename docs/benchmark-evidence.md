# Scoville Plan benchmark evidence

## Final reliability-first qualification

The promoted package is the compressed arm from
`scoville-plan-compression-final-v2`, qualified on 2026-08-10. Routing used
`gpt-5.6-sol` at `xhigh`; execution used `gpt-5.6-terra` at `medium`. Network
access and prediction reuse were disabled.

| Arm | Split | Rows | Hard | Route | Semantic | Process | Efficiency |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Control | Train | 18 | 18 | 18 | 18 | 18 | 18 |
| Control | Validation | 9 | 9 | 9 | 9 | 9 | 9 |
| Control | sealed Test | 3 | 3 | 3 | 3 | 3 | 3 |
| Compressed | Train | 18 | 18 | 18 | 18 | 18 | 18 |
| Compressed | Validation | 9 | 9 | 9 | 9 | 9 | 9 |
| Compressed | sealed Test | 3 | 3 | 3 | 3 | 3 | 3 |

All 60 result rows were agent- and provider-complete. Every per-case read
ledger was exact-once; there were zero route retries, shell calls, activation
mismatches, and failed rows. Test execution occurred exactly once per arm after
the frozen gate passed. This proves the observed benchmark conditions, not
deterministic perfection on every future task.

## Compression

Token counts use `o200k_base`.

| Metric | Control | Compressed | Reduction |
| --- | ---: | ---: | ---: |
| Core tokens | 2,207 | 1,819 | 17.5804% |
| Core bytes | 11,035 | 8,885 | 19.4835% |
| Whole-package tokens | 27,700 | 27,312 | 1.4007% |
| Whole-package bytes | 141,425 | 139,275 | 1.5202% |
| Loaded Skill tokens over 30 rows | 134,142 | 123,666 | 7.8096% |
| Total Skill-related tokens over 30 rows | 163,032 | 152,556 | 6.4257% |

Only the Core differed between the two final benchmark arms, so each of the 27
active rows loaded exactly 388 fewer literal tokens. The three
`not_applicable` rows per arm stopped before Core loading. Observed provider
usage fell from 1,013,578 to 1,003,085 tokens (-1.0352%); provider totals also
include generation and cache variance and are not a deterministic compression
measure.

The public pre-optimization comparison uses the same Core counts: `v1.2.2` used
2,207 tokens and the qualified Skill uses 1,819, a reduction of 388 tokens
(-17.58%).

## Reproducibility bindings

- Promoted Core SHA-256:
  `A63CB7EC862D9E715BC7C1881BC39999789F1FA9354F08C3D826431F8CC2357F`
- Qualified compressed package-tree SHA-256:
  `1295A860B43D0328F6C56786236A7BAA7E7B7E3E78C99BA3EBA4A5801ECA99A2`
- Final JSON report SHA-256:
  `AB78CD6F1A8440A1126270B9B639EB0B7E0B4D7BAE55EA0EEE8A048FC1642B7`
- Final Markdown report SHA-256:
  `AF975A1942CC0D2228F00EE5B6DA57A0C786B71E01B492DAAB8A094E86B0177E`
- Frozen benchmark lock SHA-256:
  `4DF7E25E45C5069ADE04E1AA6A35BEC07E29D945669819FF3D0AB9E155246263`
- Sealed Test payload SHA-256:
  `3C48C3FBA62A669449F99D16D0AD9AF80E39906B38722D010EE03FECA8F88E22`
- SkillOpt revision: Microsoft
  `ba820b500f9da96685cf2780c7dc85ed4eb6563e`

The complete machine-readable and human-readable reports remain in the central
optimization workspace under
`skillopt-studio/runs/scoville-plan-compression-final-v2/`.

## Overall Scoville optimization history

The final four-Skill inventory records 797 run artifacts, including 742
technically valid benchmark runs, 5,762 observed model calls, and 3,452 case
executions. Plan accounts for 180 artifacts, 169 valid benchmark runs, 1,389
model calls, and 792 case executions. The central machine-readable snapshot has
SHA-256
`1270F95CF9777EBC8E97151E37DFA5525D3E2DB8A6F0163DFBD71C8DA395A781`.
