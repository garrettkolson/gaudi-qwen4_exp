# Vault Workflows

Agent-agnostic workflow definitions for Infinite Brain automation. Each workflow can be triggered by any agent that supports scheduled tasks or cron execution.

---

## vault-health

**Trigger:** Weekly (recommended: Monday morning)
**Skill:** `/vault-health`
**Output:** `notes/note-vault-health-YYYYMMDD.md` + updated `_system/INDEX.md`

**What it does:**
1. Applies confidence decay to nodes not verified in 90+ days
2. Audits orphans, contradictions, stale signals, cross-link gaps, taxonomy, visibility, and summary quality
3. Writes a structured health report as a `note` node
4. Presents priority actions for human approval before executing any fix

**Two modes:**
- `/vault-health` — interactive: decay + audit + ask before each fix
- `/vault-health auto` — automated: decay + audit + report node only, zero fixes, zero prompts

**Setup by agent:**

### Claude Code
```bash
# Run once to register the weekly schedule (auto mode, no prompts):
/schedule weekly /vault-health auto
```

### GitHub Actions
Create `.github/workflows/vault-health.yml` — triggers the scheduled agent remotely via Claude Code CLI on a cron. See the GITHUB-ACTIONS section below.

### Cursor / Gemini CLI / Copilot / DSH
Manually invoke `_system/_prompts/Organize Vault Prompt.md` + apply decay rules from `.claude/skills/vault-health.md` Phase 1. The skill file is readable by any agent, and this repository is worked on by harness agents that have no slash commands — the skill text is the contract for them too.

---

## convert-note (on-demand, not scheduled)

**Trigger:** Manual — run after dropping files into `raw/`
**Skill:** `/convert-note`
**Output:** New typed nodes in their respective folders + updated `_system/INDEX.md`

No automation recommended — conversion requires human review of type classification.

Expected future inputs for this vault: vllm-gaudi PR #1829 and #1843 descriptions and diffs, plugin v0.30.0 release notes, HCCL benchmark output, P0.2 FP8 micro-benchmark numbers. Each one converts into facts that raise (or kill) the confidence of the `hyp-*` nodes seeded from the roadmap.

---

## lint (cheap, run before any commit touching the vault)

**Trigger:** Any change to a node file.
**Command:** `python _system/lint_vault.py`

Checks that every `edges[].target` resolves to a real node id, that filenames match ids, that required frontmatter fields exist, and that no `raw/` file has been modified in place. Fix before committing — an unresolved edge target silently breaks graph traversal for the next agent.

---

## GITHUB-ACTIONS

To run `vault-health` as a GitHub Action (requires Claude Code CLI installed in the runner):

```yaml
# .github/workflows/vault-health.yml
name: Vault Health

on:
  schedule:
    - cron: '0 8 * * 1'   # Every Monday at 08:00 UTC
  workflow_dispatch:        # Manual trigger

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run vault-health skill
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          claude --print --skill vault-health auto
      - name: Commit health report
        run: |
          git config user.name "vault-health[bot]"
          git config user.email "vault-health@users.noreply.github.com"
          git add notes/ _system/INDEX.md
          git diff --cached --quiet || git commit -m "chore: vault health report $(date +%Y-%m-%d)"
          git push
```

> **Note:** `--skill vault-health` requires Claude Code CLI to support skill invocation via flag. Check current CLI docs — fallback is to pass the skill content as `--system-prompt`.

---

## Workflow Principles

1. **Automated phases never delete.** Decay modifies `confidence`. Audit only collects. Fixes require human approval.
2. **Every automated run writes a node.** The health report in `notes/` creates an audit trail inside the vault itself.
3. **Workflows are additive.** New automation should write nodes, not overwrite them. Old health reports are preserved with their date in the ID.
4. **A measurement is an event.** When a benchmark finishes, write the number into a `fact-*` node, raise or lower the confidence of the `hyp-*` nodes it touches, and let the risks that depended on that hypothesis update through their edges.
