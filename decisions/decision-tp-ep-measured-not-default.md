---
id: decision-tp-ep-measured-not-default
title: Choose TP Degree and Expert Parallelism From Measured Bandwidth
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: TP degree and expert-parallelism come from measured HCCL bandwidth (P0.5: allreduce, allgather, all2all), not from the Gaudi 3 PR's TP4 default nor from all2all primitive existence.
auto_inject: false
applicable_when: When fixing TP degree or memory sizing at P0, or when higher TP / expert-parallelism is proposed as a throughput lever in P5
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P0.5 measures all2all bandwidth at or above the allreduce baseline, expect TP/EP above PR's TP4 and re-examine the pure-TP fallback this decision keeps ready"
tags: ["decision", "topology", "expert-parallelism", "hccl", "all2all", "bandwidth"]
edges: [
  {"target": "pillar-measured-before-default", "type": "supports", "weight": 0.95, "note": "The pillar is the strategy; this decision is its binding application to topology selection for TP degree and EP"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.9, "note": "The risk this decision manages: EP feasibility hinges on all2all throughput that exists on paper but is unmeasured"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "depends_on", "weight": 0.9, "note": "The measurement this decision waits on: allreduce/allgather/all2all on the Gaudi 2 fabric before topology is fixed"},
  {"target": "concept-moe-expert-parallel-vs-tp", "type": "depends_on", "weight": 0.85, "note": "Distinguishes the two parallelism styles: EP is an all-to-all dispatch/combine pattern, TP rides allreduce/allgather"},
  {"target": "task-p5-3-tune-bucketing-and-tp-ep", "type": "related_to", "weight": 0.85, "note": "P5.3 restates the rule at lever-selection time: higher TP/EP than PR's TP4 only if measured all2all supports it"}
]
related: ["[[pillar-measured-before-default]]", "[[task-p0-5-benchmark-hccl-collectives]]", "[[cust-risk-r6-hccl-all2all-bandwidth]]", "[[concept-moe-expert-parallel-vs-tp]]"]
source_url: "Empty"
---

# Choose TP Degree and Expert Parallelism From Measured Bandwidth

## Context

PR #1829 ran TP4 on Gaudi 3 (128GB, 3.7 TB/s). This target is 4x Gaudi 2 at 96GB HBM2E / 2.45 TB/s per card with on-chip 24x100 Gbps RoCE. Expert-parallel MoE is an all-to-all dispatch/combine pattern over that interconnect, and HCCL — Gaudi's NCCL emulation layer — lists all2all among its collectives, but only its existence is corroborated (secondary snippets; the authoritative primitives table 404'd), never its throughput on this fabric.

## Alternatives considered

Copy the Gaudi 3 default of TP4 and 0.80 utilization. Adopt EP because the primitive is documented. Fix pure TP without measuring, foreclosing EP before testing it.

## Decision

Benchmark HCCL collectives — allreduce, allgather, all2all — on the Gaudi 2 fabric at P0.5, before fixing a TP/EP topology. TP degree, `--max-model-len`, and utilization come from those numbers plus the P0.3 re-derivation; higher TP/EP than PR's TP4 only if measured all2all supports it, with pure TP (allreduce/allgather only) as the fallback if all2all is weak.

## Consequence

P0.5 becomes a hard gate on P5.3's topology levers, and risk R6 stays open until a number replaces the assumption. P0's exit criteria explicitly require measured collective bandwidth recorded with the TP/EP target chosen from it.
