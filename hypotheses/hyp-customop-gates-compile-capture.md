---
id: hyp-customop-gates-compile-capture
title: Single-Kernel + custom_op Namespace Is What Unblocks Capture
type: hypothesis
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Meeting the single-TPC-kernel and custom_op namespace rules is assumed to be what lets P3 kernels join HPU graph capture — the roadmap's reading, not an Intel statement.
auto_inject: false
applicable_when: When sequencing P3 kernel authoring against P4b capture work, or when reviewing whether a CustomOp is done
confidence: 0.6
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a CustomOp that satisfies both the single-kernel rule and custom_op namespace registration still fails to capture in P4.5, this hypothesis is falsified"
tags: ["customop", "tpc", "torch-compile", "graph-capture", "unverified", "author-inference"]
edges: [
  {"target": "fact-customop-single-kernel-contract", "type": "depends_on", "weight": 0.8, "note": "The documented limits — one TPC kernel per descriptor, custom_op namespace for full torch.compile — are the contract being interpreted here"},
  {"target": "cust-phase-p4-capture", "type": "related_to", "weight": 0.85, "note": "The hypothesis is why P3 is a dependency of P4b rather than a parallel track"},
  {"target": "task-p4-5-meet-customop-capture-contract", "type": "supports", "weight": 0.85, "note": "P4.5 is the written check of this claim: prove each P3 CustomOp satisfies the contract, then observe capture"},
  {"target": "decision-pin-check-before-kernels", "type": "related_to", "weight": 0.6, "note": "Both are judgment rather than sourcing; the pin check is the cheap test of how much capture the stack already does"},
  {"target": "note-provenance-register", "type": "related_to", "weight": 0.8, "note": "The register lists the P3->P4 ordering as the author's reading of the contract, not a statement by Intel"}
]
related: ["[[cust-phase-p3-custom-kernels]]", "[[playbook-tpc-customop-authoring]]", "[[concept-tpc-customop-integration]]"]
source_url: "Empty"
---

# Single-Kernel + custom_op Namespace Is What Unblocks Capture

## Claim

The roadmap sequences P3 before P4b on an assumption. The contract itself is documented: a UserCustomOp is one TPC kernel — multi-op Python decomposition just recreates eager dispatch cost — and it must register in the `custom_op` namespace for full `torch.compile` support. The inference is that satisfying both is what *unblocks* capture for these primitives. The roadmap files that inference itself: it is its author's reading of the contract, not a statement from Intel. It justifies the ordering; it is not evidence that capture will succeed, and it should not be quoted as a hard prerequisite from Intel.

## Test that settles it

`task-p4-5-meet-customop-capture-contract`: take one contract-compliant CustomOp, boot without `--enforce-eager`, and record whether that subgraph captures. A compliant op that captures confirms the reading cheaply; a compliant op that still fails capture falsifies it and moves the blocker elsewhere in the stack.

## If it turns out false

If compliant CustomOps still fail to capture, P3 no longer precedes capture work by necessity, the pin check and the PR #1843 mitigations carry more of the load, and P4b's eager-fallback branch widens past the QSA indexer — which changes what "compiled mode" means as an exit state.
