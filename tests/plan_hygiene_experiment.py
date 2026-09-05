"""Deterministic returned-text experiment, not an agent or archive implementation."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / 'docs/benchmarks/plan-hygiene'
VALIDATOR = ROOT / 'scoville-plan/scripts/validate_profile.py'
PLAN_PATH = 'docs/plans/0001-synthetic-history.md'
OPERATIONS = ('resume', 'progress', 'prerequisite', 'history', 'inventory', 'audit')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_plan(text: str) -> tuple[str, dict[str, str]]:
    """Extract exact H3 ranges from known-valid experiment fixtures only."""
    matches = list(re.finditer(r'^### (W-\d{3}) .+$', text, re.M))
    if not matches or len({m[1] for m in matches}) != len(matches):
        raise ValueError('ambiguous experiment fixture')
    blocks = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[match[1]] = text[match.start():end]
    return text[:matches[0].start()], blocks


def metadata(text: str) -> str:
    return ''.join(line + '\n' for line in text.splitlines()
                   if line.startswith(('### ', 'Status:', 'Depends on:', 'Decisions:')))


def fixture(count: int, layout: str) -> tuple[dict[str, str], dict]:
    current = count - 1
    done = {n for n in range(1, current)
            if (n <= int(count * .8) if layout == 'prefix' else n % 5 != 0)}
    prerequisite = max(done)
    header = f'''---
format_version: 1
id: PLAN-0001
status: active
created: 2026-09-05
updated: 2026-09-05
current_item: W-{current:03}
---

# Synthetic history fixture

## Goal

Exercise selective Plan reads on synthetic work; no real completion is asserted.

## Non-goals

- Do not treat generated Evidence as proof of real work.

## Work items

'''
    blocks = []
    for n in range(1, count + 1):
        status = 'done' if n in done else ('in_progress' if n == current else 'todo')
        dep = f'W-{prerequisite:03}' if n == current else (f'W-{current:03}' if n == count else '')
        evidence = f'[Synthetic acceptance record for route {n:03}]' if status == 'done' else '[]'
        block = f'''### W-{n:03} Preserve route {n:03}

Status: {status}
Depends on: [{dep}]
Blocked by: []
Decisions: [ADR-0001]
Outcome: Route {n:03} retains its observable response and persisted configuration under the agreed compatibility boundary.
Acceptance: Exercise route {n:03} with populated and empty configuration and inspect the stored values after reload.
Steps:
1. Inspect the owning route and its consumers; retain the originally observed behavior and the selected scope for later investigation of route {n:03}.
2. Compare the response and persisted configuration before and after the bounded change, including the empty-state behavior and compatibility condition for route {n:03}.
Evidence: {evidence}
'''
        if status != 'done':
            block += f'Next action: Inspect the first unobserved check for route {n:03}.\n'
        blocks.append(block + '\n')
    accepted = (ROOT / 'tests/fixtures/valid-profile/docs/decisions/0001-use-read-only-validation.md').read_text(encoding='utf-8')
    proposal = accepted.replace('ADR-0001', 'ADR-0002').replace('status: accepted', 'status: proposed').replace('accepted: 2026-08-08\n', '')
    files = {
        'PROJECT_INDEX.md': '---\nformat_version: 1\nactive_plan: PLAN-0001\n---\n',
        PLAN_PATH: header + ''.join(blocks),
        'docs/decisions/0001-use-read-only-validation.md': accepted,
        'docs/decisions/0002-synthetic-proposal.md': proposal,
    }
    return files, {'current': f'W-{current:03}', 'prerequisite': f'W-{prerequisite:03}',
                   'history': 'W-001', 'done': [f'W-{n:03}' for n in sorted(done)]}


def write_fixture(root: Path, files: dict[str, str]) -> None:
    for relative, text in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8', newline='\n')


def validate(root: Path) -> dict:
    result = subprocess.run([sys.executable, '-B', str(VALIDATOR), '--root', str(root), '--format', 'json'],
                            capture_output=True, text=True, encoding='utf-8', check=False)
    payload = json.loads(result.stdout)
    return {'exit_code': result.returncode, 'valid': payload['valid'],
            'codes': [d['code'] for d in payload['diagnostics']]}


def context(files: dict[str, str], ids: dict, operation: str) -> str:
    head, blocks = split_plan(files[PLAN_PATH])
    # All proposal frontmatter is inventoried. Only the proposal and relevant
    # accepted choice are returned in full for these direction-aware scenarios.
    decisions = ''.join(value for key, value in files.items() if key.startswith('docs/decisions/'))
    common = files['PROJECT_INDEX.md'] + decisions
    if operation == 'audit':
        return common + files[PLAN_PATH]
    if operation == 'inventory':
        return common + head + metadata(files[PLAN_PATH])
    selected = [ids['current']]
    if operation in ('progress', 'prerequisite'):
        selected.append(ids['prerequisite'])
    if operation == 'history':
        selected = [ids['history']]
    return common + head + ''.join(blocks[key] for key in selected)


def projected_route(ids: dict) -> str:
    # Deliberately noncanonical, display-only archive routing. No consumer reads it.
    return 'PROJECTION ONLY: terminal blocks in history.md; original logical order retained.\n'


def measurement(files: dict[str, str], ids: dict, operation: str) -> dict:
    head, blocks = split_plan(files[PLAN_PATH])
    before = context(files, ids, operation)
    baseline = selective = before
    if operation == 'progress':
        updated = blocks[ids['current']].replace('Inspect the first unobserved check', 'Run the remaining reload check')
        full_after = files[PLAN_PATH].replace(blocks[ids['current']], updated)
        # Same initial reads. The baseline's mandatory whole-file post-read is
        # the only difference; byte checks and validator output are separate.
        baseline += full_after
        selective += head + updated
    projection = selective + projected_route(ids)
    archived = {key: blocks[key] for key in ids['done']}
    live = {key: value for key, value in blocks.items() if key not in archived}
    merged = head + ''.join((archived if key in archived else live)[key] for key in blocks)
    assert merged == files[PLAN_PATH], 'projection lost original authored data or order'
    views = {'baseline': baseline, 'selective': selective, 'archive_projection': projection}
    base_lookups = {'resume': 1, 'progress': 3, 'prerequisite': 2, 'history': 1, 'inventory': 1, 'audit': 1}[operation]
    # Plan-section lookups only; shared Decision and index reads excluded.
    extra = int(operation in ('progress', 'prerequisite', 'history', 'inventory', 'audit'))
    return {'operation': operation,
            'views': {key: {'characters': len(value), 'utf8_bytes': len(value.encode('utf-8')),
                            'sha256': digest(value.encode('utf-8')),
                            'plan_section_lookups': base_lookups + (extra if key == 'archive_projection' else 0)}
                      for key, value in views.items()},
            'history_removed_from_postread_characters': len(baseline) - len(selective),
            'projection_incremental_saved_characters': len(selective) - len(projection),
            'common_hash_validation_output': 'Excluded equally from all views; full internal checks retained.',
            'projection_preserves_original_bytes_and_order': True}


def rollover_measurement(root: Path, count: int) -> dict:
    """Separate completed-goal case; not a substitute for a live dependency."""
    files, _ = fixture(count, 'prefix')
    head, blocks = split_plan(files[PLAN_PATH])
    head = head.replace('status: active', 'status: completed')
    head = re.sub(r'^current_item:.*\n', '', head, flags=re.M)
    completed = []
    for block in blocks.values():
        block = re.sub(r'^Status:.*$', 'Status: done', block, flags=re.M)
        block = block.replace('Evidence: []', 'Evidence: [Synthetic completed-goal acceptance]')
        block = re.sub(r'^Next action:.*\n', '', block, flags=re.M)
        completed.append(block)
    files[PLAN_PATH] = head + ''.join(completed)
    successor_files, successor_ids = fixture(8, 'prefix')
    successor_head, successor_blocks = split_plan(successor_files[PLAN_PATH])
    successor = successor_head.replace('PLAN-0001', 'PLAN-0002').replace('W-007', 'W-001')
    successor = successor.replace('# Synthetic history fixture', '# Synthetic independent successor goal')
    new_item = successor_blocks['W-007'].replace('W-007', 'W-001').replace('Depends on: [W-006]', 'Depends on: []')
    files['docs/plans/0002-independent-successor.md'] = successor + new_item
    files['PROJECT_INDEX.md'] = files['PROJECT_INDEX.md'].replace('PLAN-0001', 'PLAN-0002')
    write_fixture(root, files)
    checked = validate(root)
    assert checked['valid'], checked
    returned = files['PROJECT_INDEX.md'] + successor + new_item + ''.join(
        value for key, value in files.items() if key.startswith('docs/decisions/'))
    return {'completed_items': count, 'retained_completed_plan_characters': len(files[PLAN_PATH]),
            'current_context_characters': len(returned), 'valid': checked,
            'scope': 'Independent new goal after completion; no cross-Plan dependency implied.'}


def run() -> dict:
    protocol = json.loads((EVIDENCE / 'protocol.json').read_text(encoding='utf-8'))
    for rel, expected in protocol['frozen_sources'].items():
        if digest((ROOT / rel).read_bytes()) != expected:
            raise ValueError(f'frozen source changed: {rel}')
    rows = []
    traces = []
    rollover = []
    with tempfile.TemporaryDirectory(prefix='scoville-hygiene-') as temporary:
        for count in protocol['item_counts']:
            for layout in protocol['layouts']:
                files, ids = fixture(count, layout)
                root = Path(temporary) / f'{count}-{layout}'
                write_fixture(root, files)
                valid_before = validate(root)
                if not valid_before['valid']:
                    raise ValueError(valid_before)
                original = (root / PLAN_PATH).read_bytes()
                views = [measurement(files, ids, op) for op in OPERATIONS]
                # Exercise an actual scoped progress patch and full post-validation.
                _, blocks = split_plan(files[PLAN_PATH])
                old = blocks[ids['current']]
                new = old.replace('Inspect the first unobserved check', 'Run the remaining reload check')
                expected = files[PLAN_PATH].replace(old, new).encode('utf-8')
                if (root / PLAN_PATH).read_bytes() != original:
                    raise ValueError('changed before prepared patch')
                (root / PLAN_PATH).write_bytes(expected)
                valid_after = validate(root)
                assert valid_after['valid'] and (root / PLAN_PATH).read_bytes() == expected
                # An invalid untouched historical relation is still caught by
                # complete validation, even though no history body was returned.
                broken = expected.replace(b'Depends on: []', b'Depends on: [W-999]', 1)
                (root / PLAN_PATH).write_bytes(broken)
                diagnostic = validate(root)
                assert 'WORK_DEPENDENCY_MISSING' in diagnostic['codes']
                # A whole-file hash notices concurrent changes outside the slice.
                stale = digest(expected)
                assert digest((root / PLAN_PATH).read_bytes()) != stale
                traces.append({'fixture': f'{count}-{layout}', 'before': valid_before,
                               'after_progress': valid_after, 'untouched_dependency': diagnostic,
                               'concurrent_outside_slice_change_detected': True,
                               'written_bytes_match_prepared_result': True})
                rows.append({'fixture': f'{count}-{layout}', 'items': count, 'done': len(ids['done']),
                             'plan_characters': len(files[PLAN_PATH]),
                             'fixture_sha256': {key: digest(value.encode('utf-8')) for key, value in files.items()},
                             'operations': views})
            rollover.append(rollover_measurement(Path(temporary) / f'rollover-{count}', count))
    return {'schema_version': 1, 'protocol_sha256': digest((EVIDENCE / 'protocol.json').read_bytes()),
            'kind': 'deterministic scripted returned-text measurement; no agent runs',
            'tokenizer': None, 'provider_usage': None, 'monetary_savings': None,
            'rows': rows, 'guard_traces': traces,
            'rollover': {'active_goal': 'inapplicable: cannot close an unfinished goal or replace live dependencies with prose',
                         'completed_goal_measurements': rollover},
            'archive_setup': 'Unmeasured: new version, routing, consumers, conversion and recovery required.',
            'recommendation': 'Retain selective reading; this projection demonstrates no additional returned-text saving from moving the same records.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
