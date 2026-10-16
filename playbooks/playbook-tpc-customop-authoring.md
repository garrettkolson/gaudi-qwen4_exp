---
id: playbook-tpc-customop-authoring
title: "Authoring a TPC CustomOp for One Primitive"
type: playbook
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Five-step path from eager fallback to one fused TPC CustomOp via the TPC SDK and PyTorch CustomOp contract, gated on byte-equality to eager and the two hard limits."
auto_inject: false
applicable_when: "When executing P3 — replacing an eager fallback (sparse top-k/QSA, PLE dilated conv, FP8 n-gram gather) with a fused TPC kernel on Gaudi 2"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If plugin 0.30.0 / PyTorch 2.13 changes the registerUserCustomOp signature or the location of hpu_custom_op_pt2.h, re-verify every step against the installed SDK before writing another kernel"
tags: ["playbook", "p3", "tpc", "custom-op", "kernel-authoring", "torch-compile"]
edges: [
  {"target": "concept-tpc-customop-integration", "type": "depends_on", "weight": 0.9, "note": "The integration path this runbook operationalises — TPC-C kernel, registerUserCustomOp, custom_op namespace"},
  {"target": "fact-customop-single-kernel-contract", "type": "depends_on", "weight": 0.9, "note": "Carries the two hard limits checked in steps 7 and 8: one TPC kernel per descriptor, namespace registration"},
  {"target": "cust-phase-p3-custom-kernels", "type": "related_to", "weight": 0.9, "note": "The phase whose exit criterion — one CustomOp per primitive, byte-equal to eager — is the finish line of this procedure"},
  {"target": "ref-tpc-sdk", "type": "related_to", "weight": 0.85, "note": "The SDK used for the kernel body in step 2 — the same path Intel uses for its own kernels"},
  {"target": "ref-pytorch-customop-api", "type": "related_to", "weight": 0.85, "note": "The CustomOp API contract that defines registration, dispatch and Meta behaviour in steps 3 to 5"},
  {"target": "task-p3-1-sparse-topk-kernel", "type": "related_to", "weight": 0.85, "note": "The highest-risk instance of this procedure: data-dependent control flow in the QSA indexer"}
]
related: ["[[concept-tpc-customop-integration]]", "[[task-p3-2-ple-dilated-conv-kernel]]", "[[task-p3-3-fp8-ngram-gather-kernel]]", "[[task-p4-5-meet-customop-capture-contract]]"]
source_url: "Empty"
---

# Authoring a TPC CustomOp for One Primitive

1. **Freeze the eager reference.** Run the primitive's current eager path at a fixed input and save its outputs as golden tensors. *Check:* the same input run twice gives identical bytes. An unstable reference cannot gate anything.
2. **Write the kernel body in TPC-C via the TPC SDK** — the same path Intel uses for its own kernels. *Check:* the kernel builds in the SDK and matches the golden tensors on fixed inputs.
3. **Register the op** with `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)`, taking the types from `hpu_custom_op_pt2.h`. *Check:* registration returns clean and the schema's arity and dtypes match the eager signature exactly.
4. **Build the execution function** with `getUserCustomOpDescriptor` + `execute`. *Check:* a direct call through the descriptor reproduces the golden tensors at one shape before any model wiring.
5. **Expose it to PyTorch:** define the op with `TORCH_LIBRARY`, add HPU dispatch via `TORCH_LIBRARY_IMPL`, and add a Meta impl so `torch.compile` can do shape inference. *Check:* the Meta impl returns the correct output shape without touching the device.
6. **Compile and load:** compile `op.cpp` against `habana_pytorch2_plugin` and load it with `torch.ops.load_library`. *Check:* the op resolves through `torch.ops` and runs on the HPU device inside the model.
7. **Verify the single-kernel limit:** one TPC kernel per `UserCustomOpDescriptor`. *Check:* the descriptor holds one kernel — Python calling several ops recreates eager dispatch cost and the phase exit is not met. Per-step dispatch count drops versus eager.
8. **Verify the namespace limit:** register in the `custom_op` namespace. *Check:* full `torch.compile` support holds — proven here rather than discovered in P4.
9. **Close the correctness gate:** byte-equal to the eager reference on Gaudi 2 across the shapes the model uses. *Check:* exact byte comparison, not tolerance comparison. FP8 n-gram gather stays FP8 — no INT8 re-expression.

## Stop and escalate

Stop and report when: the primitive only closes as multi-op Python decomposition, so a single TPC kernel is off the table; outputs are not byte-equal to eager — faster-and-wrong is a bug, not an optimisation; the contract appears to need an API, flag, or step the roadmap does not state, which is a finding about the contract rather than an invitation to invent one; or sparse top-k still resists capture after steps 7 and 8, which is the R3 trigger and belongs in P4's hybrid decision, not in more kernel iterations.
