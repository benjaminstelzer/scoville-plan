# Case 02 retry ledger

## Scope

The requested artifact is an external, continuous prose paragraph. It asks for a shorter claim-preserving rewrite. Plan is absent and unavailable for this case.

## Command and read order

1. Discovery was the first skill-content access. The path variable had the value `Z:\Projekts\AI\scoville-scribe-anti-ai-slop\scoville-scribe-anti-ai-slop\SKILL.md`. The required discovery command ran exactly:

```powershell
$t=[System.IO.File]::ReadAllText($path); [regex]::Match($t,'\A---\r?\n[\s\S]*?\r?\n---(?:\r?\n|\z)').Value
```

   The path was `Z:\Projekts\AI\scoville-scribe-anti-ai-slop\scoville-scribe-anti-ai-slop\SKILL.md`. Its front matter described a wording transformation skill and directed Scribe to preserve facts, meaning, terms, and behavior.

2. The source fixture copy command was:

```powershell
$src='C:\Users\benja\AppData\Local\Temp\scoville-record-writing-906c32ca89244ff7bec8a2d315f82862\record-test\verbose-before'; $dst='C:\Users\benja\AppData\Local\Temp\scoville-record-writing-906c32ca89244ff7bec8a2d315f82862\terra-routing\case02-retry\verbose-before'; New-Item -ItemType Directory -Force -LiteralPath (Split-Path -Parent $dst) | Out-Null; Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force; Get-ChildItem -LiteralPath $dst -Force | Select-Object Name,Mode,Length
```

   `New-Item` emitted an error because `-LiteralPath` is unsupported for that cmdlet. The destination parent already existed, and the subsequent copy completed. No fixture file was edited.

3. The full Scribe Core was read with:

```powershell
Get-Content -Raw -LiteralPath 'Z:\Projekts\AI\scoville-scribe-anti-ai-slop\scoville-scribe-anti-ai-slop\SKILL.md'
```

4. After routing, the Prose reference was read with:

```powershell
Get-Content -Raw -LiteralPath 'Z:\Projekts\AI\scoville-scribe-anti-ai-slop\scoville-scribe-anti-ai-slop\references\prose-patterns.md'
```

No installed skill copy, other skill package, network source, repository content, or additional Scribe reference was accessed.

## Decision

Scribe activates because the wording transformation is the requested deliverable. The mode is Edit. The selected route is `Prose`, because this is a continuous, claim-preserving external rewrite. Fidelity and Interface do not independently trigger.

## Output

The exporter must preserve existing report IDs during export.

## Validation

The rewrite is shorter. It retains the subject, the required preservation, the existing report IDs, and the export context. It removes only the redundant explanation that the exporter performs export. The output contains no em dash, en dash, or semicolon.

The report was then read with `[System.IO.File]::ReadAllText` to confirm its existence, output, and selected route. A broad punctuation check on the complete report returned true because the required command transcripts contain semicolons. That result does not apply to the external rewrite.
