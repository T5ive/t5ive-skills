import subprocess
import sys
import tempfile
import unittest
from itertools import combinations
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/productivity/todo-finish/finish.py"


def run_finish(todo_dir, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(todo_dir), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def task_file(stage="gate", status="open", with_done_line=True):
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
    def test_list_shows_only_open_probe_gate_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            (todo / "features/a.md").write_text(task_file(stage="gate"), encoding="utf-8")
            (todo / "features/b.md").write_text(task_file(stage="wip"), encoding="utf-8")
            (todo / "features/probe.md").write_text(task_file(stage="probe"), encoding="utf-8")
            (todo / "features/closed.md").write_text(task_file(stage="gate", status="fin"), encoding="utf-8")

            result = run_finish(todo)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("(2 open at probe/gate)", result.stdout)
            self.assertIn("features/a.md", result.stdout)
            self.assertIn("features/probe.md", result.stdout)
            self.assertIn("| probe |", result.stdout)
            self.assertIn("| gate |", result.stdout)
            self.assertNotIn("features/b.md", result.stdout)
            self.assertNotIn("features/closed.md", result.stdout)

    def test_done_sets_status_and_date_and_keeps_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/a.md"
            target.write_text(task_file(stage="gate"), encoding="utf-8")

            result = run_finish(todo, "--done", "features/a.md", "--date", "2026-09-24")

            self.assertEqual(result.returncode, 0, result.stderr)
            text = target.read_text(encoding="utf-8")
            self.assertIn("status: fin", text)
            self.assertIn("done: 2026-09-24", text)
            self.assertIn("## Progress", text)
            self.assertIn("- 2026-09-20: started", text)
            self.assertLess(text.index("status: fin"), text.index("done: 2026-09-24"))

    def test_done_inserts_missing_done_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            todo = Path(tmp) / "todo"
            (todo / "features").mkdir(parents=True)
            target = todo / "features/a.md"
            target.write_text(task_file(stage="gate", with_done_line=False), encoding="utf-8")

            result = run_finish(todo, "--done", "all", "--date", "2026-09-24")

            self.assertEqual(result.returncode, 0, result.stderr)
            text = target.read_text(encoding="utf-8")
            self.assertIn("done: 2026-09-24", text)
            self.assertLess(text.index("status: fin"), text.index("done: 2026-09-24"))

    def test_done_skips_non_gate_file(self):
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
            target.write_text(task_file(stage="gate"), encoding="utf-8")

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
            original = task_file(stage="gate")
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

    def test_actions_obey_stage_and_status_boundaries(self):
        eligible = {
            "--pass": {"probe"},
            "--done": {"gate"},
            "--revert": {"probe", "gate"},
        }
        for action, stages in eligible.items():
            for stage in ("todo", "preop", "mise", "wip", "probe", "gate"):
                for status in ("open", "fin"):
                    with self.subTest(action=action, stage=stage, status=status):
                        with tempfile.TemporaryDirectory() as tmp:
                            todo = Path(tmp)
                            target = todo / "task.md"
                            original = task_file(stage=stage, status=status).replace(
                                "done:\n", "done: 2026-09-20\n",
                            ).encode("utf-8")
                            target.write_bytes(original)
                            result = run_finish(todo, action, "task.md", "--date", "2026-10-12")
                            self.assertEqual(result.returncode, 0, result.stderr)
                            if status != "open" or stage not in stages:
                                self.assertEqual(target.read_bytes(), original)
                            else:
                                text = target.read_text(encoding="utf-8")
                                if action == "--pass":
                                    self.assertIn("stage: gate", text)
                                    self.assertIn("status: open", text)
                                    self.assertIn("done: 2026-09-20", text)
                                elif action == "--done":
                                    self.assertIn("status: fin", text)
                                    self.assertIn("stage: gate", text)
                                    self.assertIn("done: 2026-10-12", text)
                                else:
                                    self.assertIn("stage: wip", text)
                                    self.assertIn("status: open", text)
                                    self.assertIn("done: 2026-09-20", text)

    def test_all_and_multiple_names_change_only_eligible_open_tasks(self):
        eligible = {"--pass": {"probe"}, "--done": {"gate"}, "--revert": {"probe", "gate"}}
        for action, stages in eligible.items():
            for selection in ("all", "names"):
                with self.subTest(action=action, selection=selection):
                    with tempfile.TemporaryDirectory() as tmp:
                        todo = Path(tmp)
                        originals = {}
                        for stage, status in (
                            ("probe", "open"), ("gate", "open"), ("wip", "open"),
                            ("probe", "fin"), ("gate", "fin"),
                        ):
                            name = f"{stage}-{status}.md"
                            originals[name] = task_file(stage=stage, status=status).encode("utf-8")
                            (todo / name).write_bytes(originals[name])
                        names = ["all"] if selection == "all" else list(originals)
                        result = run_finish(todo, action, *names)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        for name, original in originals.items():
                            stage, status = name.removesuffix(".md").split("-")
                            if status == "open" and stage in stages:
                                self.assertNotEqual((todo / name).read_bytes(), original)
                            else:
                                self.assertEqual((todo / name).read_bytes(), original)

    def test_unknown_name_after_valid_name_aborts_every_action_without_writing(self):
        for action, stage in (("--pass", "probe"), ("--done", "gate"), ("--revert", "gate")):
            with self.subTest(action=action):
                with tempfile.TemporaryDirectory() as tmp:
                    todo = Path(tmp)
                    target = todo / "task.md"
                    original = task_file(stage=stage).encode("utf-8")
                    target.write_bytes(original)
                    result = run_finish(todo, action, "task.md", "missing.md")
                    self.assertEqual(result.returncode, 2, result.stdout)
                    self.assertEqual(target.read_bytes(), original)

    def test_every_pair_of_actions_is_rejected_without_writing(self):
        for first, second in combinations(("--pass", "--done", "--revert"), 2):
            with self.subTest(first=first, second=second):
                with tempfile.TemporaryDirectory() as tmp:
                    todo = Path(tmp)
                    target = todo / "task.md"
                    original = task_file(stage="probe").encode("utf-8")
                    target.write_bytes(original)
                    result = run_finish(todo, first, "task.md", second, "all")
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(target.read_bytes(), original)

    def test_all_cannot_be_mixed_with_names(self):
        for action in ("--pass", "--done", "--revert"):
            with self.subTest(action=action):
                with tempfile.TemporaryDirectory() as tmp:
                    todo = Path(tmp)
                    target = todo / "task.md"
                    original = task_file(stage="probe").encode("utf-8")
                    target.write_bytes(original)
                    result = run_finish(todo, action, "all", "task.md")
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(target.read_bytes(), original)

    def test_pass_then_close_preserves_body_custom_metadata_and_line_endings(self):
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                with tempfile.TemporaryDirectory() as tmp:
                    todo = Path(tmp)
                    target = todo / "task.md"
                    content = task_file(stage="probe").replace(
                        "type: feature\n", "type: feature\nowner: ผู้ใช้\n",
                    ) + "\n## Before / After\n\nรายงานเดิม ต้องเก็บไว้\n"
                    original = content.replace("\n", newline).encode("utf-8")
                    target.write_bytes(original)
                    original_body = original.split((newline + "---").encode(), 1)[1]
                    for action in ("--pass", "--done"):
                        result = run_finish(todo, action, "task.md", "--date", "2026-10-12")
                        self.assertEqual(result.returncode, 0, result.stderr)
                        current = target.read_bytes()
                        self.assertEqual(current.split((newline + "---").encode(), 1)[1], original_body)
                        self.assertIn(("owner: ผู้ใช้" + newline).encode("utf-8"), current)
                        self.assertIn(("stage: gate" + newline).encode(), current)
                    closed = target.read_bytes()
                    self.assertIn(("status: fin" + newline).encode(), closed)
                    self.assertIn(("done: 2026-10-12" + newline).encode(), closed)
                    repeated = run_finish(todo, "--done", "task.md", "--date", "2026-10-13")
                    self.assertEqual(repeated.returncode, 0, repeated.stderr)
                    self.assertEqual(target.read_bytes(), closed)

    def test_bad_date_does_not_close_an_existing_gate_task(self):
        for invalid in ("2026-02-30", "12/10/2026"):
            with self.subTest(date=invalid):
                with tempfile.TemporaryDirectory() as tmp:
                    todo = Path(tmp)
                    target = todo / "task.md"
                    original = task_file().encode("utf-8")
                    target.write_bytes(original)
                    result = run_finish(todo, "--done", "task.md", "--date", invalid)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(target.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
