"""Check that fingerprint.luau and fingerprint.py agree.

Runs fingerprint.luau under the standalone Luau CLI against a stand-in
`game` object. Set LUAU to the Luau binary, or put `luau` on PATH.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "roblox-studio-playtest-guard" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import fingerprint  # noqa: E402

FIXTURES = {
    "Empty": b"",
    "Ascii": b"print('hello')\n",
    "Crlf": b"local a = 1\r\nlocal b = 2\r\n",
    "LoneCr": b"a\rb",
    "Utf8": "-- h\u00e9llo w\u00f6rld \u2713\n".encode(),
    "AllBytes": bytes(range(256)),
    "Large": b"x = x + 1\n" * 20000,
}

MOCK = """
local function script(name, source)
	return {
		Source = source,
		IsA = function(_, className) return className == "LuaSourceContainer" end,
		GetFullName = function() return "ServerScriptService." .. name end,
	}
end
local part = {
	IsA = function() return false end,
	GetFullName = function() return "ServerScriptService.Part" end,
}
local locked = setmetatable({
	IsA = function(_, className) return className == "LuaSourceContainer" end,
	GetFullName = function() return "ServerScriptService.Locked" end,
}, { __index = function() error("no permission") end })
local scripts = { part, locked }
%s
local serverScriptService = { GetDescendants = function() return scripts end }
local broken = { GetDescendants = function() error("no permission") end }
game = {
	GetService = function(_, name)
		if name == "ServerScriptService" then return serverScriptService end
		if name == "ServerStorage" then error("no access") end
		return broken
	end,
}
"""


def luau_string(data: bytes) -> str:
    return '"' + "".join(f"\\{b:03d}" for b in data) + '"'


def find_luau() -> str | None:
    return shutil.which(os.environ.get("LUAU", "luau"))


@unittest.skipUnless(find_luau(), "Luau CLI not found; set LUAU or add luau to PATH")
class ParityTest(unittest.TestCase):
    def test_luau_matches_python(self) -> None:
        inserts = "\n".join(
            f"table.insert(scripts, script({name!r}, {luau_string(data)}))".replace("'", '"')
            for name, data in FIXTURES.items()
        )
        body = (SCRIPTS / "fingerprint.luau").read_text().replace("--!strict", "", 1)
        with tempfile.TemporaryDirectory() as tmp:
            program = Path(tmp) / "run.luau"
            program.write_text(MOCK % inserts + body)
            result = subprocess.run([find_luau(), str(program)], capture_output=True, text=True, check=True)

            files = []
            for name, data in FIXTURES.items():
                path = Path(tmp) / name
                path.write_bytes(data)
                files.append(str(path))
            disk = subprocess.run(
                [sys.executable, str(SCRIPTS / "fingerprint.py"), *files],
                capture_output=True,
                text=True,
                check=True,
            )

        studio = [line.split("\t") for line in result.stdout.splitlines()]
        names = [row[0] for row in studio]
        self.assertEqual(names, sorted(f"ServerScriptService.{name}" for name in FIXTURES))

        on_disk = {Path(row[0]).name: row[1:] for row in (line.split("\t") for line in disk.stdout.splitlines())}
        for full_name, length, digest in studio:
            name = full_name.split(".", 1)[1]
            with self.subTest(name=name):
                self.assertEqual([length, digest], on_disk[name])


class HashTest(unittest.TestCase):
    def test_known_fnv1a_values(self) -> None:
        self.assertEqual(fingerprint.fnv1a(b""), 0x811C9DC5)
        self.assertEqual(fingerprint.fnv1a(b"a"), 0xE40C292C)
        self.assertEqual(fingerprint.fnv1a(b"foobar"), 0xBF9CF968)

    def test_crlf_reads_as_lf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            crlf = Path(tmp) / "crlf"
            lf = Path(tmp) / "lf"
            crlf.write_bytes(b"a\r\nb\r\n")
            lf.write_bytes(b"a\nb\n")
            out = subprocess.run(
                [sys.executable, str(SCRIPTS / "fingerprint.py"), str(crlf), str(lf)],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.splitlines()
        self.assertEqual(out[0].split("\t")[1:], out[1].split("\t")[1:])


if __name__ == "__main__":
    unittest.main()
