---
id: playbook-hccl-collective-benchmark
title: "Benchmarking HCCL Collectives Before Choosing Topology"
type: playbook
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Measure allreduce, allgather and all2all on the 4x Gaudi 2 fabric in P0.5 and choose TP/EP from those numbers, never from the Gaudi 3 reference's TP4 default."
auto_inject: false
applicable_when: "When running P0.5 on the 4-card box, before any TP degree or expert-parallel choice is written into a config"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the Gaudi software suite moves off 1.24.2, or the HCCL supported-primitives table becomes reachable on the v1.24.2 path, re-check whether per-primitive dtype and topology caveats change what has to be measured"
tags: ["playbook", "p0", "hccl", "bandwidth", "topology", "expert-parallel"]
edges: [
  {"target": "concept-hccl-collective-layer", "type": "depends_on", "weight": 0.85, "note": "HCCL is Gaudi's NCCL emulation layer — knowing which collectives it exposes is what makes this benchmark set the right set"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "related_to", "weight": 0.9, "note": "The task this runbook carries out; its exit is recorded bandwidth for all three collectives"},
  {"target": "ref-hccl-benchmarking-docs", "type": "related_to", "weight": 0.9, "note": "The Suite 1.24.2 HCCL Testing/Benchmarking documentation — the authority for how the benchmarks are run here"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.85, "note": "The risk this measures: expert-parallel feasibility, which hinges on all2all throughput rather than primitive existence"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.9, "note": "P0 is gating — its exit criteria require measured bandwidth before TP/EP is fixed"}
]
related: ["[[task-p0-5-benchmark-hccl-collectives]]", "[[cust-risk-r6-hccl-all2all-bandwidth]]", "[[question-hccl-primitive-caveats]]", "[[decision-tp-ep-measured-not-default]]"]
source_url: "Empty"
---

# Benchmarking HCCL Collectives Before Choosing Topology

Expert-parallel MoE is an all-to-all dispatch and combine pattern, so its feasibility is a bandwidth question about this 4-card fabric (96 GB HBM2E at 2.45 TB/s per card, on-chip 24x100 Gbps RoCE) — not a question of whether the primitive exists. Run this before any topology is written down.

1. **Confirm the tooling from the Suite 1.24.2 HCCL Testing/Benchmarking documentation runs on 4 ranks.** *Check:* a trivial four-rank allreduce completes and all ranks report the same participant count.
2. **Benchmark allreduce and treat it as the baseline.** *Check:* bandwidth recorded across message sizes, and a repeat run lands within a small spread — if it does not, the noise floor is not yet known and nothing measured after this is trustworthy.
3. **Benchmark allgather at the same message sizes.** *Check:* recorded next to the allreduce numbers, not in a separate note, so the comparison is one table.
4. **Benchmark all2all at the same message sizes.** *Check:* recorded, and the sizes match steps 2 and 3 exactly, so the all2all-to-allreduce ratio is a real ratio and not an artifact of different payloads.
5. **Note what each run actually exercised.** *Check:* dtype and rank-count used per collective are written down, because per-primitive dtype and topology caveats are unverified — the authoritative primitives table 404'd under `latest` — so the run log is the only evidence of coverage you will have.
6. **Write the numbers into a `fact-*` node and settle the hypothesis that hung off them.** *Check:* `hyp-all2all-enables-expert-parallel` confidence moves on the measurement, and the risk node updates through its edges.
7. **Choose TP/EP from the recorded numbers.** *Check:* the recorded choice cites the three measured bandwidths; the Gaudi 3 reference's TP4 and 0.80 utilisation appear nowhere in the justification.

## Stop and escalate

Stop and report when: a collective will not run at all on 4 ranks — a fabric or configuration problem, not a result; all2all runs only under conditions the MoE dispatch would not use, so the number does not answer the question; the authoritative primitives table is needed to read a result and still returns 404; or the numbers seem to justify raising TP or enabling EP while step 4's all2all measurement is missing or unrepeated. Falling back to pure tensor parallelism is a legitimate outcome — weak all2all is a result, not a failure.
