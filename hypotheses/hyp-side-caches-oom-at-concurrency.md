---
id: hyp-side-caches-oom-at-concurrency
title: Module-Allocated Side Caches OOM at Target Concurrency on 96GB
type: hypothesis
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: QSA rings, compressed-key cache, PLE conv state and n-gram history scale with concurrency outside scheduler accounting; on 96GB they are expected to OOM first.
auto_inject: false
applicable_when: When setting a concurrency target, sizing --max-model-len, or deciding whether prefix caching can be re-enabled
confidence: 0.65
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a concurrency ramp at the P0.3 config reaches concurrency 8+ without a side-cache allocation failure, this hypothesis is falsified"
tags: ["hbm", "side-caches", "kv-blocks", "oom", "concurrency", "unverified"]
edges: [
  {"target": "fact-gaudi2-hbm-and-bandwidth", "type": "depends_on", "weight": 0.85, "note": "The 96GB / 2.45 TB/s budget, well under the Gaudi 3 card the port was written against, is what makes the overflow plausible"},
  {"target": "cust-risk-r2-hbm-side-cache-pressure", "type": "supports", "weight": 0.9, "note": "R2 is the roadmap's high/high exposure; this hypothesis states its concrete failure mode"},
  {"target": "task-p2-1-side-caches-to-kv-blocks", "type": "related_to", "weight": 0.9, "note": "P2.1 is the fix; its exit criterion — stable at concurrency 8+ — is the pass line for this claim"},
  {"target": "concept-kv-block-ownership", "type": "related_to", "weight": 0.85, "note": "The distinction between scheduler-owned blocks and module-allocated buffers is why these caches escape clamping"}
]
related: ["[[cust-phase-p2-cache-plumbing]]", "[[decision-prefix-cache-off-until-p2-1]]", "[[question-what-tp-degree-fits-gaudi2]]"]
source_url: "Empty"
---

# Module-Allocated Side Caches OOM at Target Concurrency on 96GB

## Claim

Four buffers are allocated by model modules rather than the scheduler: the QSA raw-key ring, the compressed-key side cache, PLE dilated-conv state, and n-gram trailing-token history. Their footprint scales with concurrent sequences and context length, and they sit outside the KV block accounting that clamps decode buckets — so the scheduler can admit work the allocator cannot back. On 96GB, against the 128GB card PR #1829 was written for, the expectation is an allocation failure before the intended concurrency is reached. The roadmap rates this high/high and PR #1829 already tracked the migration as a follow-up. None of it has been reproduced on this hardware.

## Test that settles it

A concurrency ramp at the max-model-len and utilization chosen in P0.3, run before `task-p2-1-side-caches-to-kv-blocks` lands, watching for allocation failure in the side caches specifically rather than in the KV pool. P2's exit criterion is the pass line: stable at concurrency 8+ without side-cache OOM, which P2.1 then makes durable.

## If it turns out false

If the ramp clears concurrency 8 unmodified, P2.1 drops from blocker to hygiene, prefix caching can be re-enabled earlier than P6, and P0's memory sizing has headroom to spend on longer context instead of on admitting more sequences.
