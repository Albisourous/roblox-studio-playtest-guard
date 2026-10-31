# roball-studio-runtime-identity

An agent skill for testing Roblox games (built for [RoBall3D](https://github.com/Albisourous/RoBall3D)) through Roblox Studio and the Studio MCP server. It catches two failure modes that make Studio play-tests report false results:

1. **Mismatched runtime source.** Edit-mode and editor-source fingerprints can match the files on disk while the Server and Client scripts actually running in Play differ. The skill tells the agent to compare *runtime* fingerprints before trusting any UI result, and not to blame Rojo for the mismatch without evidence.
2. **Misleading stop acknowledgments.** Studio MCP can return "Game Stopped" while `get_studio_state` still reports Play. The skill tells the agent to confirm Studio is really back in Edit mode after stopping, and not to treat the acknowledgment as cleanup.

The full skill is in [`skills/roball-studio-runtime-identity/SKILL.md`](skills/roball-studio-runtime-identity/SKILL.md).

## Install

### Devin

Install the repo as a plugin, either by asking Devin:

> Install the plugin https://github.com/Albisourous/roball-studio-runtime-identity

or through **Settings → Plugins → Install from URL** with that same URL. The skill then shows up as `roball-studio-runtime-identity`.

### Claude Code

```sh
/plugin marketplace add Albisourous/roball-studio-runtime-identity
/plugin install roball-studio-runtime-identity@roball-studio-runtime-identity
```

You can also copy the skill folder by hand:

```sh
git clone https://github.com/Albisourous/roball-studio-runtime-identity
cp -r roball-studio-runtime-identity/skills/roball-studio-runtime-identity ~/.claude/skills/
```

### Other agents

`SKILL.md` is plain Markdown with YAML frontmatter (`name`, `description`), so any agent that reads `skills/<name>/SKILL.md` can load it. Copy the folder into that agent's skills directory.

## Layout

```
.devin-plugin/plugin.json      Devin plugin manifest
.claude-plugin/plugin.json     Claude Code plugin manifest
.claude-plugin/marketplace.json  Claude Code marketplace entry
skills/roball-studio-runtime-identity/SKILL.md
```

## Contributing

Issues and PRs are welcome. If you hit another Studio/MCP case where the reported state doesn't match what's actually running, open an issue with the steps to reproduce it.

## License

[MIT](LICENSE)
