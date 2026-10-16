---
id: cust-risk-r4-1733-lowbatch-moe
title: R4 — Issue #1733 Low-Batch MoE Slowness Dominates
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Known low-batch sparse-MoE slowness on Gaudi 2 can dominate end-to-end throughput, making single-request latency uncompetitive.
auto_inject: false
applicable_when: When setting latency targets, pricing the deployment, or benchmarking at concurrency 1
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the P5 cost-per-token curve shows the concurrency-1 decode step within the Gaudi 2 target budget after P5.1, this risk is retired"
tags: ["roadmap-risk", "r4", "medium", "moe", "throughput", "issue-1733"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Roadmap risk R4, probability medium, impact high, transcribed from the risks block"},
  {"target": "ref-issue-1733-low-batch-moe", "type": "derived_from", "weight": 0.9, "note": "The exposure is grounded in a filed upstream issue, not an inference — the reason probability sits at 0.7"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.95, "note": "P5 exists because of this risk; its goal is stated relative to #1733 on Gaudi 2 low batch"},
  {"target": "task-p5-1-gathered-expert-moe-combine", "type": "related_to", "weight": 0.85, "note": "The opt-in FP8 gathered-expert combine in plugin v0.30.0 is the named lever against it"},
  {"target": "question-moe-saturation-point", "type": "related_to", "weight": 0.8, "note": "Where cost-per-token saturates decides whether the risk is a business constraint or a solved one"}
]
related: ["[[ref-issue-1733-low-batch-moe]]", "[[question-moe-saturation-point]]", "[[cust-phase-p5-moe-economics]]"]
source_url: "Empty"
---
# R4 — Issue #1733 Low-Batch MoE Slowness Dominates

## Exposure

medium / high. The roadmap states the exposure as "#1733 low-batch MoE slowness on Gaudi 2 dominates end-to-end throughput." This is the best-sourced risk in the register: the symptom is a filed upstream issue against the plugin rather than an inference. At small batch the sparse-MoE path pays per-expert dispatch and gather costs without enough tokens to amortise them, so on a Gaudi 2 with less compute headroom than the reference card the slow stage moves from the dense layers to the experts and sets the whole step time. Probability is medium but the impact is high because it lands on the number the deployment is judged by.

## Mitigation

P5.1 gathered-expert combine; higher concurrency; market for high-concurrency only. Apply the opt-in gathered-expert MoE combine for FP8 shipped in plugin v0.30.0, pre-register the throughput protocol before measuring so the improvement is attributable to one lever, and raise batch where the product allows. If the curve never flattens into a competitive single-stream cost, the honest answer is a high-concurrency product, not a lower promise.

## Trigger to watch

A P5 curve whose concurrency-1 point is more than a small multiple of its saturated per-token cost, decode-step time that barely improves when concurrency rises from 1 to 2, or any benchmark quoted without its concurrency.
