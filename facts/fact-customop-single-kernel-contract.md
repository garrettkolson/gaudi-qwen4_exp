---
id: fact-customop-single-kernel-contract
title: A UserCustomOp Is One TPC Kernel and Needs the custom_op Namespace
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: A UserCustomOp is one TPC kernel (registerUserCustomOp, types in hpu_custom_op_pt2.h); multi-op Python decomposition recreates eager dispatch; the custom_op namespace gates full torch.compile support.
auto_inject: false
applicable_when: "Empty"
confidence: 0.88
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a future vllm-gaudi / habana_pytorch2_plugin release changes registerUserCustomOp's signature or relaxes the single-kernel / custom_op-namespace limits, this contract statement is outdated"
tags: ["customop", "tpc", "torch-compile", "kernel-contract", "pytorch-api"]
edges: [
  {"target": "source-pytorch-customop-docs", "type": "derived_from", "weight": 0.85, "note": "The CustomOp API contract and its single-kernel / namespace limits come from the PyTorch CustomOp documentation"},
  {"target": "ref-pytorch-customop-api", "type": "related_to", "weight": 0.9, "note": "The PyTorch CustomOp API is the contract this node states"},
  {"target": "ref-tpc-sdk", "type": "related_to", "weight": 0.9, "note": "The kernel body is written in TPC-C via the TPC SDK, the same path Intel uses for its own kernels"},
  {"target": "playbook-tpc-customop-authoring", "type": "supports", "weight": 0.9, "note": "The authoring playbook operationalises exactly this registration and namespace contract"},
  {"target": "hyp-customop-gates-compile-capture", "type": "supports", "weight": 0.8, "note": "Supports the hypothesis that single-kernel + custom_op namespace is what unblocks capture; the ordering itself is author inference"}
]
related: ["[[ref-pytorch-customop-api]]", "[[ref-tpc-sdk]]", "[[playbook-tpc-customop-authoring]]", "[[hyp-customop-gates-compile-capture]]"]
source_url: "Empty"
---

# A UserCustomOp Is One TPC Kernel and Needs the custom_op Namespace

A Gaudi UserCustomOp is a single TPC kernel. The integration path (roadmap P3 `integration_contract`) is: write the kernel body in TPC-C via the TPC SDK; register with `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)` using types in `hpu_custom_op_pt2.h`; build the execution function via `getUserCustomOpDescriptor` + `execute`; define the op with `TORCH_LIBRARY` and dispatch on HPU via `TORCH_LIBRARY_IMPL`, adding a Meta impl for `torch.compile`; compile `op.cpp` against `habana_pytorch2_plugin` and load with `torch.ops.load_library`. Two hard limits are stated: one TPC kernel per UserCustomOpDescriptor — a multi-op Python decomposition recreates the eager dispatch cost the work is trying to remove — and registration in the `custom_op` namespace is required for full `torch.compile` support, which gates P4 capture. These API facts are corroborated by the PyTorch CustomOp documentation and the Software Suite / TPC SDK authoring description, both under `evidence_grounded`, so confidence is high.

This node states the API contract only. It does NOT establish that satisfying the contract actually makes a given primitive graph-capturable — the P3→P4 ordering that treats single-kernel + namespace as the gate on capture is flagged by the roadmap as its author's reading of the contract, not an Intel statement (see `hyp-customop-gates-compile-capture`). Nothing is measured, so `verified_at` is Empty.
