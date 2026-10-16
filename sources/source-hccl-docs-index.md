---
id: source-hccl-docs-index
title: HCCL Documentation Index (Suite 1.24.2)
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "HCCL docs index for suite 1.24.2 — Gaudi's NCCL emulation layer. Corroborates the collective list including all2all; the authoritative primitives table 404'd, so caveats stay unverified."
auto_inject: false
applicable_when: "Before choosing a TP or EP topology on HCCL collective behaviour, or when reading all2all existence as if it were all2all throughput"
confidence: 0.6
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the HCCL supported-primitives table is read on the v1.24.2 path and contradicts the collective list, or names dtype or topology caveats for all2all, fact-hccl-includes-all2all and question-hccl-primitive-caveats change"
tags: ["hccl", "collectives", "all2all", "gaudi-2", "docs", "partial-retrieval"]
edges: [
  {"target": "fact-hccl-includes-all2all", "type": "supports", "weight": 0.7, "note": "The index corroborates the collective list; the primitives table itself 404'd, so support is partial and confidence stays capped"},
  {"target": "concept-hccl-collective-layer", "type": "supports", "weight": 0.8, "note": "HCCL as Gaudi's NCCL emulation layer, with testing and benchmarking docs, is what this index page establishes"},
  {"target": "question-hccl-primitive-caveats", "type": "related_to", "weight": 0.85, "note": "The missing table is exactly the gap this question tracks — existence of a primitive is not its dtype or topology envelope"},
  {"target": "bookmark-hccl-primitives-table", "type": "related_to", "weight": 0.85, "note": "The page that returned 404 under 'latest' is bookmarked for retrieval on the versioned path"}
]
related: ["[[fact-hccl-includes-all2all]]", "[[concept-hccl-collective-layer]]", "[[bookmark-hccl-primitives-table]]", "[[playbook-hccl-collective-benchmark]]"]
source_url: "Empty"
---
# HCCL Documentation Index (Suite 1.24.2)

The HCCL documentation index for Gaudi software suite 1.24.2. HCCL is Gaudi's NCCL emulation layer; the index page shows sections for supported collective primitives and for testing and benchmarking, and corroborates a collective list that includes allreduce, allgather, reduce-scatter and all2all. The roadmap is explicit about the limits of this retrieval: the authoritative primitives table returned 404 under the `latest` path, and the collective list was additionally corroborated by secondary search snippets rather than read from the table itself.

That gap is load-bearing. `fact-hccl-includes-all2all` is capped at 0.65 because of it, `question-hccl-primitive-caveats` tracks the unread per-primitive dtype and topology caveats, and `bookmark-hccl-primitives-table` holds the failed URL for a retry on the versioned path. Expert-parallel feasibility in R6 and P5.3 depends on measured all2all throughput, which no documentation page substitutes for. No URL is recorded: the roadmap gives none and the `latest` path was already dead.
