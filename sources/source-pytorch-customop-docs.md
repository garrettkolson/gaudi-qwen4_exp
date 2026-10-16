---
id: source-pytorch-customop-docs
title: PyTorch CustomOp API Documentation
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "PyTorch CustomOp API documentation, the contract P3 authors against: one TPC kernel per UserCustomOp and custom_op namespace registration for full torch.compile support."
auto_inject: false
applicable_when: "When authoring a P3 CustomOp, or when deciding whether an existing op satisfies the compiled-mode capture contract"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a PyTorch or plugin release changes custom_op namespace registration or the single-kernel requirement, fact-customop-single-kernel-contract, the P3 playbook and the capture hypothesis all need re-reading"
tags: ["pytorch", "custom-op", "tpc", "torch-compile", "kernel-authoring", "api-contract"]
edges: [
  {"target": "fact-customop-single-kernel-contract", "type": "supports", "weight": 0.9, "note": "The registration signature and the two hard limits — one TPC kernel, custom_op namespace — are read from this documentation"},
  {"target": "ref-pytorch-customop-api", "type": "related_to", "weight": 0.9, "note": "The reference node is the durable handle on this API; this source is where its content came from"},
  {"target": "playbook-tpc-customop-authoring", "type": "supports", "weight": 0.7, "note": "The playbook's steps are the documented path; the P3 to P4 dependency reading on top of it is the roadmap's own inference"}
]
related: ["[[fact-customop-single-kernel-contract]]", "[[ref-pytorch-customop-api]]", "[[playbook-tpc-customop-authoring]]", "[[concept-tpc-customop-integration]]"]
source_url: "Empty"
---
# PyTorch CustomOp API Documentation

The PyTorch CustomOp documentation the roadmap lists in `evidence_grounded` as the "PyTorch CustomOp API contract incl. single-kernel + custom_op namespace limits". Read together with the Gaudi TPC SDK description, it defines the integration path P3 must follow: author the kernel body in TPC-C via the TPC SDK, register with `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)` using the types in `hpu_custom_op_pt2.h`, build the execution function through `getUserCustomOpDescriptor` and `execute`, define the op with `TORCH_LIBRARY` and HPU dispatch with `TORCH_LIBRARY_IMPL`, add a Meta implementation for `torch.compile`, compile against `habana_pytorch2_plugin` and load with `torch.ops.load_library`.

Two hard limits carry into this vault: a single TPC kernel per UserCustomOp, because multi-op Python decomposition re-creates eager dispatch cost, and registration in the `custom_op` namespace for full `torch.compile` support. It grounds `fact-customop-single-kernel-contract`, `ref-pytorch-customop-api` and the authoring playbook. Not archived in `raw/`; the roadmap cites no URL, so none is recorded.
