---
id: ref-hccl-benchmarking-docs
title: "HCCL Testing & Benchmarking Documentation"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "HCCL documentation set — Gaudi's NCCL emulation layer — covering supported collective primitives plus the testing/benchmarking tool P0.5 measures with."
auto_inject: false
applicable_when: "When running the P0.5 allreduce/allgather/all2all bandwidth benchmark, or before choosing TP versus EP topology"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the Suite 1.24.2 documentation path no longer serves the testing/benchmarking section, or the benchmarking tool no longer reports the collective set P0.5 needs, the measurement path this reference names is gone"
tags: ["hccl", "benchmarking", "collectives", "all2all", "suite-1-24-2", "documentation"]
edges: [
  {"target": "playbook-hccl-collective-benchmark", "type": "related_to", "weight": 0.9, "note": "The playbook turns this documentation's benchmarking tool into the P0.5 procedure"},
  {"target": "concept-hccl-collective-layer", "type": "related_to", "weight": 0.85, "note": "The concept node positions HCCL as Gaudi's NCCL emulation layer, which is what these docs describe"},
  {"target": "task-p0-5-benchmark-hccl-collectives", "type": "related_to", "weight": 0.85, "note": "P0.5 measures allreduce/allgather/all2all with the tooling documented here"},
  {"target": "bookmark-hccl-primitives-table", "type": "related_to", "weight": 0.8, "note": "The supported-primitives table under this documentation set 404'd under latest and is held as an unprocessed bookmark"},
  {"target": "source-hccl-docs-index", "type": "related_to", "weight": 0.85, "note": "The index page is the only part of this set the roadmap actually corroborates; the primitives table did not resolve"}
]
related: ["[[bookmark-hccl-primitives-table]]", "[[fact-hccl-includes-all2all]]", "[[question-hccl-primitive-caveats]]"]
source_url: "Empty"
---

# HCCL Testing & Benchmarking Documentation

HCCL is Gaudi's NCCL emulation layer, and its documentation set has two parts the roadmap depends on: the supported collective primitives table, and a testing/benchmarking section describing how to drive and measure collectives. P0.5 uses the latter to measure allreduce, allgather and all2all on this 4-card fabric before any TP/EP topology is fixed. Current known state per the roadmap: the documentation index corroborates that both sections exist and that the collective set includes allreduce, allgather, reduce-scatter and all2all — but the corroboration came from secondary search snippets, and the authoritative primitives table page returned 404 under the `latest` documentation path, so per-primitive dtype and topology caveats are unverified and the roadmap's own provenance register says so.

Before relying on this: resolve the versioned v1.24.2 path rather than `latest`, read the primitives table itself, confirm all2all's supported dtypes and rank/topology constraints, and check the benchmarking tool's flags and output units before quoting any bandwidth number from it.
