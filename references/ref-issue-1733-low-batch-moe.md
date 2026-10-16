---
id: ref-issue-1733-low-batch-moe
title: "vllm-gaudi Issue #1733 — MoE Slowness at Low Batch"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "Upstream vllm-gaudi issue 1733: sparse-MoE execution is slow at low batch on Gaudi 2, the grounded reason P5 exists and R4 is rated high impact."
auto_inject: false
applicable_when: "When benchmarking decode throughput at low concurrency, or deciding whether gathered-expert MoE combine is required"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the issue thread shows a fix landed at or before plugin 0.30.0, or a P5 curve shows concurrency-1 decode within target, this reference's framing as an open blocker is out of date"
tags: ["issue-1733", "moe", "low-batch", "throughput", "vllm-gaudi", "upstream-issue"]
edges: [
  {"target": "cust-risk-r4-1733-lowbatch-moe", "type": "related_to", "weight": 0.95, "note": "R4 is the risk register entry for this issue; the issue is the issue, R4 is the exposure it creates"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.9, "note": "P5's goal is stated relative to #1733 on Gaudi 2 low batch"},
  {"target": "task-p5-1-gathered-expert-moe-combine", "type": "related_to", "weight": 0.8, "note": "The opt-in FP8 gathered-expert combine is the named mitigation against this issue's symptom"},
  {"target": "concept-moe-expert-parallel-vs-tp", "type": "related_to", "weight": 0.7, "note": "Low-batch dispatch cost is what makes EP a measured choice rather than a default here"}
]
related: ["[[cust-risk-r4-1733-lowbatch-moe]]", "[[question-moe-saturation-point]]", "[[task-p5-1-gathered-expert-moe-combine]]"]
source_url: "Empty"
---

# vllm-gaudi Issue #1733 — MoE Slowness at Low Batch

Issue number 1733 in the vllm-gaudi tracker. The roadmap cites it as evidence that sparse-MoE execution is slow at low batch on Gaudi 2, and builds risk R4 and the whole of P5 on top of that citation. The known state in this vault is the roadmap's one-line characterisation plus its mitigation list; the thread itself — reported batch sizes, expert counts, TP degrees, plugin version at report time, any maintainer response, and whether a fix shipped — has not been captured, so nothing in this node is more than the roadmap's reading of the issue.

Before relying on this: read the actual thread and record the reported configuration, confirm whether it is still open and against which plugin version, check whether the v0.30.0 gathered-expert MoE combine is the fix or merely a workaround, and re-measure the symptom on this 4-card box, because the roadmap's throughput claims have not been observed on Gaudi 2 hardware.
