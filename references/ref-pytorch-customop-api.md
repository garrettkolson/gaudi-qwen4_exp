---
id: ref-pytorch-customop-api
title: "PyTorch CustomOp API Contract"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "The PyTorch custom-op contract P3 must satisfy: one kernel per UserCustomOp, registration in the custom_op namespace for full torch.compile support."
auto_inject: false
applicable_when: "When defining a CustomOp schema, choosing between a fused kernel and a Python decomposition, or adding the Meta impl for capture"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PyTorch 2.13 changes custom_op namespace registration or the fake/Meta impl requirements, or the plugin's CustomOp base stops routing through that namespace, this contract summary needs re-reading"
tags: ["pytorch", "custom-op", "torch-compile", "api-contract", "meta-impl"]
edges: [
  {"target": "fact-customop-single-kernel-contract", "type": "related_to", "weight": 0.95, "note": "The fact node states the two hard limits this API imposes: one TPC kernel per op and custom_op namespace registration"},
  {"target": "concept-tpc-customop-integration", "type": "related_to", "weight": 0.9, "note": "The concept node is where this API contract meets the TPC SDK half of the integration path"},
  {"target": "playbook-tpc-customop-authoring", "type": "related_to", "weight": 0.85, "note": "The playbook's verification steps check schema, namespace and Meta impl against this contract"},
  {"target": "source-pytorch-customop-docs", "type": "related_to", "weight": 0.9, "note": "The documentation set this reference summarises; listed by the roadmap as evidence-grounded"}
]
related: ["[[fact-customop-single-kernel-contract]]", "[[concept-tpc-customop-integration]]", "[[task-p4-5-meet-customop-capture-contract]]"]
source_url: "Empty"
---

# PyTorch CustomOp API Contract

The PyTorch-side contract for user-defined operators, which the roadmap reads as the gate between P3 and P4. The two hard limits it states: a `UserCustomOpDescriptor` maps to a single TPC kernel, so a multi-op Python decomposition simply re-creates the eager dispatch cost the kernel was meant to remove; and an op must be registered in the `custom_op` namespace to get full `torch.compile` support, which is what makes it capturable. Definition goes through `TORCH_LIBRARY`, HPU dispatch through `TORCH_LIBRARY_IMPL`, and a Meta/fake implementation is required for compile-time shape inference. Current known state: this is the roadmap's paraphrase of the published documentation under PyTorch 2.13; nothing here has been exercised against the plugin's CustomOp base class at 0.30.0.

Before relying on this: read the current 2.13 documentation pages directly, check whether the plugin's own CustomOp wrapper still registers through the `custom_op` namespace, and treat the claim that namespace registration gates capture as unverified on Gaudi 2 — the roadmap itself flags that reading as its own.
