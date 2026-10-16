---
id: cust-phase-p5-moe-economics
title: "P5 — Throughput for Gaudi 2 MoE Economics"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Usable serving speed despite issue #1733 low-batch MoE slowness: gathered-expert combine, pre-registered attribution protocol, measured TP/EP and bucketing."
auto_inject: false
applicable_when: "When executing roadmap phase P5, after P4b serves and P2 keeps memory stable"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a measured cost-per-token curve contradicts the exit-criteria shape, or plugin features (gathered-expert combine, bucket clamp) regress, re-plan the levers"
tags: ["roadmap-phase", "p5", "moe", "throughput", "expert-parallel"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P5 — goal, three tasks, exit criteria"},
  {"target": "cust-phase-p4-capture", "type": "depends_on", "weight": 0.9, "note": "Throughput is measured on what P4b actually serves — compiled or documented hybrid"},
  {"target": "cust-phase-p2-cache-plumbing", "type": "depends_on", "weight": 0.8, "note": "Concurrency sweeps need P2's stable memory footprint first"},
  {"target": "cust-risk-r4-1733-lowbatch-moe", "type": "related_to", "weight": 0.9, "note": "R4 (#1733 low-batch MoE slowness dominating end-to-end) is the economic problem this phase exists to beat"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.85, "note": "Higher TP/EP is only a lever if P0.5 measured all2all bandwidth supports it"},
  {"target": "question-moe-saturation-point", "type": "related_to", "weight": 0.9, "note": "The cost-per-token curve this phase produces answers where saturation sits"},
  {"target": "playbook-fp8-moe-throughput-attribution", "type": "related_to", "weight": 0.9, "note": "The pre-registered protocol for attributing speed changes to a single lever"},
  {"target": "cust-phase-p6-feature-parity", "type": "followed_by", "weight": 0.7, "note": "P6's optional features are deferred behind this phase's text-only economics"}
]
related: ["[[cust-risk-r4-1733-lowbatch-moe]]", "[[playbook-fp8-moe-throughput-attribution]]", "[[question-moe-saturation-point]]", "[[decision-tp-ep-measured-not-default]]"]
source_url: "Empty"
---

# P5 — Throughput for Gaudi 2 MoE Economics

## Goal
Usable serving speed given issue #1733 low-batch MoE slowness on Gaudi 2. Apply the opt-in gathered-expert MoE combine for FP8 (plugin v0.30.0, in the spirit of the Qwen3.5/3.6 MoE work), pre-register the throughput protocol mirroring PR seeds 301-303 before and after each lever so gains are attributable, and tune decode bucketing — with higher TP / expert-parallelism treated as a measured decision gated on P0.5 all2all bandwidth, never a default lever.

## Depends on
P4b (compiled or documented-hybrid serving) and P2 (stable concurrency footprint). Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5 — the cheap pin check precedes heavy kernel authoring.

## Tasks
- [[task-p5-1-gathered-expert-moe-combine]] — enable the opt-in gathered-expert MoE combine for FP8.
- [[task-p5-2-preregister-throughput-protocol]] — fix the measurement protocol before pulling any lever; mirrors PR seeds 301-303.
- [[task-p5-3-tune-bucketing-and-tp-ep]] — tune decode bucketing; consider higher TP/EP only where measured all2all supports it.

## Exit criteria
A documented cost-per-token curve on Gaudi 2 across concurrency 1→target with an identified saturation point.
