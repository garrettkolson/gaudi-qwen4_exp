---
id: pillar-provenance-discipline
title: Separate Evidence From Inference
type: pillar
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Keep the roadmap's split between sourced claims and author inferences intact; flattening it turns flagged inferences into hard constraints and plans work around walls that may not exist.
auto_inject: false
applicable_when: When planning around a roadmap claim, setting a dependency, or quoting a node whose confidence is at or below 0.7
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If Gaudi 2 measurements repeatedly confirm roadmap-flagged inferences (FP8 MME gap, capture gating), the inferences become evidence and nodes carrying them should be re-tiered"
tags: ["strategy", "provenance", "evidence", "inference", "confidence-policy"]
edges: [
  {"target": "note-provenance-register", "type": "related_to", "weight": 0.9, "note": "The register carries the roadmap's evidence_grounded and author_inference_flagged lists verbatim — this pillar's operational form"},
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "The roadmap itself declares the split in its provenance block; the pillar generalises it into an operating rule"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.8, "note": "Worked example: all2all existence is corroborated by secondary snippets only — the authoritative primitives table 404'd, and existence is not throughput"}
]
related: ["[[note-provenance-register]]", "[[hyp-customop-gates-compile-capture]]", "[[cust-risk-r6-hccl-all2all-bandwidth]]"]
source_url: "Empty"
---

# Separate Evidence From Inference

**Principle.** The roadmap's value is not only its plan but its labelling: its `provenance` block states which claims are evidence-grounded (PR #1829's scope, the #1734 resolution via pin `c05d75a`, Gaudi 2's 96GB/2.45TB/s and FP8 E4M3/E5M2 support) and which are the author's reading (the P3-to-P4 capture gating, the residual FP8 throughput concern, the pin-check-before-kernels ordering, HCCL all2all existence via secondary snippets). The vault preserves that split through node type, confidence tier, and `verified_at: "Empty"`.

**What this rules out.** Quoting a flagged inference as a constraint. Example from the roadmap itself: expert-parallel feasibility rests on all2all *throughput*, and the primitive's existence is corroborated only by search snippets while the authoritative table 404'd — an agent that flattens this treats an unverified reading as a wall and drops EP from planning without measuring.

**What it forces under time pressure.** Under deadline, unlabelled certainty is cheap: someone says "sparse top-k can't be captured" as if settled. The pillar forces the slower sentence — sourced, inferred, or measured? — and the corresponding action: verify against the source, or run the P0/P4 test that settles it, before the claim shapes the schedule.
