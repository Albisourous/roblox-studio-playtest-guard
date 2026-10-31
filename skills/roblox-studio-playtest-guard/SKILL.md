---
name: roblox-studio-playtest-guard
description: Check that a Roblox Studio playtest runs your current scripts and has actually stopped before you trust its results.
---

# Roblox Studio playtest guard

Use this skill when you test a Roblox experience in Studio, for example through the Studio MCP server, and plan to report what happened in Play. Two Studio behaviors can make a bad run look good:

- Play can load older scripts than the ones on disk while Edit mode matches disk.
- A stop call can report "Game Stopped" while Studio is still in Play.

Tool names below (`start_stop_play`, `get_studio_state`, `execute_luau`, `list_roblox_studios`) come from Roblox's built-in Studio MCP server. If your client names them differently, use its equivalents.

## Fingerprint scripts

`scripts/fingerprint.luau` prints one line per script in Studio: full name, byte length, and a 32-bit FNV-1a hash. Run its contents with `execute_luau` in the datamodel you want to check. `scripts/fingerprint.py` prints the same length and hash for files on disk:

```sh
python3 scripts/fingerprint.py src/server/Main.server.luau src/shared/Config.luau
```

Both read CRLF as LF, so line endings do not cause false mismatches. Match each file to its instance with your sync tool's project file (for Rojo, `default.project.json`).

## Before you count a result

1. In Edit mode, fingerprint the scripts you changed and compare them with disk. Every changed script must match.
2. Start Play. Fingerprint again in the Server datamodel, then in the Client datamodel.
3. Compare both Play lists with the Edit list. Scripts that Studio copies when Play starts, such as StarterPlayerScripts into PlayerScripts or StarterGui into PlayerGui, show up under a new path. Match those by name.
4. If a changed script differs in either datamodel, the run is invalid. Count no UI checks, console output, or assertions from it. Report which scripts differ and in which datamodel.

A matching Edit list does not prove what Play is running. A value read through `require` does not prove it either, since a required module keeps the version it loaded first.

Report a mismatch as unexplained until you show its cause. A sync server serving an old checkout, a second sync server on another port, and Studio reconnecting to an old session are all possible causes. Check the ones you can see and say which ones you could not check.

## After you stop Play

1. After `start_stop_play`, confirm the real state. `get_studio_state` must report Edit, and `RunService:IsRunning()` must return `false`.
2. If Studio is still in Play, click Studio's own Stop button in the window that runs this place, then confirm the state again.
3. Fingerprint Edit against disk again. Edit source can differ from disk after a stop even when it matched before Play.
4. The Studio instance ID can change on every play or stop. If a call says the instance is not connected, run `list_roblox_studios` and use the new ID.
