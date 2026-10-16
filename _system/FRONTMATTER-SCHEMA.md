# Frontmatter Schema Reference

Every node in the vault must include a frontmatter block at the top of the markdown file. Fields marked **required** are mandatory; fields marked **optional** may be omitted but should be populated when available.

---

## Complete Field Specification

### id
- **Type:** string
- **Format:** `type-slug` in kebab-case (e.g., `hyp-creators-will-pay-29mo`)
- **Required:** yes
- **Notes:** Must be unique across the entire vault. Combine node type abbreviation with a descriptive slug. No spaces, no uppercase (except acronyms in slug). In this vault the filename is the id: `concepts/concept-gdn-gated-delta-net.md`.

### title
- **Type:** string
- **Required:** yes
- **Notes:** Human-readable, 5–80 characters. Should be recognizably unique across nodes of the same type.

### type
- **Type:** string
- **Required:** yes
- **Allowed Values:** exactly one of: `pillar`, `decision`, `concept`, `question`, `playbook`, `task`, `event`, `pattern`, `hypothesis`, `fact`, `source`, `bookmark`, `note`, `contact`, `reference`, `custom`, `log`
- **Notes:** Must match the canonical name in `NODE-TYPES.md` exactly (lowercase, singular).

### namespace
- **Type:** string
- **Required:** yes
- **Notes:** Represents the project, team, or domain area. Use kebab-case (e.g., `product-ops`, `growth`, `infra`). Enables scoped filtering and reduces cross-namespace collisions. In this vault, roadmap-derived content uses `qwen4-exp-gaudi2`; vault machinery uses `system`.

### visibility
- **Type:** string
- **Required:** yes
- **Allowed Values:** exactly one of: `public`, `namespace`, `private`, `system`
- **Default:** `namespace`
- **Notes:** Controls when an AI agent may use the node during retrieval. Use `public` for broadly reusable knowledge, `namespace` for content that should only be used inside its namespace, `private` for sensitive or personal material, and `system` for vault instructions or agent-facing operating rules.

### summary
- **Type:** string
- **Required:** yes
- **Length:** 1–2 sentences maximum (aim for under 200 characters)
- **Notes:** Written for an AI agent scanning the graph. Must convey the core idea at a glance. Avoid jargon unless defined in a concept node.

### auto_inject
- **Type:** boolean
- **Required:** yes
- **Allowed Values:** `true` or `false`
- **Notes:** When `true`, the system may automatically insert related content or triggers into this node. Default to `false` unless explicitly designed for automation hooks.

### applicable_when
- **Type:** string
- **Default:** `"Empty"`
- **Notes:** Describes the context or trigger conditions under which this node becomes relevant. Use `"Empty"` if the node is universally applicable or context-independent. For `task-*` nodes this states the phase and precondition the task becomes live in.

### confidence
- **Type:** float
- **Range:** 0.0 to 1.0
- **Required:** yes
- **Notes:** Reflects the author's confidence in the node's accuracy or validity. 1.0 = certain, 0.0 = pure speculation. Revisit and update as evidence accumulates. In this vault confidence tracks the roadmap's own provenance split: source-backed claims may sit high; author inferences flagged in `note-provenance-register` must sit at or below 0.7 until measured on Gaudi 2.

### verified_at
- **Type:** string (date)
- **Format:** `MM/DD/YYYY`
- **Default:** `"Empty"`
- **Notes:** Date on which the node's content or conclusions were last reviewed or confirmed by a human. Use `"Empty"` until first verification. Anything not measured on real Gaudi 2 hardware is not verified — it is asserted by the roadmap.

### verified_by
- **Type:** string
- **Default:** `"Empty"`
- **Notes:** Name or id of the person who last verified this node. Use `"Empty"` until verified.

### staleness_signal
- **Type:** string
- **Required:** yes
- **Notes:** A specific, observable condition that, if met, indicates this node may be outdated, incorrect, or invalidated. Write it as a conditional statement (e.g., "If revenue growth drops below 5% for two consecutive quarters, re-evaluate this assumption"). Agents should monitor for staleness signals.

### tags
- **Type:** array of strings
- **Required:** yes
- **Notes:** Array syntax: `["tag-one", "tag-two"]`. Tags are lowercase, kebab-case. Include 2–8 relevant tags. Tags are used for filtering and cross-referencing.

### edges
- **Type:** array of objects
- **Required:** yes
- **Structure:** Each object must contain exactly four keys:

| Key | Type | Notes |
|---|---|---|
| `target` | string | The `id` of the destination node |
| `type` | string | One of the 10 edge types from `EDGE-TYPES.md` |
| `weight` | float | 0.0 to 1.0, indicating relationship strength |
| `note` | string | Brief explanation of the connection |

- **Example:**

