import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/productivity/todo-finish/finish.py"


def run_finish(todo_dir, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(todo_dir), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def task_file(stage="test", status="open", with_done_line=True):
    done_line = "done:\n" if with_done_line else ""
    return (
        "---\n"
        f"status: {status}\n"
        f"stage: {stage}\n"
        "type: feature\n"
        "created: 2026-09-20\n"
        "name: ทดสอบปิดงาน\n"
        f"{done_line}"
        "---\n"
        "\n"
        "## Progress\n"
        "\n"
        "- 2026-09-20: started\n"
    )


class TodoFinishTests(unittest.TestCase):
    def test_list_shows_only_test_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            (todo / "features/a.md").write_text(task_file(stage="test"), encoding="utf-8")
            (todo / "features/b.md").write_text(task_file(stage="wip"), encoding="utf-8")

            result = run_finish(todo)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("(1 at stage: test)", result.stdout)
            self.assertIn("features/a.md", result.stdout)
            self.assertNotIn("features/b.md", result.stdout)

    def test_done_sets_status_and_date_and_keeps_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/a.md"
            target.write_text(task_file(stage="test"), encoding="utf-8")

            result = run_finish(todo, "--done", "features/a.md", "--date", "2026-09-24")

            self.assertEqual(result.returncode, 0, result.stderr)
            text = target.read_text(encoding="utf-8")
            self.assertIn("status: done", text)
            self.assertIn("done: 2026-09-24", text)
            self.assertIn("## Progress", text)
            self.assertIn("- 2026-09-20: started", text)
            self.assertLess(text.index("status: done"), text.index("done: 2026-09-24"))

    def test_done_inserts_missing_done_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/a.md"
            target.write_text(task_file(stage="test", with_done_line=False), encoding="utf-8")

            result = run_finish(todo, "--done", "all", "--date", "2026-09-24")

            self.assertEqual(result.returncode, 0, result.stderr)
            text = target.read_text(encoding="utf-8")
            self.assertIn("done: 2026-09-24", text)
            self.assertLess(text.index("status: done"), text.index("done: 2026-09-24"))

    def test_done_skips_non_test_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/wip-task.md"
            original = task_file(stage="wip")
            target.write_text(original, encoding="utf-8")

            result = run_finish(todo, "--done", "features/wip-task.md")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("skipped", result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_revert_sets_stage_wip(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/a.md"
            target.write_text(task_file(stage="test"), encoding="utf-8")

            result = run_finish(todo, "--revert", "features/a.md")

            self.assertEqual(result.returncode, 0, result.stderr)
            text = target.read_text(encoding="utf-8")
            self.assertIn("stage: wip", text)
            self.assertIn("status: open", text)

    def test_unknown_file_aborts_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/a.md"
            original = task_file(stage="test")
            target.write_text(original, encoding="utf-8")

            result = run_finish(todo, "--done", "features/missing.md")

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_done_and_revert_together_abort_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            todo.mkdir()
            target = todo / "a.md"
            original = task_file()
            target.write_text(original, encoding="utf-8")

            result = run_finish(todo, "--done", "all", "--revert", "a.md")

            self.assertEqual(result.returncode, 2)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_bad_date_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            todo.mkdir()

            result = run_finish(todo, "--done", "all", "--date", "2026-13-99")

            self.assertEqual(result.returncode, 2, result.stdout)


if __name__ == "__main__":
    unittest.main()
