---
id: fact-hccl-includes-all2all
title: HCCL Exposes allreduce, allgather, reduce-scatter and all2all
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: HCCL, Gaudi's NCCL emulation layer, exposes allreduce, allgather, reduce-scatter and all2all; corroborated by secondary snippets (primitives table 404'd), per-primitive caveats unverified.
auto_inject: false
applicable_when: "Empty"
confidence: 0.65
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the authoritative HCCL Supported Primitives table on the v1.24.2 path (which 404'd under 'latest') shows all2all absent or restricted, or a P0.5 HCCL benchmark cannot execute all2all, this claim is invalidated"
tags: ["hccl", "all2all", "collectives", "nccl-emulation", "expert-parallel"]
edges: [
  {"target": "concept-hccl-collective-layer", "type": "related_to", "weight": 0.85, "note": "HCCL as Gaudi's NCCL emulation layer is the concept framing this primitive list"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "supports", "weight": 0.7, "note": "Primitive existence underpins R6, but only weakly: existence is not throughput on the Gaudi 2 fabric"},
  {"target": "question-hccl-primitive-caveats", "type": "related_to", "weight": 0.9, "note": "Per-primitive dtype/topology caveats remain open because the authoritative table 404'd"},
  {"target": "source-hccl-docs-index", "type": "derived_from", "weight": 0.8, "note": "The HCCL documentation index corroborates the collective list; the primitives table page 404'd"}
]
related: ["[[concept-hccl-collective-layer]]", "[[cust-risk-r6-hccl-all2all-bandwidth]]", "[[question-hccl-primitive-caveats]]", "[[source-hccl-docs-index]]"]
source_url: "Empty"
---

# HCCL Exposes allreduce, allgather, reduce-scatter and all2all

HCCL, Intel Gaudi's NCCL emulation layer, is documented as exposing the collective primitives allreduce, allgather, reduce-scatter, and all2all, together with Supported Collective Primitives and Testing/Benchmarking pages. The roadmap records this under `evidence_grounded` and in the R6 source note ("HCCL index ... Collectives incl. allreduce/allgather/reducescatter/all2all corroborated via search snippets").

Confidence is capped at 0.65 by the Confidence Policy: this is secondary-source-only corroboration, not an authoritative citation. The roadmap's own `author_inference_flagged` list states plainly that the HCCL Supported_Primitives authoritative table returned 404 under the `latest` path, that all2all-existence is corroborated by secondary search snippets rather than the primitives table itself, and that per-primitive dtype/topology caveats are UNVERIFIED. It recommends re-reading on the v1.24.2 path if it matters to P5.

Two gaps are stated, not hidden. First, existence of the all2all primitive does NOT establish its throughput on the Gaudi 2 RoCE fabric — that is exactly what P0.5 must measure before any expert-parallel topology is chosen (`cust-risk-r6`). Second, which dtype and topology constraints each primitive carries is unverified (`question-hccl-primitive-caveats`). Nothing is measured, so `verified_at` is Empty.
