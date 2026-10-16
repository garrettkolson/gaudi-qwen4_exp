---
id: hyp-gaudi2-fp8-mme-throughput-gap
title: Gaudi 2 FP8 MME Throughput Trails Gaudi 3
type: hypothesis
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Gaudi 2 supports FP8 E4M3/E5M2 but publishes no PFlops figure beside it; per-card FP8 matrix throughput is assumed below Gaudi 3 until P0.2 measures it.
auto_inject: false
applicable_when: When quoting tokens-per-second or FLOPs from the Gaudi 3 reference port, or when sizing TP degree from FP8 headroom
confidence: 0.55
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the P0.2 FP8 MME micro-benchmark on this 4x Gaudi 2 box reaches or exceeds Gaudi 3 per-card FP8 throughput, this hypothesis is falsified"
tags: ["gaudi-2", "fp8", "mme", "throughput", "unverified", "author-inference"]
edges: [
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "depends_on", "weight": 0.8, "note": "FP8 capability on Gaudi 2 is confirmed; this hypothesis is only about the rate beside that capability"},
  {"target": "cust-risk-r1-fp8-mme-throughput", "type": "supports", "weight": 0.85, "note": "If the gap is real, R1 stays live and P5 cost-per-token targets must be re-derived downward"},
  {"target": "task-p0-2-fp8-mme-benchmark", "type": "related_to", "weight": 0.9, "note": "P0.2 is the measurement that settles it; no throughput claim before that number exists"},
  {"target": "fact-gaudi3-reference-specs", "type": "derived_from", "weight": 0.7, "note": "The gap is inferred by comparing Gaudi 2 spec lines against Gaudi 3's 1.8 PFlops FP8 headline"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[note-provenance-register]]", "[[decision-fp8-no-requantization]]"]
source_url: "Empty"
---

# Gaudi 2 FP8 MME Throughput Trails Gaudi 3

## Claim

Gaudi 2 supports FP8 in E4M3 and E5M2 — spec-grounded, and the reason no INT8 or BF16 re-quantization fork is needed. What is not grounded is rate. Gaudi 2's public numbers list FP8 support without a PFlops figure comparable to Gaudi 3's headline 1.8 PFlops, and the roadmap files its residual throughput concern under `author_inference_flagged`. The hypothesis is narrow: per-card FP8 matrix throughput is meaningfully lower, so PR #1829's Gaudi 3 timings describe a different machine. FP8 here is a feasibility path — a checkpoint that loads and fits — not a performance claim.

## Test that settles it

`task-p0-2-fp8-mme-benchmark` (P0.2): run an FP8 MME micro-benchmark on this box at the MoE projection and expert shapes, and compare achieved FLOPs and per-card tokens per second against the Gaudi 3 reference. Nothing downstream should quote speed before that number exists.

## If it turns out false

If Gaudi 2 measures at or near Gaudi 3 per-card FP8 throughput, R1 becomes a footnote rather than a risk, P0 stops gating on throughput, and P5 can inherit cost-per-token expectations from the reference port instead of re-deriving them downward.
