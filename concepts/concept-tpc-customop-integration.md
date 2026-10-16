---
id: concept-tpc-customop-integration
title: TPC CustomOp Integration Path
type: concept
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "How a missing primitive becomes a Gaudi kernel: TPC-C body, registerUserCustomOp, custom_op namespace. One kernel per descriptor, or dispatch cost is unchanged."
auto_inject: false
applicable_when: When authoring any P3 kernel, or reviewing whether a written CustomOp can enter a captured HPU graph
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the registration signature in the suite 1.24.2 / plugin 0.30.0 headers changes, or the custom_op namespace requirement is dropped, the authoring steps and hard limits recorded here are wrong"
tags: ["tpc", "customop", "kernel-authoring", "torch-compile", "dispatch-overhead"]
edges: [
  {"target": "fact-customop-single-kernel-contract", "type": "depends_on", "weight": 0.9, "note": "The single-kernel and namespace limits that constrain this path are stated in that fact; the path is unusable without them"},
  {"target": "playbook-tpc-customop-authoring", "type": "related_to", "weight": 0.9, "note": "The playbook operationalises these steps with per-step verification and an escalation condition"},
  {"target": "ref-tpc-sdk", "type": "related_to", "weight": 0.9, "note": "The SDK is the toolchain for the TPC-C body and the same route Intel uses for its own kernels"},
  {"target": "ref-pytorch-customop-api", "type": "related_to", "weight": 0.9, "note": "TORCH_LIBRARY declaration, HPU dispatch and the Meta implementation come from this contract, not from Gaudi"},
  {"target": "cust-phase-p3-custom-kernels", "type": "related_to", "weight": 0.9, "note": "P3 is the phase that exercises this path, on the reading that it is in the team's control rather than Intel-gated"}
]
related: ["[[fact-customop-single-kernel-contract]]", "[[playbook-tpc-customop-authoring]]", "[[ref-tpc-sdk]]", "[[ref-pytorch-customop-api]]"]
source_url: "Empty"
---

# TPC CustomOp Integration Path

The CustomOp path is how a missing primitive becomes a first-class Gaudi kernel without waiting on a vendor. The kernel body is written in TPC-C with the TPC SDK — the same route Intel uses for its own kernels — then registered with `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)` using the types in `hpu_custom_op_pt2.h`, with execution built through `getUserCustomOpDescriptor` and `execute`. On the PyTorch side the operator is declared with `TORCH_LIBRARY`, dispatched to HPU in a `TORCH_LIBRARY_IMPL` block, given a Meta implementation so a functionalised `torch.compile` can infer its shapes, compiled against `habana_pytorch2_plugin`, and loaded with `torch.ops.load_library`.

Two limits in the contract decide what P3 is allowed to ship. A `UserCustomOpDescriptor` is one TPC kernel: expressing a primitive as a Python composition of several operators recreates the per-step dispatch cost the CustomOp was meant to remove, so a decomposition is not an optimisation. Registration must live in the `custom_op` namespace for full `torch.compile` support, and the roadmap reads that as the precondition for P4 capture — a reading the roadmap itself flags as its author's inference, not a vendor statement.

The failure mode this explains is the convincing pseudo-fix: a multi-operator, un-namespaced CustomOp that returns correct values in eager, still falls outside a captured graph, and still pays launch overhead on every decode step while looking like progress in a diff.
