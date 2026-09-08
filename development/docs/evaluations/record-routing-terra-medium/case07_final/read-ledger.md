# Actual read ledger

Test case: case07_final

Candidate discovery read only complete YAML frontmatter, before selection.

| Order | Path | Read scope | Purpose |
| --- | --- | --- | --- |
| 1 | `Z:/Projekts/AI/scoville-plan/scoville-plan/SKILL.md` | Complete YAML frontmatter | Candidate discovery |
| 2 | `Z:/Projekts/AI/scoville-scribe-anti-ai-slop/scoville-scribe-anti-ai-slop/SKILL.md` | Complete YAML frontmatter | Candidate discovery |
| 3 | `Z:/Projekts/AI/scoville-plan/scoville-plan/SKILL.md` | Complete Core | Selected Plan owner rules |
| 4 | `Z:/Projekts/AI/scoville-scribe-anti-ai-slop/scoville-scribe-anti-ai-slop/SKILL.md` | Complete Core | Explicit Scribe wording request |
| 5 | `Z:/Projekts/AI/scoville-plan/scoville-plan/references/native-plan-format.md` | Complete reference | Plan text and Work Item format |
| 6 | `Z:/Projekts/AI/scoville-plan/scoville-plan/references/native-project-lifecycle.md` | Complete reference | Lifecycle preservation |
| 7 | `Z:/Projekts/AI/scoville-plan/scoville-plan/references/native-editing.md` | Complete reference | Narrow-edit and verification rules |
| 8 | `case07_final/PROJECT_INDEX.md` | Complete bytes | Root and active Plan routing |
| 9 | `case07_final/docs/plans/0001-migrate-cli-cache.md` | Complete bytes | Plan context and W-001 block |
| 10 | `case07_final/docs/decisions/0001-stage-cache-migration.md` | Complete bytes | Proposed Decision inventory and W-001 relation |
| 11 | `Z:/Projekts/AI/scoville-plan/scoville-plan/references/profile-validation.md` | Complete reference | Post-write validation route |
| 12 | `case07_final/docs/plans/0001-migrate-cli-cache.md` | Complete affected Work Item block | Post-write prose and field-order check |

Selection: Plan owns native format and lifecycle. Scribe was explicitly requested for native record wording, so it was active for the Outcome transformation. The target is a fixed short Work Item field, therefore Scribe used Core-only. Plan loaded routes `P`, `L`, and `E`; post-write validation additionally loaded `V`.
