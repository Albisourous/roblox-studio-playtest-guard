#!/usr/bin/env python3
"""Print the byte length and FNV-1a 32-bit hash of each script file.

The output matches fingerprint.luau, so a file on disk can be compared
with the Source Studio has loaded. CRLF is read as LF on both sides.

Usage: fingerprint.py FILE [FILE ...]
"""

from __future__ import annotations

import sys


def fnv1a(data: bytes) -> int:
    h = 2166136261
    for byte in data:
        h ^= byte
        h = (h * 16777619) % 2**32
    return h


def main(paths: list[str]) -> int:
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    for path in paths:
        with open(path, "rb") as f:
            data = f.read().replace(b"\r\n", b"\n")
        print(f"{path}\t{len(data)}\t{fnv1a(data):08x}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
