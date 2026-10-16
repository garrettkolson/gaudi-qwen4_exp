---
id: pillar-correctness-gates-speed
title: Correctness Gates Speed
type: pillar
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Nothing counts as done until it matches the eager reference byte-for-byte; a kernel that is faster but not byte-equal to eager is a bug generator, not an optimisation.
auto_inject: false
applicable_when: When accepting a kernel, capture change, or throughput lever as done on the Gaudi 2 port
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a P3 primitive is shown on Gaudi 2 to beat eager without byte-equality while still producing correct served output, the byte-equality gate is too strict and should be relaxed"
tags: ["strategy", "correctness", "byte-equality", "custom-kernels", "eager-baseline"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.8, "note": "P3's exit criterion is explicit: each primitive a single CustomOp, byte-equal to the eager reference on Gaudi 2"},
  {"target": "cust-phase-p3-custom-kernels", "type": "related_to", "weight": 0.9, "note": "P3 is where the gate binds hardest: three fused TPC kernels, each checked against eager before it counts"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.7, "note": "Throughput measured on a fast-but-wrong kernel is worthless; P5's cost-per-token curve presumes correct primitives"}
]
related: ["[[cust-phase-p3-custom-kernels]]", "[[decision-eager-first-compiled-later]]", "[[cust-phase-p4-capture]]"]
source_url: "Empty"
---

# Correctness Gates Speed

**Principle.** The eager forward from the retargeted PR #1829 port is the reference implementation. A fused TPC CustomOp for the sparse top-k / QSA indexer, the PLE dilated short-conv, or the FP8 n-gram gather is *done* when it is byte-equal to that eager reference on Gaudi 2 — the roadmap states this as P3's exit criterion, alongside a drop in per-step dispatch count. Correctness is a gate on speed work, not a parallel track: nothing is optimised before it is correct, and nothing is declared done before it matches.

**What this rules out.** Shipping a kernel that is "close enough", faster, and numerically divergent — on a hybrid architecture with GDN state, QSA selection and n-gram history, small divergences compound into silent output corruption, which is worse than a loud crash. It also rules out measuring MoE throughput (P5) on primitives that have not passed the gate, since a cost-per-token curve computed on a wrong kernel documents nothing.

**What it forces under time pressure.** When a deadline demands speed, the temptation is to accept a fast kernel with an unexplained small delta. The pillar forces the boring order: prove byte-equality on Gaudi 2 first, then remove `--enforce-eager`; a day of differential debugging against eager now buys back a week of chasing which benchmark result was fiction later.
