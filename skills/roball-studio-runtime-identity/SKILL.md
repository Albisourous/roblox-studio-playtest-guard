---
name: roball-studio-runtime-identity
description: Guard RoBall3D Studio tests against mismatched runtime source and misleading stop acknowledgments.
---

Edit and editor-source fingerprints can match current disk while Server and
Client Source during Play differ. Compare runtime fingerprints before counting
UI results; do not infer that Rojo caused the mismatch.

Studio MCP returned “Game Stopped” while get_studio_state still reported Play.
Confirm actual Edit mode after stopping. In this run one explicitly scoped
native Stop click restored Edit; do not assume a stop acknowledgment is cleanup.
