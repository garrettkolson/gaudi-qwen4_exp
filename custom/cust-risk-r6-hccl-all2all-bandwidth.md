---
id: cust-risk-r6-hccl-all2all-bandwidth
title: R6 — Expert-Parallel MoE Hinges on HCCL All2All Bandwidth
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Expert parallelism for MoE is only feasible if measured HCCL all2all bandwidth on the Gaudi 2 fabric supports it; the number does not exist yet.
auto_inject: false
applicable_when: When choosing TP/EP topology or considering higher TP and expert parallelism than the Gaudi 3 reference's TP4
confidence: 0.55
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a P0.5 benchmark records all2all bandwidth on the 4x Gaudi 2 fabric at or above the allreduce baseline ratio needed for dispatch/combine, the topology branch of this risk closes"
tags: ["roadmap-risk", "r6", "medium", "hccl", "all2all", "expert-parallel"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Roadmap risk R6, probability medium, impact medium-high, transcribed with its source note from the risks block"},
  {"target": "hyp-all2all-enables-expert-parallel", "type": "depends_on", "weight": 0.9, "note": "The risk is only live because the hypothesis that all2all throughput suffices is unmeasured"},
  {"target": "fact-hccl-includes-all2all", "type": "derived_from", "weight": 0.7, "note": "Primitive existence is corroborated by secondary snippets, not the authoritative table — existence is not throughput"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.9, "note": "P0.5 measures allreduce/allgather/all2all before the topology is fixed, which is what this risk is waiting on"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.85, "note": "P5.3 treats higher TP and EP as a measured decision gated on the P0.5 numbers"},
  {"target": "question-hccl-primitive-caveats", "type": "related_to", "weight": 0.85, "note": "Per-primitive dtype and topology caveats are unverified and could bound all2all independently of raw bandwidth"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "related_to", "weight": 0.9, "note": "The benchmark that turns this risk into a topology choice"}
]
related: ["[[hyp-all2all-enables-expert-parallel]]", "[[task-p0-5-benchmark-hccl-collectives]]", "[[question-hccl-primitive-caveats]]"]
source_url: "Empty"
---
# R6 — Expert-Parallel MoE Hinges on HCCL All2All Bandwidth

## Exposure

medium / medium-high. The roadmap states the exposure as "Expert-parallel MoE feasibility hinges on HCCL all2all bandwidth on Gaudi 2 interconnect (primitive exists; throughput unverified). Docs flag collectives/congestion as config-sensitive." Its source note is part of the risk: "HCCL index (NCCL emulation layer, collectives incl. all2all); primitives table page 404 under 'latest' - per-primitive caveats unverified." Expert parallelism is an all-to-all dispatch and combine pattern, so feasibility is a bandwidth question about the 4-card fabric with its on-chip 24x100 Gbps RoCE — not a question of whether the primitive exists.

## Mitigation

P0.5 benchmark all2all/allgather; fall back to pure TP (allreduce/allgather only) if all2all is weak. Measure allreduce, allgather and all2all on the actual Gaudi 2 fabric and record all three before TP/EP is fixed, then treat higher TP or EP than the reference TP4 as a decision the numbers justify rather than a lever to pull. Pure tensor parallelism stays available regardless of the outcome, which is why the impact is medium-high rather than blocking.

## Trigger to watch

Any plan, config, or estimate that raises TP degree or enables EP before P0.5 numbers exist; a measured all2all that trails its allreduce baseline by more than the dispatch/combine pattern can absorb; or reliance on the HCCL primitives table as authority while it still returns 404 under `latest`.
