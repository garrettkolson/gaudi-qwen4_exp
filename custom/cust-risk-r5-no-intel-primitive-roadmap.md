---
id: cust-risk-r5-no-intel-primitive-roadmap
title: R5 — No Public Roadmap for the Remaining Primitives
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: No public Intel roadmap covers the three hard primitives, so P3 kernel authoring is entirely the team's responsibility.
auto_inject: false
applicable_when: When estimating P3 effort or waiting for a plugin or suite release to supply a fused kernel
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a suite or plugin release ships fused kernels for sparse top-k/QSA, PLE dilated short-conv, or FP8 n-gram gather, this risk no longer applies to that primitive"
tags: ["roadmap-risk", "r5", "confirmed", "tpc-sdk", "customop", "kernel-authoring"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Roadmap risk R5, probability confirmed, impact medium, transcribed from the risks block"},
  {"target": "cust-phase-p3-custom-kernels", "type": "related_to", "weight": 0.9, "note": "The phase whose entire scope exists because nobody upstream is going to supply these kernels"},
  {"target": "ref-tpc-sdk", "type": "related_to", "weight": 0.85, "note": "The authoring path Intel uses for its own kernels — the toolchain that makes the risk ours to close"},
  {"target": "playbook-tpc-customop-authoring", "type": "related_to", "weight": 0.9, "note": "The procedure that converts an accepted risk into three bounded kernel efforts"},
  {"target": "fact-customop-single-kernel-contract", "type": "derived_from", "weight": 0.8, "note": "The contract the mitigation must satisfy: one TPC kernel per CustomOp plus custom_op namespace registration"}
]
related: ["[[cust-phase-p3-custom-kernels]]", "[[playbook-tpc-customop-authoring]]", "[[ref-tpc-sdk]]"]
source_url: "Empty"
---
# R5 — No Public Roadmap for the Remaining Primitives

## Exposure

confirmed / medium. The roadmap states the exposure as "No public Intel roadmap for remaining primitives -> P3 is on you (SDK/CustomOp)." This is the one risk the roadmap marks confirmed: nothing public commits Intel to fused kernels for the QSA sparse top-k indexer, the PLE dilated short-conv, or the FP8 n-gram gather-then-dequant, and none appear in the release lineage through plugin v0.30.0. The impact is medium rather than high because the primitives already work in eager and the toolchain to fuse them is documented and public — the cost is engineering time and scheduling, not an unsolvable gap.

## Mitigation

Use TPC SDK + PyTorch CustomOp API contract. Write the kernel body in TPC-C through the TPC SDK, the same path Intel uses for its own kernels, then integrate through `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)` with types in `hpu_custom_op_pt2.h`, exposing each primitive as one kernel in the `custom_op` namespace with a Meta implementation for `torch.compile`. Treating P3 as in-house work with a known contract is what keeps it off the critical path; treating it as an upstream dependency is what would stall the plan.

## Trigger to watch

Any P3 estimate that assumes a suite or plugin release will supply one of the three primitives, waiting on an Intel release note before scheduling kernel work, or a P3 exit criterion quietly relaxed from a single CustomOp to a Python decomposition of several ops.
