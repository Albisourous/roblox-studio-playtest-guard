# Roblox Studio playtest guard

An agent skill for testing Roblox experiences in Studio. Before an agent reports what happened in Play, it checks two things:

- Play is running the scripts on disk. Studio can load older Server or Client scripts while Edit mode matches disk.
- Studio really left Play. The Studio MCP stop call can return "Game Stopped" while Studio stays in Play.

It works with any Roblox experience and any sync setup (Rojo, Argon, or plain Studio edits). The checks use Roblox's built-in Studio MCP server, but the steps also work by hand from the command bar.

## Requirements

- Roblox Studio. For agent use, turn on Assistant, Manage MCP Servers, "Enable Studio as MCP server".
- Python 3.8 or newer for `fingerprint.py`.

## What's in it

```
skills/roblox-studio-playtest-guard/SKILL.md                    the steps the agent follows
skills/roblox-studio-playtest-guard/scripts/fingerprint.luau    length and hash of every script in a Studio datamodel
skills/roblox-studio-playtest-guard/scripts/fingerprint.py      the same length and hash for files on disk
```

The two fingerprint scripts give the same output for the same source, so you can compare disk, Edit, Server, and Client line by line.

## Install

### Devin

Ask Devin to install the plugin from `https://github.com/Albisourous/roblox-studio-playtest-guard`, or add that URL under Settings, Plugins.

### Claude Code

```sh
/plugin marketplace add Albisourous/roblox-studio-playtest-guard
/plugin install roblox-studio-playtest-guard@roblox-studio-playtest-guard
```

### Other agents

Copy `skills/roblox-studio-playtest-guard` into your agent's skills folder:

```sh
git clone https://github.com/Albisourous/roblox-studio-playtest-guard
cp -r roblox-studio-playtest-guard/skills/roblox-studio-playtest-guard ~/.claude/skills/
```

Replace `~/.claude/skills/` with the skills folder your agent reads.

## Use without an agent

1. In Edit mode, paste `fingerprint.luau` into the Studio command bar and run it.
2. Run `python3 fingerprint.py` on the files you changed and compare the lines.
3. Start Play, run `fingerprint.luau` again on the Server and on the Client, and compare.

If a script you changed has a different length or hash in Play, the playtest is running old code.

## Contributing

Run the checks before you open a pull request. The parity test needs the [Luau CLI](https://github.com/luau-lang/luau/releases) on your PATH, or its path in `LUAU`:

```sh
python3 -m unittest discover -s tests -v
stylua --check skills
selene skills
```

Open an issue if you find another case where Studio reports one state and runs another. Include the steps to reproduce it.

Release notes are in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
