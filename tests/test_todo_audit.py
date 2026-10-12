import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/productivity/todo-audit/audit.py"


class TodoAuditTests(unittest.TestCase):
    def test_related_paths_are_expected_to_be_missing_in_todo_and_preop(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp)
            for stage in ("todo", "preop", "mise", "wip", "probe", "gate"):
                (todo / f"{stage}.md").write_text(
                    f"---\nstatus: open\nstage: {stage}\n---\n\n## Related files\n",
                    encoding="utf-8",
                )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(todo), "--checks", "paths"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("| todo.md |", result.stdout)
            self.assertNotIn("| preop.md |", result.stdout)
            for stage in ("mise", "wip", "probe", "gate"):
                self.assertIn(f"| {stage}.md | paths |", result.stdout)

    def test_fin_requires_a_date_but_open_work_does_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp)
            cases = {
                "closed-missing": ("fin", ""),
                "closed-dated": ("fin", "2026-10-12"),
                "open-gate": ("open", ""),
            }
            for name, (status, done) in cases.items():
                (todo / f"{name}.md").write_text(
                    f"---\nstatus: {status}\nstage: gate\ndone: {done}\n---\n",
                    encoding="utf-8",
                )
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(todo), "--checks", "done-date"],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| closed-missing.md | done-date |", result.stdout)
            self.assertNotIn("| closed-dated.md |", result.stdout)
            self.assertNotIn("| open-gate.md |", result.stdout)


if __name__ == "__main__":
    unittest.main()
