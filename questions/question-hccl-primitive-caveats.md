---
id: question-hccl-primitive-caveats
title: What Per-Primitive Caveats Apply to HCCL all2all on Suite 1.24.2?
type: question
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: all2all is listed in HCCL, but its per-primitive dtype, topology and congestion caveats are unverified: the authoritative primitives table 404'd under latest.
auto_inject: false
applicable_when: Before relying on expert-parallel MoE, and whenever a bandwidth figure from HCCL is used to justify topology
confidence: 0.35
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "Once the Supported Primitives table is re-read on the v1.24.2 docs path and its caveats recorded, this question is answered"
tags: ["hccl", "all2all", "docs-gap", "expert-parallel", "open-question", "author-inference"]
edges: [
  {"target": "fact-hccl-includes-all2all", "type": "depends_on", "weight": 0.8, "note": "The fact this question qualifies: all2all presence is corroborated by snippets, so its limits were never read"},
  {"target": "bookmark-hccl-primitives-table", "type": "related_to", "weight": 0.9, "note": "The uncaptured source page whose conversion into a fact would close this question"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.9, "note": "R6 assumes all2all is usable at all; caveats could void EP independently of measured bandwidth"},
  {"target": "note-provenance-register", "type": "related_to", "weight": 0.75, "note": "The register carries this item as unverified and says to re-read on the v1.24.2 path if P5 depends on it"}
]
related: ["[[source-hccl-docs-index]]", "[[task-p0-5-benchmark-hccl-collectives]]", "[[hyp-all2all-enables-expert-parallel]]"]
source_url: "Empty"
---

# What Per-Primitive Caveats Apply to HCCL all2all on Suite 1.24.2?

## The question

For suite 1.24.2, does HCCL's all2all carry dtype, topology or configuration caveats — on four cards, RoCE-attached — that bound how an expert-parallel MoE dispatch could be built, and does it behave badly under congestion as the docs' config-sensitivity warning suggests?

## Why it blocks the plan

The roadmap's own register records that the authoritative primitives table returned 404 under `latest`, so all2all's presence rests on secondary search snippets rather than the table. That makes `fact-hccl-includes-all2all` corroborated but not sourced, and every caveat around it unread. A dtype restriction would be decisive: the checkpoint stays FP8 on Gaudi 2 with no INT8 re-expression, so if all2all accepted only wider types, dispatch traffic would go back to BF16 and the bandwidth number P0.5 records would mean something different from what the topology choice assumes.

## What answers it

A re-read of the Supported Primitives table on the v1.24.2 docs path, which converts `bookmark-hccl-primitives-table` into a sourced fact with its caveats itemised, together with the P0.5 measurements from `task-p0-5-benchmark-hccl-collectives` on this four-card fabric.
