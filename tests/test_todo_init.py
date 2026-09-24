import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/productivity/todo-init/init.py"


def run_init(root, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(root), *args, "--no-board", "--no-jira"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def view_layout(board, name):
    match = re.search(
        rf"  - type: table\n    name: {re.escape(name)}\n(.*?)(?=\n  - type: table|\Z)",
        board,
        re.S,
    )
    if not match:
        raise AssertionError(f"missing board view: {name}")
    body = match.group(1)
    return body[body.index("    order:\n"):].rstrip()


class TodoInitTests(unittest.TestCase):
    def test_invalid_phase_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            result = run_init(root, "--phases", "x/../../../outside")

            self.assertEqual(result.returncode, 2)
            self.assertFalse((root / "todo").exists())
            self.assertFalse((Path(tmp) / "outside").exists())

    def test_legacy_preamble_stays_under_general(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "legacy.md"
            source.write_text("standalone note\n## Phase 2\nphase task\n", encoding="utf-8")
            result = run_init(root, "--phases", "2", "--from", str(source))

            self.assertEqual(result.returncode, 0, result.stderr)
            inbox = (root / "todo/inbox.md").read_text(encoding="utf-8")
            self.assertLess(inbox.index("## General"), inbox.index("standalone note"))
            self.assertLess(inbox.index("standalone note"), inbox.index("## Phase 2"))
            self.assertLess(inbox.index("## Phase 2"), inbox.index("phase task"))
            self.assertLess(inbox.index("phase task"), inbox.index("## Misc"))

    def test_utf8_bom_heading_is_recognized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "legacy.md"
            source.write_text("## Phase 2\nphase task\n", encoding="utf-8-sig")
            result = run_init(root, "--phases", "2", "--from", str(source))

            self.assertEqual(result.returncode, 0, result.stderr)
            inbox = (root / "todo/inbox.md").read_text(encoding="utf-8")
            self.assertNotIn("\ufeff", inbox)
            self.assertEqual(inbox.count("## Phase 2"), 1)
            self.assertLess(inbox.index("## Phase 2"), inbox.index("phase task"))

    def test_normal_phase_setup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_init(root, "--phases", "2,3")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "todo/phase-2").is_dir())
            self.assertTrue((root / "todo/phase-3").is_dir())
            inbox = (root / "todo/inbox.md").read_text(encoding="utf-8")
            self.assertIn("## Phase 2", inbox)
            self.assertIn("## Phase 3", inbox)

    def test_board_has_all_todo_preop_mise_wip_testing_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            board = (root / "todo/_board.base").read_text(encoding="utf-8")
            self.assertIn('status != "done"', board)
            self.assertEqual(board.count("  - type: table"), 6)
            self.assertIn("name: All", board)
            self.assertIn("name: Todo", board)
            self.assertIn('stage == "todo"', board)
            self.assertIn("name: Preop", board)
            self.assertIn('stage == "preop"', board)
            self.assertIn("name: Mise", board)
            self.assertIn('stage == "mise"', board)
            self.assertIn("name: WIP", board)
            self.assertIn('stage == "wip"', board)
            self.assertIn("name: Testing", board)
            self.assertIn('stage == "test"', board)
            all_layout = view_layout(board, "All")
            for name in ("Todo", "Preop", "Mise", "WIP"):
                with self.subTest(view=name):
                    self.assertEqual(view_layout(board, name), all_layout)
            self.assertEqual(
                view_layout(board, "Testing"),
                all_layout.replace(
                    "      - stage\n", "      - stage\n      - status\n      - done\n", 1
                ),
            )
            ignored = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
            self.assertIn("/todo/.obsidian/", ignored)
            rules = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("stage: todo|preop|mise|wip|test", rules)

    def test_stage_views_keep_phase_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--phases", "2"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            board = (root / "todo/_board.base").read_text(encoding="utf-8")
            all_layout = view_layout(board, "All")
            self.assertIn("      - phase\n", all_layout)
            for name in ("Todo", "Preop", "Mise", "WIP"):
                with self.subTest(view=name):
                    self.assertEqual(view_layout(board, name), all_layout)
            self.assertEqual(
                view_layout(board, "Testing"),
                all_layout.replace(
                    "      - stage\n", "      - stage\n      - status\n      - done\n", 1
                ),
            )

    def test_existing_board_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            todo = root / "todo"
            todo.mkdir()
            board = todo / "_board.base"
            board.write_text("custom board\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(board.read_text(encoding="utf-8"), "custom board\n")


if __name__ == "__main__":
    unittest.main()
