---
id: cust-risk-r1-fp8-mme-throughput
title: R1 — Gaudi 2 FP8 MME Throughput Below Gaudi 3
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Gaudi 2 FP8 matrix-engine rate may trail Gaudi 3, so FP8 is a feasibility path on Gaudi 2, not a performance claim.
auto_inject: false
applicable_when: When quoting tokens-per-second or reusing Gaudi 3-derived config numbers on the 4x Gaudi 2 box
confidence: 0.6
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the P0.2 FP8 MME micro-benchmark on Gaudi 2 records per-card throughput at or above the Gaudi 3 reference, this risk is retired"
tags: ["roadmap-risk", "r1", "medium", "fp8", "mme", "throughput"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Roadmap risk R1, probability medium, impact medium, transcribed from the risks block"},
  {"target": "hyp-gaudi2-fp8-mme-throughput-gap", "type": "depends_on", "weight": 0.85, "note": "Likelihood rests on a flagged unmeasured hypothesis, so the risk cannot be scored before P0.2"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.8, "note": "The gating phase that closes this risk before any throughput commitment is made"},
  {"target": "fact-gaudi3-reference-specs", "type": "derived_from", "weight": 0.7, "note": "The 1.8 PFlops FP8 Gaudi 3 headline is the comparison point Gaudi 2 has no matching figure for"},
  {"target": "task-p0-2-fp8-mme-benchmark", "type": "related_to", "weight": 0.9, "note": "The measurement that moves this risk from open to closed"}
]
related: ["[[hyp-gaudi2-fp8-mme-throughput-gap]]", "[[task-p0-2-fp8-mme-benchmark]]", "[[cust-phase-p0-platform-gate]]"]
source_url: "Empty"
---
# R1 — Gaudi 2 FP8 MME Throughput Below Gaudi 3

## Exposure

medium / medium. The roadmap states the exposure as "Gaudi 2 FP8 MME throughput lower than Gaudi 3 (unverified; measure in P0.2)." Gaudi 2 advertises FP8 E4M3/E5M2 support without a matching PFlops figure, while the reference port was built against Gaudi 3's 1.8 PFlops FP8 headline. Capability is confirmed; only the rate is in doubt, which is why the pair is medium/medium rather than a feasibility blocker. The roadmap itself flags the residual throughput concern as author inference, not measurement.

## Mitigation

P0.2 micro-benchmark; treat as perf not feasibility. Measure FP8 MME throughput and maturity on Gaudi 2 against the Gaudi 3 reference before quoting any tokens-per-second or cards-per-service target. The plan's shape does not change with the result: a low number revises expectations and sizing, it does not fork the checkpoint to INT8 or BF16.

## Trigger to watch

Any speed, capacity, or cost claim for this box that leans on Gaudi 3 numbers, PR #1829 settings, or datasheet FP8 support with no Gaudi 2 measurement attached. A first P0.2 result well below the Gaudi 3 per-card figure is also a trigger to revisit concurrency and context targets, because a lower compute ceiling makes the memory risks cheaper and the MoE economics harder.
