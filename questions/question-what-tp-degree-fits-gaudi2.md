---
id: question-what-tp-degree-fits-gaudi2
title: What TP Degree and Context Length Actually Fit on 4x Gaudi 2?
type: question
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: No TP degree, --max-model-len or memory-utilization has been established on 4x Gaudi 2; the Gaudi 3 reference settings are inherited, not measured.
auto_inject: false
applicable_when: Before any phase that sizes memory — P0.3, the P2 concurrency target, and any P5.3 topology change
confidence: 0.4
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "Once P0.3 records a TP + max-model-len + memory-utilization config that boots and serves on all TP workers without OOM, this question is answered"
tags: ["tp-degree", "memory-utilization", "max-model-len", "hbm", "open-question"]
edges: [
  {"target": "task-p0-3-resize-tp-and-memory", "type": "related_to", "weight": 0.9, "note": "P0.3 is the task that produces the answer by re-deriving the triple for 96GB/2.45TB/s"},
  {"target": "hyp-side-caches-oom-at-concurrency", "type": "depends_on", "weight": 0.75, "note": "The fit depends on how much the unaccounted side caches consume at the concurrency the config targets"},
  {"target": "fact-gaudi2-hbm-and-bandwidth", "type": "depends_on", "weight": 0.85, "note": "The budget being divided: 96GB HBM2E per card across four cards"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.9, "note": "A no-OOM config is one of P0's exit criteria, so the gate cannot close while this is open"}
]
related: ["[[task-p0-5-benchmark-hccl-collectives]]", "[[pillar-measured-before-default]]", "[[cust-risk-r2-hbm-side-cache-pressure]]"]
source_url: "Empty"
---

# What TP Degree and Context Length Actually Fit on 4x Gaudi 2?

## The question

How many tensor-parallel ranks, what `--max-model-len`, and what `--gpu-memory-utilization` fit and run on four Gaudi 2 cards — rather than the Gaudi 3 reference settings PR #1829 shipped with (TP4, 0.80 utilization, 128GB cards)?

## Why it blocks the plan

Everything downstream is sized by this triple. P2's concurrency target assumes a context length and a utilization; the side-cache pressure in `hyp-side-caches-oom-at-concurrency` is a function of both; P5's cost-per-token curve is comparable to nothing unless the topology was fixed before it ran; and an expert-parallel decision in P5.3 is meaningless while TP degree is still inherited. Copying the reference numbers would break the measured-before-default pillar on exactly the numbers that pillar exists to protect.

## What answers it

`task-p0-3-resize-tp-and-memory`, given the successful FP8 load from P0.1 and the collective bandwidth from `task-p0-5-benchmark-hccl-collectives`. The answer is a recorded config that boots on all TP workers without OOM at the intended context length, with the boundary observed by walking utilization and max-model-len upward until allocation fails, then backed off.
