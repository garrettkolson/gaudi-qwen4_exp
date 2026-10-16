---
id: task-p5-2-preregister-throughput-protocol
title: Pre-register the Throughput Protocol Before Each Lever
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Fix the measurement protocol before and after each P5 lever, mirroring PR seeds 301-303, so every throughput change attributes to exactly one change on Gaudi 2.
auto_inject: false
applicable_when: P5 (cust-phase-p5-moe-economics) — live before any throughput lever (P5.1 or P5.3) is switched on; the protocol must exist before the first measurement run.
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PR seeds 301-303 describe a materially different protocol than assumed, or an official vllm-gaudi benchmark harness supersedes it, the protocol must be re-registered before any further measurement counts."
tags: ["roadmap-task", "p5", "benchmark", "attribution", "throughput"]
edges: [
  {"target": "cust-phase-p5-moe-economics", "type": "part_of", "weight": 0.9, "note": "Without attribution discipline the P5 exit curve is unfalsifiable"},
  {"target": "playbook-fp8-moe-throughput-attribution", "type": "depends_on", "weight": 0.95, "note": "The playbook defines the before/after-per-lever protocol this task instantiates"},
  {"target": "pillar-measured-before-default", "type": "related_to", "weight": 0.85, "note": "Pre-registration is how this phase keeps its numbers measured rather than inherited"},
  {"target": "question-moe-saturation-point", "type": "related_to", "weight": 0.8, "note": "The protocol exists to answer where cost-per-token saturates on Gaudi 2"}
]
related: ["[[cust-phase-p5-moe-economics]]", "[[playbook-fp8-moe-throughput-attribution]]", "[[question-moe-saturation-point]]"]
source_url: "Empty"
---
# Pre-register the Throughput Protocol Before Each Lever

Before switching on any P5 lever, fix the throughput protocol — mirroring PR seeds 301-303 — with a fixed prompt set, a fixed concurrency ladder, identical seeds, and a before/after run recorded for each individual change. Pre-registration is what makes MoE attribution on Gaudi 2 possible: without it, gathered-expert combine, decode bucketing, and TP/EP changes all move the same number at once and the interaction with issue #1733 stays invisible.

Done when: a documented cost-per-token curve on Gaudi 2 across concurrency 1 to target, with an identified saturation point, is producible from the pre-registered before/after runs.
