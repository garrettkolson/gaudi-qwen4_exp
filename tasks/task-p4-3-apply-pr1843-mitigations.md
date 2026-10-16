---
id: task-p4-3-apply-pr1843-mitigations
title: Integrate PR #1843 Capture Mitigations
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Port the PR #1843 capture mitigations — DS=0 concrete-plan recipe, host-side decode count fix, bmm score contraction fix, flat index_copy_ store rewrite — into the Gaudi 2 port.
auto_inject: false
applicable_when: P4b (cust-phase-p4-capture) — live once the P4a boot without --enforce-eager has recorded which subgraphs still fail and compiled-mode work begins.
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the plugin 0.30.0 line already carries the PR #1843 changes, or the PR is superseded or closed unmerged, this integration becomes a no-op and must be re-scoped against the current tree."
tags: ["roadmap-task", "p4-capture", "graph-capture", "pr-1843", "hpu-graph"]
edges: [
  {"target": "cust-phase-p4-capture", "type": "part_of", "weight": 0.9, "note": "One of the three P4b tasks toward serving with --enforce-eager removed"},
  {"target": "source-vllm-gaudi-pr1843", "type": "derived_from", "weight": 0.9, "note": "Task content is the mitigation list as stated in PR #1843; the diff itself is still an unprocessed bookmark"},
  {"target": "ref-pr1843-mitigations", "type": "depends_on", "weight": 0.9, "note": "The reference node carries the itemized mitigations this task applies"},
  {"target": "concept-graph-capture-vs-eager", "type": "related_to", "weight": 0.8, "note": "The mitigations target HPU graph-capture failures on the path off eager-only serving"}
]
related: ["[[cust-phase-p4-capture]]", "[[playbook-graph-capture-triage]]", "[[bookmark-pr1843-diff]]"]
source_url: "Empty"
---
# Integrate PR #1843 Capture Mitigations

Integrate the PR #1843 mitigations into the port as written: the DS=0 concrete-plan recipe, the host-side decode count fix, the bmm score contraction fix, and the flat `index_copy_` store rewrite that restores first-request survival. These are recorded repairs for HPU graph-capture failures observed while removing --enforce-eager; on Gaudi 2 the same capture path runs through synapse, so skipping any one of them re-imports a documented failure mode. Land each mitigation as a discrete change, re-attempt a capture boot, and keep what holds.

Done when: the server boots and serves on all TP workers without --enforce-eager, or there is a documented per-subgraph eager fallback for the QSA indexer only.
