"""The old repository's last tree: a notice that pcnotify moved to PendiFy, and an installer stub
that installs nothing, prints where the program went and leaves exit code 1."""

import hashlib
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = ROOT / "install.ps1"
README = ROOT / "README.md"
UNINSTALL = ROOT / "uninstall.ps1"
BASE = "4ebc546"

ADDRESS = "https://github.com/ElkinDev/PendiFy"
NEW_LINE = (r'powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pendify-install.ps1 -ea 0; '
            r'irm https://raw.githubusercontent.com/ElkinDev/PendiFy/main/install.ps1 -OutFile ~\pendify-install.ps1; '
            r'~\pendify-install.ps1"')
OLD_UNINSTALL_LINE = (r'powershell -NoExit -NoProfile -ExecutionPolicy Bypass -Command "ri ~\pcnotify-uninstall.ps1 -ea 0; '
                      r'irm https://raw.githubusercontent.com/ElkinDev/pcnotify/main/uninstall.ps1 '
                      r'-OutFile ~\pcnotify-uninstall.ps1; ~\pcnotify-uninstall.ps1"')
OLD_INSTALL_ROAD = "ElkinDev/pcnotify/main/install.ps1"
TREE = {".gitignore", "LICENSE", "README.md", "install.ps1", "uninstall.ps1", "tests/test_moved_notice.py"}
# What an installer does; none of it may stand in the stub outside the printed line.
FORBIDDEN = [r"\bpip\b", r"\bwinget\b", r"Start-Process", r"New-Object\s+-ComObject", r"Set-ItemProperty",
             r"\birm\b", r"Invoke-WebRequest", r"Invoke-RestMethod", r"\$env:"]
SPANISH = "Esta linea ya no instala nada"
ENGLISH = "This line installs nothing any more"

POWERSHELL = shutil.which("powershell")
GIT = shutil.which("git")


def _git(*args):
    return subprocess.run([GIT, "-C", str(ROOT), *args], capture_output=True, timeout=60)


class MovedNoticeTest(unittest.TestCase):
    """The old repository's last commit: the stub as run, its source, the README and the tree."""

    def _assert_notice(self, out):
        self.assertEqual(out.count(ADDRESS), 2, out)
        self.assertEqual(out.count(NEW_LINE), 2, out)
        self.assertIn(SPANISH, out)
        self.assertIn(ENGLISH, out)
        self.assertNotIn(OLD_INSTALL_ROAD, out)

    @unittest.skipIf(POWERSHELL is None, "Windows PowerShell is not on this machine")
    def test_run_as_a_file_exits_1_and_prints_the_new_line(self):
        done = subprocess.run([POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(INSTALL)],
                              cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self._assert_notice(done.stdout)
        self.assertEqual(done.stderr.strip(), "")

    @unittest.skipIf(POWERSHELL is None, "Windows PowerShell is not on this machine")
    def test_run_as_pasted_text_keeps_the_shell_and_leaves_lastexitcode_1(self):
        text = INSTALL.read_text(encoding="ascii") + "\n\n" + 'Write-Output "after:$LASTEXITCODE"\n\n'
        done = subprocess.run([POWERSHELL, "-NoProfile", "-Command", "-"], input=text, cwd=str(ROOT),
                              capture_output=True, text=True, timeout=120)
        self._assert_notice(done.stdout)
        # Mutation: an exit in the piped form closes the shell, so the next line never prints, red.
        self.assertIn("after:1", done.stdout, done.stdout + done.stderr)
        self.assertEqual(done.stderr.strip(), "")

    def test_install_is_ascii_and_does_nothing_but_print(self):
        raw = INSTALL.read_bytes()
        self.assertTrue(all(b < 128 for b in raw), "install.ps1 is not pure ASCII")
        source = raw.decode("ascii")
        self.assertIn(NEW_LINE, source)
        self.assertNotIn(OLD_INSTALL_ROAD, source)
        self.assertNotRegex(source, r"(?im)^\s*param\s*\(", "the stub takes parameters")
        rest = source.replace(NEW_LINE, "")
        for pattern in FORBIDDEN:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, rest, re.IGNORECASE), pattern)

    def test_readme_points_to_pendify_once_per_language_with_the_old_uninstall_line(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("pcnotify ahora es PendiFy", text)
        self.assertIn("pcnotify is now PendiFy", text)
        self.assertEqual(text.count(ADDRESS), 2, "the address once per language")
        self.assertEqual(text.count(NEW_LINE), 2, "the install line once per language")
        self.assertEqual(text.count(OLD_UNINSTALL_LINE), 2, "the old uninstall line once per language")
        self.assertNotIn(OLD_INSTALL_ROAD, text)

    @unittest.skipIf(GIT is None, "git is not on this machine")
    def test_uninstall_is_byte_for_byte_the_old_one(self):
        old = _git("show", BASE + ":uninstall.ps1")
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertEqual(hashlib.sha256(UNINSTALL.read_bytes()).hexdigest(), hashlib.sha256(old.stdout).hexdigest())

    @unittest.skipIf(GIT is None, "git is not on this machine")
    def test_tree_holds_only_the_six_paths(self):
        listed = _git("ls-files")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertEqual(set(listed.stdout.decode("utf-8").split()), TREE)


if __name__ == "__main__":
    unittest.main()
