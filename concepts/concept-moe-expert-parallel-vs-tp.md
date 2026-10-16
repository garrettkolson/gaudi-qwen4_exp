---
id: concept-moe-expert-parallel-vs-tp
title: Expert Parallelism vs Tensor Parallelism for Sparse MoE
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: TP shards expert matrices and pays allreduce; EP shards experts and pays all2all. On 4x Gaudi 2 the choice is a measured all2all question, never a default.
auto_inject: false
applicable_when: When choosing TP degree, or weighing expert parallelism against the FP8 sparse MoE stack on this 4-card box
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P0.5 measured all2all bandwidth lands close to the allreduce baseline, EP stops being a risk to avoid and becomes a first-choice topology, and the weighting here needs revisiting"
tags: ["moe", "expert-parallel", "tensor-parallel", "all2all", "topology", "interconnect"]
edges: [
  {"target": "fact-model-architecture-blocks", "type": "related_to", "weight": 0.85, "note": "Establishes that the model carries an FP8 sparse MoE, the component whose sharding this node compares"},
  {"target": "concept-hccl-collective-layer", "type": "depends_on", "weight": 0.85, "note": "Both sharding styles are defined here by the collectives they spend, so the comparison is meaningless without the HCCL layer underneath"},
  {"target": "decision-tp-ep-measured-not-default", "type": "related_to", "weight": 0.9, "note": "That decision turns this comparison into a rule: pick the topology from measured bandwidth, not the Gaudi 3 TP4 default"},
  {"target": "hyp-all2all-enables-expert-parallel", "type": "related_to", "weight": 0.9, "note": "The open half of the trade — whether all2all sustains EP on this fabric — is tracked as that hypothesis"},
  {"target": "task-p5-3-tune-bucketing-and-tp-ep", "type": "related_to", "weight": 0.8, "note": "P5.3 is where this trade is exercised, gated on the P0.5 collective numbers"},
  {"target": "cust-risk-r4-1733-lowbatch-moe", "type": "related_to", "weight": 0.75, "note": "At low batch the MoE execution path, not the sharding width, is the bottleneck, which bounds how much EP could help"}
]
related: ["[[concept-hccl-collective-layer]]", "[[decision-tp-ep-measured-not-default]]", "[[hyp-all2all-enables-expert-parallel]]", "[[cust-risk-r4-1733-lowbatch-moe]]"]
source_url: "Empty"
---

# Expert Parallelism vs Tensor Parallelism for Sparse MoE

Tensor parallelism shards every expert's matrices across cards: each card holds a slice of all experts, every token's activations visit all cards, and the row-parallel output is reduced with an allreduce. Communication volume is activation-sized and independent of what the router decided. Expert parallelism shards the experts themselves: each card owns a subset, so each token must travel to the card holding its selected experts — an all-to-all dispatch before the experts, an all-to-all combine after. That volume scales with top-k and token count, sits on the interconnect rather than the local HBM link, and goes idle on one card whenever routing is skewed.

On this 4x Gaudi 2 target the distinction is the entire EP question. EP exchanges allreduce-shaped traffic for all2all-shaped traffic over a fabric whose all2all throughput has never been measured here, with 2.4 TB/s local HBM and on-chip 24x100 Gbps RoCE. Hence the roadmap's stance: EP is a decision taken from P0.5 numbers with pure TP as the fallback, not a lever to pull. EP is also the only one of the two that relieves per-card expert-weight pressure, which is what 96 GB makes tempting.

The failure mode is choosing EP from a Gaudi 3 default or from the bare fact that HCCL exposes all2all, then finding the dispatch/combine pair is the bottleneck — or discovering the workload sits in the low-batch MoE regime of issue #1733, where a gathered-expert combine is the relevant lever and wider sharding is not.
