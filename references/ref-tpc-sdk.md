---
id: ref-tpc-sdk
title: "Gaudi TPC SDK"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "Intel's Tensor Processing Core SDK for authoring Gaudi kernels in TPC-C — the path P3 uses to own the three hard primitives instead of waiting on Intel."
auto_inject: false
applicable_when: "When writing or building a TPC kernel for sparse top-k, PLE dilated conv, or the FP8 n-gram gather"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the Suite 1.24.2 SDK no longer ships hpu_custom_op_pt2.h or the registerUserCustomOp(schema, tpc_guid, OutputMetaFn, FillParamsFn) signature differs, the P3 integration steps must be re-derived from the headers"
tags: ["tpc-sdk", "tpc-c", "custom-op", "kernel-authoring", "suite-1-24-2", "gaudi"]
edges: [
  {"target": "fact-customop-single-kernel-contract", "type": "related_to", "weight": 0.9, "note": "The SDK is the tool half of the contract; the fact node states the single-kernel and namespace limits it must satisfy"},
  {"target": "playbook-tpc-customop-authoring", "type": "related_to", "weight": 0.9, "note": "The playbook operationalises the SDK's integration steps into an ordered procedure"},
  {"target": "cust-phase-p3-custom-kernels", "type": "related_to", "weight": 0.9, "note": "P3's exit criteria are met through this SDK; the roadmap calls it the same path Intel uses for its own kernels"},
  {"target": "cust-risk-r5-no-intel-primitive-roadmap", "type": "related_to", "weight": 0.85, "note": "R5's mitigation is exactly this: author the missing primitives ourselves with the SDK and the CustomOp contract"},
  {"target": "bookmark-tpc-sdk-kernel-guide", "type": "related_to", "weight": 0.8, "note": "The kernel-authoring guide behind this reference is captured as an unprocessed bookmark, not yet converted"}
]
related: ["[[playbook-tpc-customop-authoring]]", "[[fact-customop-single-kernel-contract]]", "[[ref-pytorch-customop-api]]"]
source_url: "Empty"
---

# Gaudi TPC SDK

The Tensor Processing Core SDK shipped with the Gaudi software suite: Intel's own path for writing kernels that run on Gaudi's TPC vector engines, in TPC-C. The roadmap's P3 rests on it because the remaining three primitives have no public Intel roadmap (R5 is rated confirmed), so the port author writes them — the roadmap notes this is the same path Intel uses for its own kernels. Its documented integration steps: write the kernel body in TPC-C; register with `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)`, types in `hpu_custom_op_pt2.h`; build the execution function via `getUserCustomOpDescriptor` and `execute`; define the op with `TORCH_LIBRARY`, dispatch on HPU via `TORCH_LIBRARY_IMPL`, and add a Meta implementation for `torch.compile`; compile `op.cpp` against `habana_pytorch2_plugin` and load with `torch.ops.load_library`.

Before relying on this: confirm the SDK version matches Suite 1.24.2, confirm the header and the registration signature still look like the above, and re-read the kernel-authoring guide itself — the roadmap paraphrases it and the guide is only bookmarked here.
