# Query Vault Prompt

Agent-agnostic version of `/query-vault`. Use this when your agent has no slash commands. This is the procedure a working agent uses to answer project questions from the graph instead of reading the whole vault.

---

You are answering a question by traversing the knowledge graph, not by reading everything.

1. Take the question.
2. Read `_system/INDEX.md` for the map of nodes and their summaries.
3. Scope the retrieval:
   - Namespace named → prefer that namespace's nodes.
   - No namespace → use `public` nodes; use `namespace` nodes only where the summary clearly matches.
   - Explicit private request → `private` nodes are in scope.
   - Never present `system`-visibility nodes as answer content.
4. Pick likely types by question shape:
   - "why" → `pillar`, `decision`
   - "how" → `playbook`, `pattern`
   - "what if / is this true" → `hypothesis`
   - "what is / how much" → `concept`, `fact`
   - "when" → `event`, `note`
   - "who" → `contact`
   - "what don't we know" → `question`
5. Traverse edges rather than scanning files:
   - `supports` / `contradicts` → find the polarised positions
   - `depends_on` → find what must be true first
   - `derived_from` → trace a conclusion back to its evidence
6. Read only the nodes whose summary, `applicable_when`, namespace and visibility actually match.
7. Answer in this shape:

```
### Answer
<direct answer, 1-3 paragraphs>

### Sources
- `[[node-id]]` — what it contributed

### Confidence
<average of the source nodes' confidence>

### Related Nodes to Explore
- `[[node-id]]` — why it matters
```

8. Ask whether to save the answer as a synthesis node.
9. Write one log node `logs/log-query-vault-YYYYMMDD-HHmmss.md` (reduced log schema; `affected_nodes` = ids actually read; body 30-80 words).

## Rules for this project

- If any load-bearing node has `confidence` below 0.7, say so explicitly and name the node carrying the uncertainty.
- Never present a `hyp-*` node as an established constraint — it is untested by definition.
- Cite node ids, not just titles, so the next agent opens exactly what you opened.
- Prefer `playbook-*` nodes when the question is procedural; they encode the checks and the stop conditions, not just the steps.
