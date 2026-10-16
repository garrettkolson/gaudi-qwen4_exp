---
id: hyp-all2all-enables-expert-parallel
title: HCCL All2All Bandwidth Is Sufficient for Expert-Parallel MoE
type: hypothesis
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: HCCL exposes all2all, but expert-parallel MoE turns on its measured bandwidth over the Gaudi 2 fabric; the primitive existing is not the same as throughput.
auto_inject: false
applicable_when: When choosing TP versus expert-parallel topology in P0, or when P5.3 considers raising TP/EP above the reference port's TP4
confidence: 0.45
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the P0.5 all2all measurement is low enough relative to the allreduce baseline that dispatch/combine dominates expert step time, this hypothesis is falsified"
tags: ["hccl", "all2all", "expert-parallel", "sparse-moe", "interconnect", "unverified", "author-inference"]
edges: [
  {"target": "fact-hccl-includes-all2all", "type": "depends_on", "weight": 0.7, "note": "Rests on a fact itself capped at 0.65: all2all presence is corroborated by secondary snippets, not the primitives table"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "supports", "weight": 0.9, "note": "R6 is the exposure; its fallback is pure TP over allreduce/allgather if all2all proves weak"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "related_to", "weight": 0.9, "note": "P0.5 records allreduce/allgather/all2all before topology is fixed — the measurement that settles this"},
  {"target": "concept-moe-expert-parallel-vs-tp", "type": "depends_on", "weight": 0.8, "note": "The EP-versus-TP distinction defines what an all2all-shaped MoE step actually costs"},
  {"target": "question-hccl-primitive-caveats", "type": "related_to", "weight": 0.8, "note": "Unverified per-primitive dtype and topology caveats could void the hypothesis independently of bandwidth"}
]
related: ["[[decision-tp-ep-measured-not-default]]", "[[playbook-hccl-collective-benchmark]]", "[[task-p5-3-tune-bucketing-and-tp-ep]]"]
source_url: "Empty"
---

# HCCL All2All Bandwidth Is Sufficient for Expert-Parallel MoE

## Claim

HCCL exposes all2all — and the roadmap flags that this rests on secondary search snippets, because the authoritative primitives table 404'd under `latest` and per-primitive dtype/topology caveats are recorded as unverified. Existence is not throughput. Expert-parallel MoE is an all-to-all dispatch and combine over the interconnect, on a card with 2.45 TB/s HBM and on-chip 24x100 Gbps RoCE. The hypothesis is that measured all2all bandwidth is high enough that dispatch and combine do not dominate expert step time. It has never been measured on this four-card box.

## Test that settles it

`task-p0-5-benchmark-hccl-collectives` (P0.5): record allreduce, allgather and all2all bandwidth on this fabric before any topology is chosen, comparing all2all against the allreduce baseline at expert-activation payload sizes. `task-p5-3-tune-bucketing-and-tp-ep` consumes the result; the roadmap makes higher TP/EP conditional on it.

## If it turns out false

If all2all is weak or congestion-sensitive, expert-parallel is off the table, P5 stays on pure TP over allreduce/allgather, and #1733 low-batch MoE slowness has to be answered by gathered-expert combine and higher concurrency rather than by topology.
