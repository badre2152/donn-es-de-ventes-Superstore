"""Check that local database credentials are not tracked."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositorySecurityTests(unittest.TestCase):
    def test_database_env_is_not_tracked(self):
        files = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True
        ).splitlines()
        self.assertNotIn("testdb/data.env", files)
        self.assertFalse(any(path.endswith(".env") for path in files))

    def test_safe_configuration_template(self):
        template = ROOT / "testdb" / ".env.example"
        content = template.read_text(encoding="utf-8")
        self.assertIn("DB_PASSWORD=replace_with_local_password", content)


if __name__ == "__main__":
    unittest.main()
