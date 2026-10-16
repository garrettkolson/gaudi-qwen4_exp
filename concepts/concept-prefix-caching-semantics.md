---
id: concept-prefix-caching-semantics
title: Prefix Caching Correctness Under Hybrid State
type: concept
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Prefix reuse is sound only when all conditioning state is block-owned and content-keyed; module-allocated QSA and PLE state makes a hit silently wrong.
auto_inject: false
applicable_when: When considering enabling prefix caching, or auditing what state a prefix cache hit must restore
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P2.1 lands with every side cache block-managed, the off-by-default conclusion here expires and P6.3's regression coverage defines the semantics instead"
tags: ["prefix-caching", "hybrid-state", "cache-invalidation", "correctness", "kv-cache"]
edges: [
  {"target": "task-p2-2-keep-prefix-caching-off", "type": "related_to", "weight": 0.9, "note": "That task is the operational form of this analysis: the flag stays off while the unsound state exists"},
  {"target": "task-p6-3-enable-prefix-caching", "type": "related_to", "weight": 0.9, "note": "Re-enabling is deferred to P6.3 with regression coverage, which is the only path to a sound hit on this model"},
  {"target": "concept-kv-block-ownership", "type": "depends_on", "weight": 0.85, "note": "The argument that side state cannot be invalidated with a prefix rests on the distinction between block-owned and module-owned memory"},
  {"target": "decision-prefix-cache-off-until-p2-1", "type": "related_to", "weight": 0.9, "note": "That decision is the consequence of this correctness reading, chosen over shipping a feature nobody could serve correctly"},
  {"target": "concept-ple-dilated-conv-ngram", "type": "related_to", "weight": 0.75, "note": "PLE conv taps and trailing-token history are the clearest example of state a content-keyed KV hit does not restore"}
]
related: ["[[concept-kv-block-ownership]]", "[[decision-prefix-cache-off-until-p2-1]]", "[[task-p6-3-enable-prefix-caching]]", "[[concept-ple-dilated-conv-ngram]]"]
source_url: "Empty"
---

# Prefix Caching Correctness Under Hybrid State

Prefix caching reuses computed KV blocks across requests sharing a leading token sequence. A full, immutable block is keyed by its content; a new request whose prefix hashes to that key skips recomputation and ref-counts the block instead of recomputing or copying it. The correctness requirement is strict: everything that conditions future computation for that prefix must be equally content-addressable, equally immutable, and equally reclaimed with the block.

Qwen3.8-Flash-Next breaks that requirement, which is why the roadmap keeps prefix caching off until P2.1 lands. Several pieces of conditioning state are allocated inside modules, per state slot: the QSA indexer's raw-key ring and compressed-key side cache, the PLE dilated-conv left-context taps, and the n-gram trailing-token history. The prefix cache neither keys nor frees them, and the position-indexed contents are not derivable from the KV block alone. The failure is silent rather than safe — a resumed request can find correct KV blocks alongside stale or missing side state, and emit wrong tokens instead of reporting a cache miss. GDN's recurrent state is mutated in place rather than appended, so it is not an immutable prefix under any allocator.

The sequence follows directly: prefix caching stays off through P2, side state migrates onto scheduler-owned blocks in P2.1 so it becomes block-addressable and reclaimable with the block that owns it, and only then is caching re-enabled in P6.3 with regression coverage.
