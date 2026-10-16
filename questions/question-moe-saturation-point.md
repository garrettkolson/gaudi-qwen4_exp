---
id: question-moe-saturation-point
title: Where Does Cost-per-Token Saturate on Gaudi 2?
type: question
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: The concurrency at which cost per token stops improving on this box is unmeasured, as is whether the knee comes from MoE execution, HBM bandwidth, or the fabric.
auto_inject: false
applicable_when: When making any throughput or pricing claim, and when deciding whether a P5 lever actually helped
confidence: 0.4
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "Once a pre-registered cost-per-token curve across concurrency 1 to target exists with an identified saturation point, this question is answered"
tags: ["throughput", "cost-per-token", "sparse-moe", "concurrency", "open-question"]
edges: [
  {"target": "task-p5-2-preregister-throughput-protocol", "type": "related_to", "weight": 0.85, "note": "The protocol must be fixed before any lever runs, or the curve cannot be attributed"},
  {"target": "cust-risk-r4-1733-lowbatch-moe", "type": "depends_on", "weight": 0.8, "note": "Issue #1733 predicts the knee sits further left than the Gaudi 3 reference implies"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.9, "note": "A documented curve with an identified saturation point is P5's exit criterion"}
]
related: ["[[playbook-fp8-moe-throughput-attribution]]", "[[ref-issue-1733-low-batch-moe]]", "[[task-p5-1-gathered-expert-moe-combine]]"]
source_url: "Empty"
---

# Where Does Cost-per-Token Saturate on Gaudi 2?

## The question

Across concurrency 1 to target, at what point does cost per token stop improving on this box — and is that knee caused by MoE expert execution, HBM bandwidth, or interconnect traffic?

## Why it blocks the plan

P5's exit criterion is a documented cost-per-token curve with an identified saturation point. Without it there is no defensible throughput claim, no way to say whether a lever helped, and no basis for the high-concurrency-only positioning R4's mitigation implies. #1733 reports MoE slowness at low batch on Gaudi 2, which would put the knee well left of where the Gaudi 3 reference port suggests — but no curve has been run here, so both the location and the cause are open.

## What answers it

`task-p5-2-preregister-throughput-protocol` fixes the measurement protocol first, mirroring PR seeds 301-303. The curve is then measured under that protocol before and after `task-p5-1-gathered-expert-moe-combine` and any decode-bucketing change, so a single lever's effect is attributable rather than confounded. The knee's cause is separated by comparing the curve against the P0.5 collective bandwidth numbers.
