# Create Vault Prompt

Agent-agnostic version of `/init-vault`. Use this when your agent has no slash commands: paste the prompt, or read it as the procedure.

---

You are scaffolding an Infinite Brain vault in the current directory.

1. Ask which namespace the vault should start with (for this repository the answer is already `qwen4-exp-gaudi2`).
2. Create the content folders: `pillars decisions concepts questions playbooks tasks events patterns hypotheses facts sources bookmarks notes contacts references custom raw raw/processed logs`.
3. Create `.gitkeep` in each empty folder so git tracks them.
4. Create `_system/` files: `INDEX.md`, `NODE-TYPES.md`, `EDGE-TYPES.md`, `FRONTMATTER-SCHEMA.md`, `LOCAL-TYPES.md`, `AGENTS.md`, `WORKFLOWS.md`, and the `_prompts/` folder.
5. Create `_templates/Template - Infinite Node.md`.
6. Create `CLAUDE.md` at the root pointing agents at `_system/AGENTS.md` and the skills.
7. Create two example nodes in the chosen namespace and wire them with a `supports` edge.
8. Add both rows to `_system/INDEX.md`.
9. Report: folders created, nodes wired, next step is ingestion.

## Already scaffolded

This repository is already scaffolded and seeded from `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json`. Do not re-run this procedure here — it would duplicate ids that the graph already resolves against. Use it only when creating a vault somewhere else.

Read `_system/SEED-MANIFEST.md` before adding nodes: it is the id registry, and ids that drift from it break edge resolution across the whole graph.
