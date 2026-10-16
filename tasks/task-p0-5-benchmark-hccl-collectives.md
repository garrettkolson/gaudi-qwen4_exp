---
id: task-p0-5-benchmark-hccl-collectives
title: "Benchmark HCCL Collective Bandwidth Before Fixing Topology"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Measure allreduce, allgather and all2all bandwidth over the Gaudi 2 fabric before choosing a TP/EP topology, since expert parallelism depends on measured all2all throughput."
auto_inject: false
applicable_when: "P0, before any TP/EP topology is fixed; the recorded numbers gate task-p5-3 and the expert-parallel decision"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the Gaudi software suite version changes, or the topology or link configuration of the 4-card box changes, the recorded bandwidth no longer describes this system"
tags: ["roadmap-task", "p0", "hccl", "benchmark", "topology"]
edges: [
  {"target": "cust-phase-p0-platform-gate", "type": "part_of", "weight": 0.9, "note": "The measurement behind P0's third exit criterion: TP/EP target chosen from measured numbers"},
  {"target": "playbook-hccl-collective-benchmark", "type": "related_to", "weight": 0.9, "note": "The procedure this task executes"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.9, "note": "The roadmap names this benchmark as the mitigation for the all2all risk"},
  {"target": "concept-hccl-collective-layer", "type": "depends_on", "weight": 0.8, "note": "HCCL is Gaudi's NCCL emulation layer; knowing its collective surface is what makes the benchmark meaningful"},
  {"target": "ref-hccl-benchmarking-docs", "type": "related_to", "weight": 0.8, "note": "The HCCL Testing and Benchmarking documentation is the tool reference for this task"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[cust-risk-r6-hccl-all2all-bandwidth]]"]
source_url: "Empty"
---

# Benchmark HCCL Collective Bandwidth Before Fixing Topology

Using HCCL Testing and Benchmarking, measure inter-collective bandwidth on the Gaudi 2 fabric — allreduce, allgather and all2all — before a TP/EP topology is fixed. Reference hardware facts: 2.4 TB/s HBM and on-chip 24x100 Gbps RoCE.

Why it matters: the tempting shortcut is to assume that because HCCL exposes all2all, expert parallelism is available. An MoE all-to-all is a dispatch/combine pattern that saturates the interconnect at a rate that depends on this fabric's actual behaviour, on card count and on message size. Primitive existence is not throughput. Choosing TP degree or an EP degree before measuring means the topology decision is made by hope, and it is expensive to reverse once weights are sharded.

Run the collectives at message sizes that reflect real dispatch traffic rather than one default buffer, and record all three so the ratio between them is visible — all2all that is far weaker than allreduce is precisely the signal that pure TP is the right fallback. Save the raw output with the suite version and topology it was taken on.

Done when: allreduce, allgather and all2all bandwidth are recorded on this box and the TP/EP target is chosen from those numbers rather than from the reference configuration.
