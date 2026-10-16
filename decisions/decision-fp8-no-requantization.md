---
id: decision-fp8-no-requantization
title: Serve the FP8 Checkpoint Directly — No Re-quantization Fork
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Serve the FP8 checkpoint as-is on Gaudi 2 — E4M3/E5M2 are supported — with no INT8 or BF16 re-quantization fork, including the n-gram gather which stays FP8 on Gaudi 2 MME.
auto_inject: false
applicable_when: When loading the checkpoint at P0.1, when writing FP8 kernels in P3, or when a re-quantization fork is proposed
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P0.1 shows the FP8 E4M3/E5M2 path fails or silently falls back on Gaudi 2 despite spec-sheet support, the no-requantization decision must be revisited"
tags: ["decision", "fp8", "quantization", "gaudi-2", "checkpoint"]
edges: [
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "supports", "weight": 0.9, "note": "The grounding fact: Gaudi 2 supports FP8 E4M3 and E5M2, so the checkpoint's dtypes are runtime-native"},
  {"target": "task-p3-3-fp8-ngram-gather-kernel", "type": "related_to", "weight": 0.8, "note": "Applies at kernel level: the n-gram gather-then-dequant stays FP8 on Gaudi 2 MME, no INT8 re-expression"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.8, "note": "P0's whole goal is confirming FP8 is a real runtime path, which this decision presupposes and P0.1 tests"},
  {"target": "task-p0-1-load-fp8-on-eager", "type": "related_to", "weight": 0.85, "note": "P0.1 is the direct test: load the FP8 checkpoint on Gaudi 2 eager and run deterministic single-token probes"}
]
related: ["[[fact-gaudi2-fp8-dtype-support]]", "[[task-p0-1-load-fp8-on-eager]]", "[[task-p3-3-fp8-ngram-gather-kernel]]", "[[hyp-gaudi2-fp8-mme-throughput-gap]]"]
source_url: "Empty"
---

# Serve the FP8 Checkpoint Directly — No Re-quantization Fork

## Context

The roadmap's P0.1 states it plainly: FP8 E4M3/E5M2 is supported on Gaudi 2, so no re-quantization fork. The checkpoint for Qwen3.8-Flash-Next is FP8, and Gaudi 2 lists both FP8 formats as supported dtypes. The open Gaudi 2 question about FP8 is throughput on the matrix engine relative to Gaudi 3, which the roadmap treats as a performance question, not a feasibility one.

## Alternatives considered

An INT8 re-quantization fork of the checkpoint, including re-expressing the FP8 n-gram gather as INT8. A BF16 fork, which roughly doubles weight memory against 96GB HBM2E per card on the 4-card target.

## Decision

Serve the FP8 checkpoint directly. Load it unmodified at P0.1 on Gaudi 2 eager; the P3 n-gram gather-then-dequant kernel stays FP8 on Gaudi 2 MME with no INT8 re-expression.

## Consequence

No second checkpoint artifact, no divergent quantization path to validate, and P3 keeps one dtype story. The FP8 MME throughput gap versus Gaudi 3 stays tracked as risk R1 — settled by the P0.2 micro-benchmark, and if the gap bites it changes cost-per-token, not the serving path's dtypes.
