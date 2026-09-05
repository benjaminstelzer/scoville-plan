"""Guard the experiment's fact selection and full-profile checks, not prose."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from plan_hygiene_experiment import context, digest, fixture, measurement, metadata, split_plan, validate, write_fixture, PLAN_PATH


class PlanHygieneTest(unittest.TestCase):
    def test_current_and_proposed_choice_survive_without_unrelated_history(self):
        files, ids = fixture(160, 'interleaved')
        view = context(files, ids, 'resume')
        self.assertIn(f"### {ids['current']} ", view)
        self.assertIn('id: ADR-0002\nstatus: proposed', view)
        self.assertIn('## Goal', view)
        self.assertNotIn('### W-001 ', view)
        self.assertNotIn('Synthetic acceptance record for route 001', view)

    def test_prerequisite_and_historical_evidence_are_retrievable(self):
        files, ids = fixture(160, 'prefix')
        _, blocks = split_plan(files[PLAN_PATH])
        self.assertIn(blocks[ids['prerequisite']], context(files, ids, 'prerequisite'))
        self.assertIn(blocks['W-001'], context(files, ids, 'history'))

    def test_inventory_preserves_every_id_order_and_relation_without_evidence(self):
        files, ids = fixture(160, 'interleaved')
        graph = metadata(files[PLAN_PATH])
        self.assertEqual(160, graph.count('### W-'))
        self.assertLess(graph.index('### W-001'), graph.index('### W-160'))
        self.assertIn(f"Depends on: [{ids['prerequisite']}]", graph)
        self.assertNotIn('Evidence:', graph)

    def test_progress_and_audit_preserve_their_different_read_scopes(self):
        files, ids = fixture(160, 'prefix')
        progress = measurement(files, ids, 'progress')
        self.assertGreater(progress['history_removed_from_postread_characters'], 0)
        audit = measurement(files, ids, 'audit')
        self.assertEqual(0, audit['history_removed_from_postread_characters'])
        self.assertIn(files[PLAN_PATH], context(files, ids, 'audit'))

    def test_ambiguous_duplicate_blocks_are_not_silently_selected(self):
        files, _ = fixture(8, 'prefix')
        text = files[PLAN_PATH].replace('### W-008 ', '### W-007 ')
        with self.assertRaises(ValueError):
            split_plan(text)

    def test_selective_view_does_not_hide_invalid_untouched_history_from_validation(self):
        files, ids = fixture(160, 'interleaved')
        with tempfile.TemporaryDirectory(prefix='hygiene-proof-') as tmp:
            root = Path(tmp)
            write_fixture(root, files)
            self.assertTrue(validate(root)['valid'])
            path = root / PLAN_PATH
            before = path.read_bytes()
            # The extracted current block is unchanged, but another record is invalid.
            files[PLAN_PATH] = files[PLAN_PATH].replace('Evidence: [Synthetic acceptance record for route 001]', 'Evidence: []')
            write_fixture(root, files)
            self.assertNotIn('### W-001 ', context(files, ids, 'resume'))
            self.assertNotEqual(digest(before), digest(path.read_bytes()))
            self.assertIn('WORK_TERMINAL_EVIDENCE_REQUIRED', validate(root)['codes'])

    def test_progress_patch_preserves_other_bytes_and_rejects_stale_source(self):
        files, ids = fixture(160, 'prefix')
        with tempfile.TemporaryDirectory(prefix='hygiene-progress-') as tmp:
            root = Path(tmp)
            write_fixture(root, files)
            path = root / PLAN_PATH
            captured = path.read_bytes()
            _, blocks = split_plan(files[PLAN_PATH])
            old = blocks[ids['current']].encode('utf-8')
            new = old.replace(b'Inspect the first unobserved check', b'Run the remaining reload check')
            prepared = captured.replace(old, new)
            self.assertEqual(captured, path.read_bytes())
            path.write_bytes(prepared)
            self.assertEqual(prepared, path.read_bytes())
            self.assertEqual(captured.replace(old, b''), path.read_bytes().replace(new, b''))
            self.assertTrue(validate(root)['valid'])
            captured = path.read_bytes()
            path.write_bytes(captured.replace(b'Depends on: []', b'Depends on: [W-999]', 1))
            observed = path.read_bytes()
            self.assertIn('WORK_DEPENDENCY_MISSING', validate(root)['codes'])
            # The intended edit is refused because whole-file equality fails,
            # even though its selected current block is unchanged.
            wrote = False
            if observed == captured:
                path.write_bytes(prepared)
                wrote = True
            self.assertFalse(wrote)
            self.assertEqual(observed, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
