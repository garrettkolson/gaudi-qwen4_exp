---
id: task-p4-5-meet-customop-capture-contract
title: Prove Each P3 CustomOp Satisfies the Capture Contract
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Verify each P3 CustomOp is a single TPC kernel registered in the custom_op namespace with a Meta impl, so sparse top-k, PLE conv, and FP8 n-gram ops capture instead of forcing eager.
auto_inject: false
applicable_when: P4b (cust-phase-p4-capture) — live once the P3 CustomOps have landed and a compiled-mode boot without --enforce-eager is attempted.
confidence: 0.65
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If Intel changes the UserCustomOp capture requirements, or a fully contract-compliant single-kernel CustomOp still fails to capture, the contract reading this task rests on is wrong and must be re-derived."
tags: ["roadmap-task", "p4-capture", "customop", "tpc", "torch-compile"]
edges: [
  {"target": "cust-phase-p4-capture", "type": "part_of", "weight": 0.9, "note": "Capture of the P3 kernels is the hinge between P3 authoring and P4b compiled serving"},
  {"target": "fact-customop-single-kernel-contract", "type": "depends_on", "weight": 0.95, "note": "The single-kernel and custom_op namespace limits are the contract being proven here"},
  {"target": "hyp-customop-gates-compile-capture", "type": "related_to", "weight": 0.9, "note": "The gating premise is a flagged author inference; this task is its test on Gaudi 2"},
  {"target": "task-p3-1-sparse-topk-kernel", "type": "depends_on", "weight": 0.8, "note": "The sparse top-k / QSA indexer CustomOp is one of the three ops being proven capturable"},
  {"target": "task-p3-2-ple-dilated-conv-kernel", "type": "depends_on", "weight": 0.8, "note": "The PLE dilated short-conv CustomOp is one of the three ops being proven capturable"},
  {"target": "task-p3-3-fp8-ngram-gather-kernel", "type": "depends_on", "weight": 0.8, "note": "The FP8 n-gram gather-then-dequant CustomOp is one of the three ops being proven capturable"}
]
related: ["[[cust-phase-p4-capture]]", "[[concept-tpc-customop-integration]]", "[[playbook-tpc-customop-authoring]]"]
source_url: "Empty"
---
# Prove Each P3 CustomOp Satisfies the Capture Contract

Verify that each P3 primitive — sparse top-k / QSA indexer, PLE dilated short-conv, and FP8 n-gram gather-then-dequant — meets the capture contract: a single TPC kernel per UserCustomOp, registered in the custom_op namespace, with a Meta implementation for torch.compile. A multi-op Python decomposition re-creates eager dispatch cost and will not capture. This check sits on the phase's known blocker, synStatus-26 / synapse `compileGraph` (issue #1734 family), so each proof must record which subgraphs still refuse capture and why.

Done when: the server boots and serves on all TP workers without --enforce-eager with all three CustomOps captured, or the QSA indexer only carries a documented per-subgraph eager fallback.
