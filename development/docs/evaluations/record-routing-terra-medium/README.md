# Native record routing with Terra Medium

Date: 2026-09-08. Each execution used a fresh `gpt-5.6-terra` subagent with
`medium` effort and no inherited conversation. Availability was stipulated per
case. These are candidate-file routing checks, not live host discovery tests.

| Case | Observed routing |
| --- | --- |
| 1 | Plan alone edits the native Outcome through P/W/E. |
| 2 | Scribe alone edits an external plan paragraph through Prose. |
| 3 | With both available, native Outcome wording stays with Plan. |
| 4 | Native Decision wording audit uses Plan and D, without edits. |
| 5 | Plan handles the native Outcome, Scribe the separate release note. |
| 6 | Prior Scribe use does not carry into the native Goal rewrite. |
| 7 | Initial explicit Scribe run omitted Plan's edit checks. See correction below. |
| 8 | With Plan opted out, Scribe edits the external paragraph. |
| 9 | Unavailable Plan does not prevent explicit Scribe use. |

## Failures and correction

The original case 1 and 2 discovery reads exposed Core text. Case 9 initially
used an installed copy and the wrong read order. Those executions are invalid
as discovery evidence. Each has one fresh corrected run in its `-retry` folder.
All original reports are retained alongside the corrected reports.

Case 7 exposed a real gap: explicit Scribe use was treated as sufficient to edit
a native record without loading available Plan for its format and lifecycle.
Both Cores now state that explicit Scribe use supplies wording while applicable
Plan still checks permitted edits, format, and lifecycle. The targeted final
execution is recorded separately. It loaded both Cores but selected P/L/E for
the Work Item field, omitting W. The rewrite table was then split into separate
Plan, Work Item, and Decision rows, with selection by edited record rather
than containing file. The [final targeted run](case07_routes_final/REPORT.md)
loaded both Cores and P/W/E/V, changed only Outcome, retained all other fields,
and passed native structural validation. Its [ledger](case07_routes_final/LEDGER.md)
records the actual reads and byte checks. The earlier eight case results cover
unchanged branches, not a repeat of all nine cases on the final Core bytes.

The initial cases used these SHA-256 values:

- Plan Core: `E0ED7AEAC589CC15E65DF2D256DC3C2482CC17F69716C81823D421D258F82B91`
- Scribe Core: `39A14BE01FCBE3B0D3575F1A671B4EA4237FAD6D649C6F22D90A97F2AEFA7F45`

## Evidence limits

Final Core SHA-256 values:

- Plan: `3BEF62E1C76F133A450D7B328B0F14E66D9618FC3BE12AD506335ECA6F66D3DC`
- Scribe: `CCFC04CCAEEE5DEE18A157422A86E243FB90CBD60BEBA4693213F047BCC14600`

Reports and any separate ledgers contain actual reads, outputs, and native
validation observations. Case 5 changed `CSV export is available.` to
`CSV export is now available.`, adding unsupported temporal emphasis. Routing
success does not qualify general prose fidelity, token savings, or every host.
The source fixture is retained under `development/tests/fixtures/record-writing/before/`.
