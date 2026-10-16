---
id: bookmark-tpc-sdk-kernel-guide
title: "Unprocessed: TPC SDK Kernel Authoring Guide"
type: bookmark
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Un-ingested pointer to the TPC SDK kernel-authoring guide named by the roadmap as grounding P3's integration steps. Held as a bookmark, not converted."
auto_inject: false
applicable_when: "When P3 starts and the CustomOp integration steps must be read from the guide rather than the roadmap's paraphrase"
confidence: 0.3
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the guide is unreachable or has moved at the Suite 1.24.2 documentation path when P3 begins, the authoring playbook must be written from the SDK headers instead of from documentation"
tags: ["bookmark", "unprocessed", "tpc-sdk", "kernel-authoring", "custom-op"]
edges: [
  {"target": "ref-tpc-sdk", "type": "related_to", "weight": 0.9, "note": "This guide is the primary document behind the TPC SDK reference node's integration steps"},
  {"target": "playbook-tpc-customop-authoring", "type": "related_to", "weight": 0.85, "note": "The playbook's steps would be verified against the guide's own commands and build flags once converted"},
  {"target": "cust-risk-r5-no-intel-primitive-roadmap", "type": "related_to", "weight": 0.7, "note": "The guide is the mitigation for R5 made concrete: it is how the team authors what Intel has not shipped"}
]
related: ["[[ref-tpc-sdk]]", "[[playbook-tpc-customop-authoring]]", "[[fact-customop-single-kernel-contract]]"]
source_url: "Empty"
---

# Unprocessed: TPC SDK Kernel Authoring Guide

Pointer: the TPC SDK kernel-authoring documentation in the Gaudi software suite docs — the source the roadmap cites when it grounds the P3 integration path (TPC-C kernel body, `registerUserCustomOp`, `hpu_custom_op_pt2.h`, `TORCH_LIBRARY`/`TORCH_LIBRARY_IMPL`, `habana_pytorch2_plugin`, `torch.ops.load_library`). It matters because P3 has no Intel roadmap to wait on, so the team works from this guide, and the vault currently holds only the roadmap's paraphrase of it.

Ingesting and converting it would verify the steps inside `ref-tpc-sdk`, give `playbook-tpc-customop-authoring` its real build and load commands, and confirm or correct `fact-customop-single-kernel-contract`.
