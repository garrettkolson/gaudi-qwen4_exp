---
id: task-p6-2-vision-tower
title: Implement the Vision Stack for Conditional Generation
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Deferred, not required for text-only serving. Build the vision tower behind Qwen4ExpForConditionalGeneration, which PR #1829 excluded, if multimodal serving becomes a requirement.
auto_inject: false
applicable_when: P6 (cust-phase-p6-feature-parity) — deferred and product-driven; live only if multimodal serving is required after text-only enablement on Gaudi 2 is complete.
confidence: 0.75
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the multimodal requirement is dropped, or a later vllm-gaudi release or PR ships the vision tower for this architecture, this task becomes obsolete and the class needs only a re-test."
tags: ["roadmap-task", "p6", "deferred", "vision", "multimodal"]
edges: [
  {"target": "cust-phase-p6-feature-parity", "type": "part_of", "weight": 0.9, "note": "P6 task, explicitly deferred and not part of text-only serving enablement"},
  {"target": "task-p1-2-register-model-and-runner", "type": "depends_on", "weight": 0.7, "note": "P1.2 registers Qwen4ExpForConditionalGeneration; this task fills in the vision stack behind that class"},
  {"target": "source-vllm-gaudi-pr1829", "type": "related_to", "weight": 0.7, "note": "PR #1829 deliberately excluded the vision tower, so nothing can be reused from the base port"}
]
related: ["[[cust-phase-p6-feature-parity]]", "[[task-p1-2-register-model-and-runner]]", "[[decision-defer-feature-parity-p6]]"]
source_url: "Empty"
---
# Implement the Vision Stack for Conditional Generation

Deferred — not required for text-only serving. If multimodal serving becomes a product requirement, implement the vision tower behind the Qwen4ExpForConditionalGeneration class. PR #1829 excluded the vision tower from its scope, so there is nothing to reuse from the base port: the work is a new encoder path plus its wiring into the already-registered conditional-generation class, validated on the 4x Gaudi 2 memory budget.

Done when: the per-feature criterion is met — images serve correctly through the conditional-generation class on Gaudi 2; text-only serving enablement does not wait for this.
