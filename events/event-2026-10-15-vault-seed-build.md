---
id: event-2026-10-15-vault-seed-build
title: Vault Seeded from the Roadmap (111 Nodes)
type: event
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "2026-10-15: the v1.1 baseline was converted into 111 typed content nodes with ids registered in SEED-MANIFEST. Nothing seeded is verified — no Gaudi 2 measurement exists."
auto_inject: false
applicable_when: "When auditing vault completeness, reconciling node counts, or deciding whether a missing node is a gap or a deliberate non-seed"
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If _system/INDEX.md no longer counts 111 content nodes without a logged conversion event explaining the difference, or a roadmap v1.2 baseline lands, these totals and this coverage statement are stale"
tags: ["event", "seed-build", "vault", "node-count", "coverage"]
edges: [
  {"target": "event-2026-10-15-roadmap-baseline-v1-1", "type": "preceded_by", "weight": 0.9, "note": "The seed converts the adopted baseline; adoption came first on the same date"},
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Every seeded node was synthesized from this immutable copy, nothing else"},
  {"target": "note-seed-coverage-and-gaps", "type": "related_to", "weight": 0.9, "note": "That note records what this build could not convert: PR diffs, release notes, the HCCL table, and zero measurements"}
]
related: ["[[event-2026-10-15-roadmap-baseline-v1-1]]", "[[note-seed-coverage-and-gaps]]", "[[source-roadmap-qwen4-exp-gaudi2-v1-1]]"]
source_url: "Empty"
---
# Vault Seeded from the Roadmap (111 Nodes)

On 2026-10-15 the v1.1 baseline was converted into this vault: 111 content nodes — 4 pillars, 8 phases, 6 risks, 27 tasks, 7 decisions, 10 facts, 5 hypotheses, 5 questions, 11 concepts, 5 playbooks, 8 references, 7 sources, 4 bookmarks, 2 events, 2 notes. Ids were registered in `_system/SEED-MANIFEST.md` before files were written, so edges authored later point at names other agents will honour.

What this makes true: the roadmap's phases, tasks, risks and provenance split are traversable as typed nodes and edges — an agent can ground itself by walking `depends_on` upstream instead of reading prose. Nothing seeded carries `verified_at`; confidence follows the roadmap's evidence-versus-inference split, and `patterns/` and `contacts/` were left empty on purpose because nothing has survived a Gaudi 2 run and the roadmap names no people.

What it triggers next: converting the four bookmarks as their `raw/` inputs arrive (PR #1829 diff, PR #1843 diff, HCCL primitives table, TPC SDK guide), then running P0, whose numbers become the first facts and the first real verifications.
