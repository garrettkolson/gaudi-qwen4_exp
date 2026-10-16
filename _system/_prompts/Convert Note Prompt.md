# Convert Note Prompt

Agent-agnostic version of `/convert-note`. Use this when your agent has no slash commands.

---

You are ingesting raw content from `raw/` into the knowledge graph.

1. Ask which file in `raw/` to convert, or "all".
2. Read the target file(s). Treat them as immutable — never modify or delete a `raw/` file.
3. Decompose into atomic nodes: one idea per node, 50-300 words each. Err toward more nodes, never merge two concepts into one.
4. For each node:
   - Pick exactly one type: `pillar decision concept question playbook task event pattern hypothesis fact source bookmark note contact reference custom`
   - Assign a unique `id` as `type-descriptive-slug`, kebab-case. The filename is the id.
   - Fill every required field from `_system/FRONTMATTER-SCHEMA.md`.
   - Wire at least one edge using the ten types in `_system/EDGE-TYPES.md`, with an honest weight and a specific note.
   - Write it to the folder matching its type (`type: concept` → `concepts/<id>.md`).
5. Append each new node's row to `_system/INDEX.md` under the right type heading.
6. Copy — do not move — nothing; move the processed original from `raw/` to `raw/processed/` with its dated filename preserved.
7. Write one log node to `logs/log-convert-note-YYYYMMDD-HHmmss.md` with the reduced 8-field log schema: operation, date, namespace, summary under 150 chars, `affected_nodes` listing every created id, tags `["log", "convert-note"]`. Body 30-80 words of plain prose.
8. Confirm what was converted, where the original moved, and that the log was written.

## Rules

- Summaries under 200 characters; no placeholder text.
- `confidence` reflects what the source actually establishes. In this project nothing counts as verified until it is measured on Gaudi 2 hardware — a document is not verification.
- `staleness_signal` is a specific observable condition, never "when things change".
- Never create a node with `type: raw`.
- Check `_system/INDEX.md` first; duplicate ids break traversal.
- Custom subtypes must be registered in `_system/LOCAL-TYPES.md` before use.
- Run `python _system/lint_vault.py` when finished; unresolved edge targets are defects, not warnings.
