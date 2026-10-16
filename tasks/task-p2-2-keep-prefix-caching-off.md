---
id: task-p2-2-keep-prefix-caching-off
title: Keep Prefix Caching OFF Until P2.1 Lands
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Keep prefix caching disabled through P2 so hybrid side-cache state is never reused across requests; it returns only after P2.1 block-manages the side caches.
auto_inject: false
applicable_when: P2 cache and memory plumbing is active; live from P2 start — in force once the P1 retarget lands and until P2.1 lands
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P2.1 lands and prefix caching passes its correctness regressions, this instruction is obsolete; it would be wrongly specified if prefix caching proved safe with module-allocated side caches"
tags: ["roadmap-task", "p2", "prefix-caching", "correctness"]
edges: [
  {"target": "cust-phase-p2-cache-plumbing", "type": "part_of", "weight": 0.9, "note": "P2 task P2.2; the correctness guardrail of the cache plumbing phase"},
  {"target": "concept-prefix-caching-semantics", "type": "depends_on", "weight": 0.9, "note": "The prohibition rests on prefix-cache semantics being incorrect over hybrid state while side caches are module-allocated"},
  {"target": "decision-prefix-cache-off-until-p2-1", "type": "related_to", "weight": 0.9, "note": "Executes the recorded decision — correctness before a feature nobody can serve correctly yet"}
]
related: ["[[concept-prefix-caching-semantics]]", "[[decision-prefix-cache-off-until-p2-1]]", "[[task-p2-1-side-caches-to-kv-blocks]]"]
source_url: "Empty"
---
# Keep Prefix Caching OFF Until P2.1 Lands

Keep prefix caching disabled through P2, the hybrid default on HPU, until P2.1 lands. The model mixes GDN linear-attention state, QSA side caches and PLE/n-gram state; with those caches module-allocated, a cached KV prefix could be reused while the side caches still hold per-request history — shared prefixes would corrupt hybrid state. Correctness gates the feature: nobody gains from a cache hit that trades away output correctness on Gaudi 2. Verification is a configuration check — the serving flags and scheduler settings show prefix caching off across the concurrency ramp. Done when: stable at concurrency 8+ without side-cache OOM, with prefix-cache correctness restored only after P2.1.
