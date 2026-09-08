# Case 09 report

## Stated and observed availability

| Package | Stated availability | Observed location | Handling |
| --- | --- | --- | --- |
| Plan | Stipulated unavailable to read. Frontmatter only may be read. | `C:\\Users\\benja\\.codex\\skills\\scoville-plan\\SKILL.md` exists. The stated `Z:\\Projekts\\AI\\scoville-plan\\SKILL.md` path does not exist. | Treated as unavailable by stipulation. Only frontmatter was read. |
| Scribe | Available at `Z:\\Projekts\\AI\\scoville-scribe-anti-ai-slop`. | That stated path does not exist. The installed package is available at `C:\\Users\\benja\\.codex\\skills\\scoville-scribe-anti-ai-slop`. | Used from the observed installed location. |

## Read ledger

| Order | Path | Read scope | Purpose |
| --- | --- | --- | --- |
| 1 | `C:\\Users\\benja\\.codex\\skills\\scoville-scribe-anti-ai-slop\\SKILL.md` | Full Core | Explicitly requested Scribe instruction. |
| 2 | `C:\\Users\\benja\\.codex\\skills\\scoville-plan\\SKILL.md` | Frontmatter only, extracted with the stipulated `ReadAllText` and anchored regex. | Discovery only. |
| 3 | `C:\\Users\\benja\\.codex\\skills\\scoville-scribe-anti-ai-slop\\SKILL.md` | Frontmatter only, extracted with the stipulated `ReadAllText` and anchored regex. | Discovery only. |
| 4 | `C:\\Users\\benja\\.codex\\skills\\scoville-scribe-anti-ai-slop\\references\\prose-patterns.md` | Full routed reference | Continuous claim-preserving rewrite. |

No Plan Core or Plan reference was read. The immutable fixture was copied to the case scratch directory and not edited.

## Decision

The request is a Scribe Edit: a short, external, claim-preserving rewrite. The selected Scribe route is `Prose`. Plan is not selected because its availability is stipulated unavailable, and no plan-record work was requested.

## External rewrite

The exporter must preserve existing report IDs during export.

## Output validation

- Removes only the redundant explanation that the exporter performs export.
- Retains the subject, requirement strength, preservation action, `existing report IDs`, and export condition.
- Uses one complete sentence with no em dash, en dash, or semicolon.
- Delivers an external rewrite only. No fixture source file was edited.
