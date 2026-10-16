---
id: task-p5-1-gathered-expert-moe-combine
title: Enable Gathered-Expert MoE Combine for FP8
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Apply the opt-in gathered-expert MoE combine for FP8 shipped in plugin v0.30.0 as the first P5 lever against issue #1733 low-batch MoE slowness on Gaudi 2.
auto_inject: false
applicable_when: P5 (cust-phase-p5-moe-economics) — live once P4b has removed --enforce-eager, P2 is stable, and a pre-registered throughput protocol (P5.2) is in place.
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If gathered-expert combine becomes the default or is removed in a later plugin release, or pre/post measurement shows no FP8 MoE gain on Gaudi 2, this lever is obsolete and must be dropped from the plan."
tags: ["roadmap-task", "p5", "moe", "fp8", "throughput"]
edges: [
  {"target": "cust-phase-p5-moe-economics", "type": "part_of", "weight": 0.9, "note": "First throughput lever of P5 toward the cost-per-token curve"},
  {"target": "fact-plugin-0-30-0-features", "type": "depends_on", "weight": 0.9, "note": "The feature exists only because plugin v0.30.0 ships the gathered-expert MoE combine"},
  {"target": "cust-risk-r4-1733-lowbatch-moe", "type": "related_to", "weight": 0.85, "note": "Named mitigation for #1733 low-batch MoE slowness dominating end-to-end throughput"},
  {"target": "concept-moe-expert-parallel-vs-tp", "type": "related_to", "weight": 0.8, "note": "The combine pattern sits in the MoE dispatch/combine space this concept maps"}
]
related: ["[[cust-phase-p5-moe-economics]]", "[[ref-issue-1733-low-batch-moe]]", "[[fact-plugin-0-30-0-features]]"]
source_url: "Empty"
---
# Enable Gathered-Expert MoE Combine for FP8

Apply the opt-in gathered-expert MoE combine for FP8 that plugin v0.30.0 ships, in the spirit of the Qwen3.5/3.6 MoE work. It is the direct lever against issue #1733 — MoE slowness at low batch that can dominate end-to-end throughput on Gaudi 2, where the FP8 matrix-engine rate is already expected to trail Gaudi 3. Because it is opt-in, measure it only behind the pre-registered protocol so its effect is attributable to this lever alone.

Done when: a documented cost-per-token curve on Gaudi 2 across concurrency 1 to target exists, with the saturation point identified, covering the combine on and off.
