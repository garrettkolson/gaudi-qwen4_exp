---
id: fact-gaudi2-fp8-dtype-support
title: Gaudi 2 Supports FP8 E4M3 and E5M2
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Gaudi 2 supports FP8 E4M3 and E5M2, so the FP8 checkpoint loads with no re-quantization fork. Capability is confirmed; FP8 MME throughput is not measured.
auto_inject: false
applicable_when: "Empty"
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If Gaudi Software Suite 1.24.2 drops or degrades FP8 E4M3/E5M2 execution on Gaudi 2, or a P0.1 load shows the FP8 checkpoint falling back off the FP8 path, this capability claim is invalidated"
tags: ["gaudi-2", "fp8", "e4m3", "e5m2", "dtype-support"]
edges: [
  {"target": "source-gaudi2-spec-sheets", "type": "derived_from", "weight": 0.9, "note": "FP8 E4M3/E5M2 support is drawn from the Gaudi 2 hardware specification sources"},
  {"target": "decision-fp8-no-requantization", "type": "supports", "weight": 0.9, "note": "Confirmed FP8 support is the basis for serving the checkpoint directly with no INT8/BF16 fork"},
  {"target": "hyp-gaudi2-fp8-mme-throughput-gap", "type": "related_to", "weight": 0.85, "note": "Support is about capability; the open question is the rate, which the hypothesis tracks"},
  {"target": "task-p0-1-load-fp8-on-eager", "type": "supports", "weight": 0.9, "note": "P0.1 relies on FP8 support to load the checkpoint on Gaudi 2 eager"}
]
related: ["[[decision-fp8-no-requantization]]", "[[task-p0-1-load-fp8-on-eager]]", "[[hyp-gaudi2-fp8-mme-throughput-gap]]"]
source_url: "Empty"
---

# Gaudi 2 Supports FP8 E4M3 and E5M2

Gaudi 2 supports the FP8 E4M3 and E5M2 data types. The roadmap records this in `target_stack.gaudi2_fp8_support: ["E4M3", "E5M2"]`, in P0.1 ("FP8 E4M3/E5M2 is supported, so no re-quantization fork"), and in its `evidence_grounded` provenance list ("Gaudi 2 FP8 E4M3/E5M2 support"). Intel's Gaudi 2 specification sheets corroborate FP8 support at the hardware level. This is an externally checkable capability, so confidence is high.

The consequence is concrete: the Qwen3.8-Flash-Next FP8 checkpoint can be served directly on Gaudi 2 without an INT8 or BF16 re-quantization fork, which is what `decision-fp8-no-requantization` rests on, and P3.3 keeps the n-gram path in FP8 on the Gaudi 2 MME rather than re-expressing it.

This node asserts that FP8 execution is available; it does NOT assert that FP8 matrix-engine (MME) throughput on Gaudi 2 matches Gaudi 3. The roadmap explicitly flags the throughput concern as an inference — Gaudi 2 "lists FP8 without matching PFlops" — and defers it to the P0.2 micro-benchmark. Existence is confirmed; throughput is not measured, so `verified_at` is Empty.
