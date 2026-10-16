---
id: concept-kv-block-ownership
title: Scheduler-Owned KV Blocks vs Module-Allocated Buffers
type: concept
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Only block-pool memory is counted, ref-counted and reclaimed; module-allocated per-sequence state escapes scheduler accounting and OOMs instead of preempting.
auto_inject: false
applicable_when: When adding per-sequence state to a model module, or debugging an OOM at concurrency on 96 GB Gaudi 2
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P2.1 lands and a concurrency ramp at target max-model-len shows no allocation growth outside the block pool, the OOM mechanism here is closed and R2 can be downgraded"
tags: ["kv-cache", "block-allocation", "memory-accounting", "oom", "side-cache", "admission-control"]
edges: [
  {"target": "task-p2-1-side-caches-to-kv-blocks", "type": "related_to", "weight": 0.95, "note": "That task is the direct remedy: it moves the QSA, PLE and n-gram buffers into the pool this node describes"},
  {"target": "hyp-side-caches-oom-at-concurrency", "type": "related_to", "weight": 0.9, "note": "The mechanism here is why that hypothesis predicts an OOM at target concurrency rather than a throughput regression"},
  {"target": "concept-prefix-caching-semantics", "type": "supports", "weight": 0.8, "note": "State that the block pool does not own cannot be invalidated with the block that owns its prefix, which underpins that node's argument"},
  {"target": "concept-gdn-gated-delta-net", "type": "related_to", "weight": 0.7, "note": "GDN's mutable recurrent state is the reason the architecture needs mamba-style cache-group handling rather than plain KV blocks"},
  {"target": "cust-phase-p2-cache-plumbing", "type": "related_to", "weight": 0.9, "note": "P2 exists because of this distinction; its exit criterion is stability at concurrency 8+ without side-cache OOM"}
]
related: ["[[task-p2-1-side-caches-to-kv-blocks]]", "[[hyp-side-caches-oom-at-concurrency]]", "[[concept-prefix-caching-semantics]]", "[[cust-phase-p2-cache-plumbing]]"]
source_url: "Empty"
---

# Scheduler-Owned KV Blocks vs Module-Allocated Buffers

The KV cache manager allocates a fixed block pool sized from measured free HBM, hands blocks to sequences through a block table, ref-counts them, and drives admission control and preemption from a single number: blocks available. That control loop is sound only if the pool is the sole allocator of per-sequence memory. A buffer a module allocates for itself — a per-state-slot tensor in a custom cache — sits outside it. The scheduler cannot see it, cannot reclaim it when a sequence finishes, and cannot refuse an admission because of it.

This port allocates a great deal of that invisible state: the QSA raw-key ring, the compressed-key side cache, the PLE dilated-conv taps, and the n-gram trailing-token history. Each grows with the number of live sequences, and each was sized by code written against a Gaudi 3 card with more HBM. On 96 GB the consequence is the difference between graceful degradation and a crash. With block ownership, memory exhaustion means the scheduler defers or preempts a request. With module ownership, exhaustion surfaces as an allocation failure inside a kernel launch while the scheduler still believes it has blocks to hand out.

P2.1 therefore moves that state onto scheduler-owned blocks so it is counted, ref-counted, and freed with the sequence it belongs to; P2.3 separately confirms that decode block buckets clamp to the physical KV cache size, so the pool's own sizing cannot overshoot either.
