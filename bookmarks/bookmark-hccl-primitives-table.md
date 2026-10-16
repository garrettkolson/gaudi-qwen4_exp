---
id: bookmark-hccl-primitives-table
title: "Unprocessed: HCCL Supported Primitives Table (404 under latest)"
type: bookmark
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Un-ingested pointer to the HCCL supported-collective-primitives table that 404s under the latest docs path; the authority on per-primitive all2all caveats."
auto_inject: false
applicable_when: "When the P0.5 result or an EP decision depends on per-primitive dtype and topology caveats rather than the mere existence of all2all"
confidence: 0.3
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the table resolves at a versioned v1.24.2 documentation path, capture and convert it immediately; until then all2all existence rests on secondary snippets, not the authoritative page"
tags: ["bookmark", "unprocessed", "hccl", "primitives", "all2all", "404"]
edges: [
  {"target": "source-hccl-docs-index", "type": "derived_from", "weight": 0.85, "note": "The index page is what was reachable; this bookmark is the table the index points to and that 404'd"},
  {"target": "question-hccl-primitive-caveats", "type": "related_to", "weight": 0.9, "note": "This table is the document that would answer the open question on per-primitive caveats"},
  {"target": "fact-hccl-includes-all2all", "type": "related_to", "weight": 0.8, "note": "The fact's confidence is capped at 0.65 precisely because this page never resolved; existence is not throughput"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.75, "note": "R6 stays open partly because the table's caveats on collectives and congestion were never read"}
]
related: ["[[question-hccl-primitive-caveats]]", "[[fact-hccl-includes-all2all]]", "[[ref-hccl-benchmarking-docs]]"]
source_url: "Empty"
---

# Unprocessed: HCCL Supported Primitives Table (404 under latest)

Pointer: the HCCL "Supported Collective Primitives" table in the Gaudi software suite documentation, which returned 404 under the `latest` path when the roadmap was written. It matters because it is the authority on which collectives exist, at which dtypes, and under what topology constraints — the roadmap's all2all claim is corroborated only by secondary search snippets, and its author flags the per-primitive caveats as unverified.

Ingesting a captured copy (ideally from the versioned v1.24.2 path) and converting it would raise or correct `fact-hccl-includes-all2all`, answer `question-hccl-primitive-caveats`, tighten `cust-risk-r6-hccl-all2all-bandwidth`, and let P5's EP decision rest on documented constraints instead of inference.
