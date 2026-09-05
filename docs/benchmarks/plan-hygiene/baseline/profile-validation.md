# Read-only profile validation

Use the bundled validator only to inspect a complete supported Scoville Plan
`format_version: 1` profile. It is an optional structural check, not a planning
CLI, writer, repair tool, lifecycle authority, or requirement for using this
Skill.

## When to run it

Run the validator when its script and a Python 3 interpreter are already
available:

- after changing any canonical Plan, Work Item, Decision, or project index;
- when the user requests a complete native-profile audit; or
- when a supported profile is invalid or an interrupted cross-record state
  needs diagnosis.

Do not run it for a read-only status answer that needs only the index, current
Work Item, and routed Decisions. Do not load the Python source merely to invoke
it. Inspect the source only when debugging the validator itself.

Resolve `<skill-directory>` from the loaded `SKILL.md` location and
`<project-root>` as the immutable root that owns `PROJECT_INDEX.md`,
`docs/plans/`, and `docs/decisions/`. Then run:

```text
python "<skill-directory>/scripts/validate_profile.py" --root "<project-root>" --format json
```

Use JSON for agent work. `--format text` is an optional human-readable view and
does not change exit semantics. The validator accepts no write, repair,
formatting, normalization, migration, allocation, or transition mode.

## Interpret the result

Read both the process exit code and JSON `valid` field:

| Exit | `valid` | Meaning | Next action |
| --- | --- | --- | --- |
| `0` | `true` | Complete inspection found no structural error. | Record only native structural validation; continue with independent behavioral acceptance evidence. |
| `1` | `false` | Complete inspection found one or more contract errors. | Follow ordered diagnostics. Correct only unambiguous representation defects through the native editing route, then rerun. |
| `2` | `null` | Root, path safety, access, I/O, or concurrent change prevented a complete inspection. | Resolve the stated inspection condition or report it. Do not claim the profile is structurally valid or edit around it. |
| `3` | `null` | The validator itself failed unexpectedly. | Report the diagnostic and use manual inspection without claiming validator evidence. Debug the script only when that is the task. |

Each diagnostic names a stable `code`, severity, repository-relative file,
best available line, record and field, expected and observed shape, safe
suggestion, and related records. Diagnostics are deterministically ordered.
Warnings do not make a profile invalid; any structural error does.

Treat a suggestion as bounded guidance, not authority. An exact correction is
permitted only when it changes representation and preserves authored intent.
If a diagnostic asks which lifecycle, evidence, scope, successor, relation, or
authorized choice is intended, stop and ask the user. Never invent the missing
fact to obtain exit `0`.

Load only the native reference needed for the reported record or intended
correction. A Plan field error usually routes to
[native-plan-format.md](native-plan-format.md); Work Item lifecycle and current
selection route to [native-work-items.md](native-work-items.md); Decision shape
or lifecycle routes to [native-decision-format.md](native-decision-format.md);
batch integrity routes to
[native-decision-batches.md](native-decision-batches.md); project activation or
completion routes to
[native-project-lifecycle.md](native-project-lifecycle.md). Any correction also
uses [native-editing.md](native-editing.md).

## Preserve the proof boundary

The validator checks native bytes, local record shape, references, and
lifecycle invariants. It does not prove human authorization, Decision quality,
evidence truth, acceptance sufficiency, reported work occurrence, or the
meaning of authored prose. It checks a Decision batch hash only for its
64-hexadecimal shape and shared symmetric metadata; it cannot recompute a hash
that depends on unavailable pre-mutation bytes.

If Python or the script is unavailable, do not install a dependency merely to
run the check. Follow [native-editing.md](native-editing.md), inspect the same
scoped format and graph invariants manually, and report `native structural
inspection passed` only when actually observed. Never describe manual
inspection as validator output.
