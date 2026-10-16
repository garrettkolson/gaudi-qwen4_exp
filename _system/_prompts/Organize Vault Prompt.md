# Organize Vault Prompt

Agent-agnostic version of `/organize-vault` and `/vault-health`. Use this when your agent has no slash commands.

---

You are auditing the graph for health problems. Collect findings first; fix nothing without approval.

0. Run `python _system/lint_vault.py` and fold its findings into checks 1 and 3. An unresolved edge target is a defect, not a suggestion.
1. Read `_system/INDEX.md` as the baseline.
2. Run the eight checks below.
3. Deliver the report.
4. Ask which actions to execute. Never auto-fix.

## Checks

1. **Orphan census** — nodes with zero edges and zero `related`. Suggest 2-3 concrete connection targets with edge types per orphan.
2. **Contradiction scan** — conflicting claims within one namespace. Report as `[a] contradicts [b] about [topic]`.
3. **Confidence gaps** — missing, zero, or content-inconsistent `confidence`; high confidence sitting on a triggered `staleness_signal`.
4. **Stale nodes** — `verified_at` older than 90 days; priority order pillars > decisions > facts > patterns > hypotheses.
5. **Cross-link opportunities** — nodes sharing 2+ tags with no edge between them; propose the type and weight.
6. **Taxonomy health** — tag spelling drift and near-duplicate tags worth merging.
7. **Visibility health** — missing `visibility`, or sensitivity that no longer matches the setting.
8. **Summary quality** — over 200 chars, placeholder text, or a summary that no longer matches the body.

## Output format

```
## Vault Health — [Date]

### Summary
- Total nodes: XX | Orphans: XX | Contradictions: XX | Stale: XX | Cross-links: XX

### Priority Actions (Top 5)
1. [ ] [high] ...

### Details
| File | Issue | Suggested fix |
```

## After execution

Write one log node `logs/log-organize-vault-YYYYMMDD-HHmmss.md` with the reduced log schema: `affected_nodes` = ids modified (empty if none approved), summary naming node count / issue count / fixes applied, body 30-80 words.

## Project-specific notes

- Nodes carrying `verified_at: "Empty"` are not stale — in this project they are honestly unmeasured. Confidence decay skips them by design.
- A node whose `staleness_signal` has actually fired (a benchmark contradicted it, a plugin release superseded it) is the highest-value finding this audit can produce. Surface those before cosmetic issues.
