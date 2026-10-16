---
id: task-p6-3-enable-prefix-caching
title: Re-enable Prefix Caching With Regression Coverage
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Deferred until P2.1 lands. Re-enable prefix caching, currently held off by P2.2, with regression coverage proving reuse is correct under hybrid state on the 96GB card.
auto_inject: false
applicable_when: P6 (cust-phase-p6-feature-parity) — deferred; live only after task-p2-1 side-cache block management lands and text-only serving is already enabled.
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P2.1 is abandoned, prefix caching stays off indefinitely and this task is void; if regression runs show reuse is already correct under current block management, the task shrinks to a flag change plus tests."
tags: ["roadmap-task", "p6", "deferred", "prefix-caching", "kv-blocks"]
edges: [
  {"target": "cust-phase-p6-feature-parity", "type": "part_of", "weight": 0.9, "note": "P6 task, explicitly deferred and not part of text-only serving enablement"},
  {"target": "concept-prefix-caching-semantics", "type": "depends_on", "weight": 0.9, "note": "Correct reuse under hybrid state is defined by this concept; the regression suite must encode it"},
  {"target": "task-p2-1-side-caches-to-kv-blocks", "type": "depends_on", "weight": 0.95, "note": "Hard precondition: caching can only be trusted once side caches are scheduler-owned KV blocks"},
  {"target": "task-p2-2-keep-prefix-caching-off", "type": "contradicts", "weight": 0.8, "note": "This task lifts the P2.2 prohibition; the two hold at different points in time, sequenced by P2.1"}
]
related: ["[[cust-phase-p6-feature-parity]]", "[[task-p2-2-keep-prefix-caching-off]]", "[[concept-prefix-caching-semantics]]", "[[decision-defer-feature-parity-p6]]"]
source_url: "Empty"
---
# Re-enable Prefix Caching With Regression Coverage

Deferred until P2.1 lands — not required for text-only serving. Re-enable prefix caching, which P2.2 keeps off, and add regression coverage proving reused prefixes are correct under the model's hybrid state: the QSA raw-key ring, compressed-key cache, PLE dilated-conv state, and n-gram trailing-token history must all round-trip through scheduler-owned KV blocks, or a reused prefix silently diverges. On the 96GB Gaudi 2 card this is also where the P2.1 block management earns its keep.

Done when: the per-feature criterion is met — prefix caching is enabled with passing regression coverage; text-only serving enablement does not wait for this.
