---
id: task-p0-2-fp8-mme-benchmark
title: "Benchmark FP8 MME Throughput vs Gaudi 3"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Measure FP8 matrix-engine (MME) throughput and maturity on Gaudi 2 against Gaudi 3, turning an unresolved spec-sheet gap into a number."
auto_inject: false
applicable_when: "P0, once task-p0-1 proves the checkpoint loads; results feed task-p0-3 sizing and the P5 economics work"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If Intel publishes Gaudi 2 FP8 MME throughput figures, or a later suite release materially changes MME performance, re-run before trusting the recorded number"
tags: ["roadmap-task", "p0", "fp8", "benchmark", "throughput"]
edges: [
  {"target": "cust-phase-p0-platform-gate", "type": "part_of", "weight": 0.9, "note": "Second P0 task; it is the measurement that settles the FP8 performance question"},
  {"target": "hyp-gaudi2-fp8-mme-throughput-gap", "type": "related_to", "weight": 0.9, "note": "This benchmark is the test that confirms or falsifies the throughput-gap hypothesis"},
  {"target": "cust-risk-r1-fp8-mme-throughput", "type": "related_to", "weight": 0.9, "note": "The roadmap names this benchmark as the risk's mitigation"},
  {"target": "fact-gaudi3-reference-specs", "type": "related_to", "weight": 0.7, "note": "Gaudi 3's headline 1.8 PFlops FP8 is the comparison point, and the reason the gap needs measuring rather than assuming"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[hyp-gaudi2-fp8-mme-throughput-gap]]"]
source_url: "Empty"
---

# Benchmark FP8 MME Throughput vs Gaudi 3

Gaudi 3 advertises 1.8 PFlops FP8. Gaudi 2 lists FP8 support without a matching PFlops figure. That asymmetry is the gap this measurement closes: run FP8 MME throughput and maturity checks on Gaudi 2 and compare against the Gaudi 3 reference numbers.

Why it matters: the port's economics depend on FP8 doing real work on this card. The roadmap treats a shortfall as a performance problem rather than a feasibility problem — capability is confirmed, rate is not — and that distinction decides whether a weak result means "re-plan the sizing" or "re-plan the project".

Keep it a micro-benchmark: fixed shapes around the model's dominant MME dimensions, FP8 inputs in both E4M3 and E5M2, and a BF16 baseline for comparison. Record maturity signals too — fallbacks, unsupported shapes, or warnings — since an unsupported shape in the model's real layer geometry matters more than peak throughput. Record raw numbers before interpreting them; the interpretation belongs in the hypothesis node this task settles.

Done when: FP8 MME throughput on Gaudi 2 is recorded next to the Gaudi 3 reference, with unsupported-shape and fallback behaviour documented.
