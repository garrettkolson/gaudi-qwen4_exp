---
id: fact-gaudi3-reference-specs
title: "Gaudi 3 Reference: 128GB, 3.7 TB/s, 1.8 PFlops FP8"
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: PR #1829's reference Gaudi 3 has 128GB HBM @ 3.7 TB/s and 1.8 PFlops FP8 — why its TP4 / 0.80 util numbers do not transfer to Gaudi 2's 96GB/2.45 TB/s.
auto_inject: false
applicable_when: "Empty"
confidence: 0.88
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the Gaudi 3 hardware spec (128GB / 3.7 TB/s / 1.8 PFlops FP8) is corrected, or PR #1829's reference hardware is shown not to be Gaudi 3, this comparison point is invalid"
tags: ["gaudi-3", "reference-spec", "hbm", "fp8", "pflops"]
edges: [
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.85, "note": "The Gaudi 3 reference and its TP4 / 0.80 settings come from the PR #1829 baseline the roadmap contrasts against"},
  {"target": "fact-gaudi2-hbm-and-bandwidth", "type": "related_to", "weight": 0.8, "note": "The 128GB/3.7TB/s reference is meaningful only against Gaudi 2's smaller 96GB/2.45TB/s budget"},
  {"target": "pillar-measured-before-default", "type": "supports", "weight": 0.85, "note": "The larger reference budget is the evidence that inherited config must be re-derived, not copied"}
]
related: ["[[fact-gaudi2-hbm-and-bandwidth]]", "[[fact-pr1829-scope-and-limits]]", "[[task-p0-3-resize-tp-and-memory]]"]
source_url: "Empty"
---

# Gaudi 3 Reference: 128GB, 3.7 TB/s, 1.8 PFlops FP8

The reference hardware against which vllm-gaudi PR #1829 was built is Gaudi 3: 128GB HBM at 3.7 TB/s bandwidth with a headline 1.8 PFlops FP8. The roadmap states these in P0.2 ("Gaudi 3 headline 1.8 PFlops FP8") and P0.3 ("PR's Gaudi 3 128GB/3.7TB/s, 0.80 util"), and lists them under `evidence_grounded` ("Gaudi 3 128GB/3.7TB/s/1.8PFlops FP8"). They are externally checkable hardware specs, so confidence is high.

The point of recording them is contrast. PR #1829 chose TP4 and 0.80 GPU-memory-utilization for a card with roughly a third more HBM and half again the bandwidth than the Gaudi 2 target. That is the mechanical reason those inherited numbers do not transfer here and why P0.3 re-derives TP degree, max-model-len, and memory-utilization.

This node states the Gaudi 3 reference figures only. It does NOT establish Gaudi 2's achieved FP8 throughput, nor that TP4 is wrong for Gaudi 2 — only that copying it is unjustified without measurement. No number here has been measured on the 4-card Gaudi 2 box, so `verified_at` is Empty.
