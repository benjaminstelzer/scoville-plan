# Record writing check, 2026-09-08

One independent agent executed creation, wording refinement, and historical
preservation against the candidate Plan rules in four scratch profiles.
The retained [before](../../tests/fixtures/record-writing/before/) and
[after](../../tests/fixtures/record-writing/after/) profiles contain the actual
verbose input and shortened output.

The Plan changed from 224 to 159 whitespace-delimited words, the Decision from
217 to 165. Six prose lines changed. Acceptance, Confirmation, frontmatter,
Steps, constraints, alternatives, and evidence remained unchanged. Manual
comparison retained the supplied requirements and uncertainty. These counts
describe one synthetic example, not token costs or a general quality score.

Eight native validations passed with no errors or warnings. Nine untouched
canonical files stayed byte-identical, including an already concise Plan, an
accepted Decision, and the entire Plan containing a started Work Item.

The same agent authored and assessed the fixtures. This was not a blinded
quality comparison. It captured Skill reference hashes late, so this run does
not qualify reference reuse between requests. A later routing-row clarification
did not change the prose rules exercised here. No migration implementation or
behavioral acceptance was performed.

No numeric lint threshold was adopted. Length alone cannot distinguish required
criteria from filler, and repeated terms can preserve necessary meaning. The
required prose check stays with the agent, separate from structural validation.
