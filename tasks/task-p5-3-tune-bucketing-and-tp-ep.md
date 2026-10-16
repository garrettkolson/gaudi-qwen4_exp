---
id: task-p5-3-tune-bucketing-and-tp-ep
title: Tune Decode Bucketing; Treat Higher TP/EP as Measured
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Tune decode bucketing; consider TP/EP above PR #1829's Gaudi 3 TP4 default only if P0.5 measured HCCL all2all bandwidth supports it — EP MoE is all2all dispatch/combine.
auto_inject: false
applicable_when: P5 (cust-phase-p5-moe-economics) — live once P0.5 has recorded measured allreduce/allgather/all2all bandwidth and the pre-registered protocol (P5.2) is in place.
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P0.5 measured all2all bandwidth materially below the allreduce baseline, higher TP/EP drops out of scope and only bucketing remains; if it materially exceeds it, the candidate set widens and this task must be re-scoped."
tags: ["roadmap-task", "p5", "bucketing", "tp-ep", "all2all"]
edges: [
  {"target": "cust-phase-p5-moe-economics", "type": "part_of", "weight": 0.9, "note": "Topology and bucketing tuning complete the P5 lever set"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "depends_on", "weight": 0.9, "note": "The measured all2all number gates whether higher TP/EP is admissible at all"},
  {"target": "hyp-all2all-enables-expert-parallel", "type": "related_to", "weight": 0.9, "note": "EP becomes viable only if this unmeasured hypothesis survives the P0.5 numbers"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.85, "note": "R6 is the exposure: weak all2all forces the pure-TP (allreduce/allgather) fallback"},
  {"target": "decision-tp-ep-measured-not-default", "type": "related_to", "weight": 0.9, "note": "Implements the decision that TP/EP come from measurement, not the Gaudi 3 TP4 default"}
]
related: ["[[cust-phase-p5-moe-economics]]", "[[task-p0-5-benchmark-hccl-collectives]]", "[[decision-tp-ep-measured-not-default]]"]
source_url: "Empty"
---
# Tune Decode Bucketing; Treat Higher TP/EP as Measured

Tune decode block bucketing, and treat higher TP degree or expert parallelism as a measured decision gated on the P0.5 HCCL numbers — not a default lever. EP MoE is an all-to-all dispatch/combine pattern over the interconnect, so expect TP/EP beyond PR #1829's Gaudi 3 TP4 only if measured all2all supports it; if all2all is weak, stay on pure TP using allreduce/allgather only. Each bucketing or topology change runs through the pre-registered before/after protocol.

Done when: the documented cost-per-token curve on Gaudi 2 across concurrency 1 to target identifies the saturation point for the chosen bucketing and TP/EP topology.