```yaml
edges: [
  {"target": "pillar-example-philosophy", "type": "related_to", "weight": 0.7, "note": "Provides grounding for this decision"}
]
```

- **Note on delimiters:** the array opens with `[` on the `edges:` line, and each object stays on one line. Never insert a blank line inside the array and never wrap object values in folded scalars — the vault linter parses these arrays literally.

### related
- **Type:** array of strings
- **Required:** no
- **Notes:** Wikilinks (`[[Node Title]]`) or bare node ids for casual cross-references that don't warrant a formal edge. Useful for discovery and browsing.

### source_url
- **Type:** string
- **Default:** `"Empty"`
- **Notes:** URL of the external resource this node was derived from, if any. Use `"Empty"` when no source applies.

---

## Example Frontmatter Block

```yaml
---
id: hyp-gaudi2-fp8-mme-throughput-gap
title: Gaudi 2 FP8 MME Throughput Trails Gaudi 3
type: hypothesis
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Gaudi 2 FP8 matrix-engine throughput is lower per card than Gaudi 3, making FP8 a feasibility path on Gaudi 2 rather than a performance claim.
auto_inject: false
applicable_when: When sizing TP degree or promising tokens-per-second on Gaudi 2
confidence: 0.55
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a P0.2 micro-benchmark on Gaudi 2 shows FP8 MME at or above Gaudi 3 per-card throughput, this hypothesis is falsified"
tags: ["gaudi-2", "fp8", "mme", "throughput"]
edges: [
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "derived_from", "weight": 0.8, "note": "FP8 existence on Gaudi 2 is confirmed; the gap is about rate, not capability"},
  {"target": "cust-risk-r1-fp8-mme-throughput", "type": "supports", "weight": 0.7, "note": "If this holds, FP8 headroom assumptions in the plan need rework"}
]
related: ["[[cust-phase-p0-platform-feasibility]]"]
source_url: "Empty"
---
```

---

## Log Node Schema

`log` nodes use a reduced schema designed for minimal token cost. Do NOT apply the full frontmatter checklist to log nodes.

### Fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | Format: `log-[operation]-[YYYYMMDD-HHmmss]` (e.g., `log-convert-note-20260515-143022`) |
| `type` | string | Always `log` |
| `operation` | string | One of: `convert-note`, `query-vault`, `organize-vault`, `vault-health`, `init-vault` |
| `date` | string | ISO 8601: `"YYYY-MM-DDTHH:MM:SS"` |
| `namespace` | string | Namespace(s) affected, or `"vault"` if global |
| `summary` | string | One sentence, under 150 chars |
| `affected_nodes` | array | Node IDs created or modified. Empty array `[]` if none. |
| `tags` | array | Always includes `"log"` and the operation name |

### Example

```yaml
---
id: log-convert-note-20260515-143022
type: log
operation: convert-note
date: "2026-05-15T14:30:22"
namespace: personal
summary: "Processed raw/karpathy-llm-wiki.md → 3 nodes created (concept, source, fact)"
affected_nodes: ["concept-llm-wiki-pattern", "source-karpathy-llm-wiki", "fact-rag-vs-compounding"]
tags: ["log", "convert-note"]
---
```

### Body

Log body should be 30–80 words. Cover: what ran, what changed, any notable finding or error. No markdown headers — plain prose.

### Rules

- Log nodes are **never edited** after creation.
- Log nodes are **not indexed** in `_system/INDEX.md` — the `logs/` folder is self-contained.
- Log nodes are **not subject to confidence decay** in `/vault-health`.
- Log nodes have `visibility: system` implicitly — agents do not use them for query answers.

---

## Field-by-Field Validation Checklist

- [ ] `id` is unique, kebab-case, prefixed with type
- [ ] `id` equals the filename (minus `.md`)
- [ ] `title` is non-empty, human-readable
- [ ] `type` matches one of the canonical types
- [ ] `namespace` is kebab-case
- [ ] `visibility` is one of `public`, `namespace`, `private`, `system`
- [ ] `summary` is 1–2 sentences, under 200 chars
- [ ] `auto_inject` is boolean
- [ ] `applicable_when` is a string or `"Empty"`
- [ ] `confidence` is between 0.0 and 1.0
- [ ] `verified_at` is MM/DD/YYYY or `"Empty"`
- [ ] `verified_by` is a string or `"Empty"`
- [ ] `staleness_signal` is a non-empty conditional string
- [ ] `tags` is a non-empty array of kebab-case strings
- [ ] `edges` is a non-empty array of objects with `target`, `type`, `weight`, `note`
- [ ] every `edges[].target` resolves to an id that exists in the vault
- [ ] `related` is an array of wikilinks or ids (optional)
- [ ] `source_url` is a URL string or `"Empty"`

Run `python _system/lint_vault.py` to check the whole vault mechanically.
