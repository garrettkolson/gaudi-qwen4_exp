---
id: concept-hccl-collective-layer
title: HCCL as Gaudi's NCCL Emulation Layer
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Gaudi's NCCL-emulation collective layer, exposing allreduce, allgather, reduce-scatter and all2all. A primitive existing is not the same as its throughput being adequate.
auto_inject: false
applicable_when: Before fixing TP degree or any expert-parallel topology, and when reading measured collective bandwidth
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the HCCL supported-primitives table is read on the v1.24.2 docs path and contradicts this collective list or adds per-primitive dtype or topology caveats, this node needs revision"
tags: ["hccl", "collectives", "interconnect", "all2all", "benchmarking", "topology"]
edges: [
  {"target": "fact-hccl-includes-all2all", "type": "related_to", "weight": 0.9, "note": "That fact carries the collective list, itself capped because the authoritative primitives table 404'd; this node is the framework around it"},
  {"target": "ref-hccl-benchmarking-docs", "type": "related_to", "weight": 0.85, "note": "The suite's testing and benchmarking tooling is the instrument that turns this layer from an assumption into P0.5 numbers"},
  {"target": "concept-moe-expert-parallel-vs-tp", "type": "supports", "weight": 0.8, "note": "Defining the collective vocabulary is what makes the allreduce-versus-all2all comparison in that node well posed"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "related_to", "weight": 0.85, "note": "P0.5 measures this layer's primitives before topology is fixed, which is the only way its caveats get resolved"},
  {"target": "bookmark-hccl-primitives-table", "type": "related_to", "weight": 0.7, "note": "The unprocessed source that would confirm or contradict the primitive list and its per-primitive caveats"}
]
related: ["[[fact-hccl-includes-all2all]]", "[[ref-hccl-benchmarking-docs]]", "[[bookmark-hccl-primitives-table]]", "[[task-p0-5-benchmark-hccl-collectives]]"]
source_url: "Empty"
---

# HCCL as Gaudi's NCCL Emulation Layer

HCCL, the Habana Collective Communications Library, is Gaudi's NCCL-emulation layer: the collective backend a tensor-parallel PyTorch process group runs on. It presents the standard collective set — allreduce, allgather, reduce-scatter, all-to-all — over the Gaudi interconnect, and the software suite ships testing and benchmarking tooling alongside it.

Every topology decision in this project is implicitly a claim about HCCL throughput. Tensor parallelism spends allreduce traffic at every sharded layer; expert parallelism spends all-to-all dispatch and combine at every MoE layer; gradient-free decode makes those per-step costs the serving bottleneck. P0.5 compares the levers by measuring allreduce, allgather and all2all on the actual 4-card fabric before any TP degree or EP configuration is fixed. The roadmap's position, which this node carries, is that primitive existence is not throughput: HCCL listing all2all says nothing about what it sustains on Gaudi 2's on-chip RoCE under a real token payload.

The constraint here is a provenance constraint, and it is why R6 stays live rather than being closed by documentation. The authoritative supported-primitives table returned 404 under the `latest` docs path, so the collective list rests on the documentation index plus secondary snippets, and per-primitive dtype and topology caveats are unverified. The docs also flag collectives and congestion as configuration-sensitive, which is a requirement to benchmark on this box rather than a licence to extrapolate from another platform.
