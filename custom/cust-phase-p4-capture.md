---
id: cust-phase-p4-capture
title: "P4b — Compiled (HPU-Graph) Mode: Off Eager-Only"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Serve with --enforce-eager removed, or a documented hybrid: PR #1843 mitigations, host-coercing ops removed, P3 CustomOps meeting the capture contract."
auto_inject: false
applicable_when: "When executing roadmap phase P4b, after P4a's failure list and P3's compliant CustomOps exist"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If synStatus-26/compileGraph recurs on the target stack after the pin and the #1843 mitigations, re-open this phase and the issue-#1734 evidence"
tags: ["roadmap-phase", "p4b", "graph-capture", "hpu-graph", "enforce-eager"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P4_capture — goal, three tasks, exit criteria, known blocker"},
  {"target": "cust-phase-p4-pin-check", "type": "depends_on", "weight": 0.9, "note": "P4b's scope is defined by the remaining-failure list P4a documents"},
  {"target": "cust-phase-p3-custom-kernels", "type": "depends_on", "weight": 0.7, "note": "Soft dependency: capture needs the P3 CustomOps to meet the single-kernel + namespace contract — itself the roadmap's flagged reading"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.9, "note": "Known blocker: synStatus-26 / synapse compileGraph, issue #1734 family"},
  {"target": "hyp-customop-gates-compile-capture", "type": "related_to", "weight": 0.85, "note": "This phase is the test of the hypothesis that single-kernel + custom_op namespace unblocks capture"},
  {"target": "hyp-sparse-topk-not-capturable", "type": "related_to", "weight": 0.9, "note": "The P4.2/P4b capture attempt settles whether sparse top-k stays uncapturable"},
  {"target": "playbook-graph-capture-triage", "type": "related_to", "weight": 0.9, "note": "The triage procedure to run when a subgraph refuses capture"},
  {"target": "cust-phase-p4-pin-check", "type": "preceded_by", "weight": 0.9, "note": "Recommended order: P0 → P1 → P4_pin_check → P3 → P4_capture → P5; the cheap pin check runs first"},
  {"target": "cust-phase-p5-moe-economics", "type": "followed_by", "weight": 0.9, "note": "P5's throughput work assumes compiled mode or the documented hybrid is serving"}
]
related: ["[[ref-issue-1734-synstatus-26]]", "[[ref-pr1843-mitigations]]", "[[playbook-graph-capture-triage]]", "[[decision-eager-first-compiled-later]]"]
source_url: "Empty"
---

# P4b — Compiled (HPU-Graph) Mode: Off Eager-Only

## Goal
Serve with `--enforce-eager` removed, or a documented hybrid compiled+eager split. Integrate the PR #1843 mitigations — DS=0 concrete-plan recipe, host-side decode count fix, bmm score contraction fix, flat `index_copy_` store rewrite restoring first-request survival — eliminate host-coercing ops from the QSA/PLE hot paths, and prove the P3 CustomOps satisfy the capture contract. Known blocker: synStatus-26 / synapse `compileGraph` (issue #1734 family).

## Depends on
P4a (remaining-failure list) and, softly, P3 (capture-contract CustomOps). Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5 — the cheap pin check precedes heavy kernel authoring.

## Tasks
- [[task-p4-3-apply-pr1843-mitigations]] — integrate the four #1843 capture mitigations into the build.
- [[task-p4-4-eliminate-host-coercing-ops]] — remove .nonzero in PLE _pool_and_store, .item(), torch.minimum in _expand_plan, and keep.any() in the KV-store epilogue.
- [[task-p4-5-meet-customop-capture-contract]] — prove each P3 CustomOp is single-kernel and custom_op-namespace registered.

## Exit criteria
Boots and serves on all TP workers without `--enforce-eager`, or a documented per-subgraph eager fallback limited to the QSA indexer.
