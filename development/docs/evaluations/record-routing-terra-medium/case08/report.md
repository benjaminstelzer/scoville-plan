# Case 08 report

## Read ledger

- `Z:\Projekts\AI\scoville-scribe-anti-ai-slop\scoville-scribe-anti-ai-slop\SKILL.md`: frontmatter discovery, then selected Core.
- `Z:\Projekts\AI\scoville-scribe-anti-ai-slop\scoville-scribe-anti-ai-slop\references\prose-patterns.md`: selected Prose reference for a continuous claim-preserving rewrite.
- `verbose-before\docs\plans\0001-migrate-cli-cache.md`: inspected only to confirm the copied fixture and that no native edit was required.

## Availability and opt-out

Scribe was available and applicable because the requested artifact was a rewrite. Scoville Plan was explicitly opted out and unavailable for this case, so it was not discovered, loaded, required, or simulated.

## Decision

Use Scribe routes `CORE_ONLY, Prose`. Treat the supplied external paragraph as the rewrite target. Remove only the redundant explanation of the exporter while preserving the component, export action, existing-report scope, and requirement to preserve report IDs.

## Output

The exporter must preserve existing report IDs during export.

## Validation

The rewrite is shorter, retains the original requirement and terminology, and uses a complete sentence with no prohibited punctuation. No fixture content was edited.
