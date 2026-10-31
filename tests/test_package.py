"""Check that the plugin manifests, the skill, and the changelog agree."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "roblox-studio-playtest-guard"


def skill_frontmatter() -> dict[str, str]:
    text = (ROOT / "skills" / NAME / "SKILL.md").read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert match, "SKILL.md must start with YAML frontmatter"
    return dict(line.split(": ", 1) for line in match.group(1).splitlines())


class PackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = skill_frontmatter()
        self.devin = json.loads((ROOT / ".devin-plugin" / "plugin.json").read_text())
        self.claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())["plugins"][0]

    def test_names_match(self) -> None:
        self.assertEqual(self.skill["name"], NAME)
        for manifest in (self.devin, self.claude, self.market):
            self.assertEqual(manifest["name"], NAME)

    def test_descriptions_match(self) -> None:
        for manifest in (self.devin, self.claude, self.market):
            self.assertEqual(manifest["description"], self.skill["description"])

    def test_versions_match_changelog(self) -> None:
        changelog = (ROOT / "CHANGELOG.md").read_text()
        latest = re.search(r"^## (\d+\.\d+\.\d+)", changelog, re.M)
        assert latest, "CHANGELOG.md needs a '## X.Y.Z' heading"
        for manifest in (self.devin, self.claude, self.market):
            self.assertEqual(manifest["version"], latest.group(1))


if __name__ == "__main__":
    unittest.main()
