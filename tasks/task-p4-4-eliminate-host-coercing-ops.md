---
id: task-p4-4-eliminate-host-coercing-ops
title: Remove Host-Coercing Ops From QSA/PLE Hot Paths
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Delete the host-coercing ops in QSA/PLE hot paths — .nonzero in PLE _pool_and_store, .item(), torch.minimum in _expand_plan, keep.any() in the KV-store epilogue — to unblock capture.
auto_inject: false
applicable_when: P4b (cust-phase-p4-capture) — live once the P4a capture record shows these hot-path ops coercing to host and failing HPU graph capture.
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the QSA/PLE hot paths in plugin 0.30.0 no longer contain these ops, or a fresh capture-triage boot log shows different host syncs, this op list is stale and must be re-derived."
tags: ["roadmap-task", "p4-capture", "graph-capture", "host-coercion", "qsa", "ple"]
edges: [
  {"target": "cust-phase-p4-capture", "type": "part_of", "weight": 0.9, "note": "P4b cannot leave eager-only while hot-path ops force host syncs during capture"},
  {"target": "concept-qsa-indexer", "type": "related_to", "weight": 0.85, "note": "The KV-store epilogue keep.any() and _expand_plan torch.minimum sit in the QSA path"},
  {"target": "concept-ple-dilated-conv-ngram", "type": "related_to", "weight": 0.85, "note": "The .nonzero in PLE _pool_and_store is the PLE-side host-coercing op named by the roadmap"},
  {"target": "concept-graph-capture-vs-eager", "type": "depends_on", "weight": 0.85, "note": "Host coercion is precisely what breaks graph capture; the concept defines the failure mechanism"}
]
related: ["[[cust-phase-p4-capture]]", "[[playbook-graph-capture-triage]]", "[[concept-qsa-indexer]]", "[[concept-ple-dilated-conv-ngram]]"]
source_url: "Empty"
---
# Remove Host-Coercing Ops From QSA/PLE Hot Paths

Eliminate the host-coercing ops in the QSA/PLE hot paths: `.nonzero` in PLE `_pool_and_store`, `.item()` calls, `torch.minimum` in `_expand_plan`, and `keep.any()` in the KV-store epilogue. Each forces a device-to-host sync and breaks HPU graph capture, keeping the model eager-bound on Gaudi 2 where removing compiled-mode overhead matters most. Rewrite each to a shape-stable, device-resident equivalent that stays byte-equal to the eager reference — correctness first, capture second.

Done when: the boot without --enforce-eager covers these subgraphs and the rest serves compiled, with a documented per-subgraph eager fallback remaining for the QSA indexer only.
