---
id: concept-qsa-indexer
title: QSA Indexer and Sparse Attention Selection
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Two-pass attention where a cheap indexer scores keys and selects a data-dependent top-k block set; its side caches and dynamic shapes are the core P3/P4 risk.
auto_inject: false
applicable_when: When authoring or capturing the sparse top-k kernel, or reasoning about QSA side-cache memory
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a P4.2 capture attempt shows the QSA region capturing with fixed-width masked selection, the high capture-risk rating and the hybrid compiled-plus-eager fallback recorded here are obsolete"
tags: ["qsa", "sparse-attention", "top-k", "data-dependent-control-flow", "graph-capture", "side-cache"]
edges: [
  {"target": "fact-model-architecture-blocks", "type": "related_to", "weight": 0.9, "note": "Grounds the component names this node expands: HpuQSAIndexer plus HpuQwen4ExpQSAAttention in the PR #1829 port"},
  {"target": "task-p3-1-sparse-topk-kernel", "type": "related_to", "weight": 0.9, "note": "That task collapses the indexer's selection path into one CustomOp; the data dependence described here is what makes it the hardest of the three"},
  {"target": "concept-tpc-customop-integration", "type": "related_to", "weight": 0.8, "note": "The single-kernel and custom_op namespace limits decide whether a rewritten indexer can ever be captured"},
  {"target": "task-p4-4-eliminate-host-coercing-ops", "type": "related_to", "weight": 0.85, "note": "The host-coercing ops that task removes are exactly the reads of top-k results described here"},
  {"target": "hyp-sparse-topk-not-capturable", "type": "related_to", "weight": 0.85, "note": "That hypothesis is the claim that the data dependence described here is a compiler-layer limit rather than an implementation gap"}
]
related: ["[[concept-tpc-customop-integration]]", "[[task-p3-1-sparse-topk-kernel]]", "[[hyp-sparse-topk-not-capturable]]", "[[concept-graph-capture-vs-eager]]"]
source_url: "Empty"
---

# QSA Indexer and Sparse Attention Selection

QSA splits attention into two passes. A cheap indexer projects the query and the candidate keys into a reduced space, scores them, and selects a small top-k subset of key blocks; the full attention then reads only those blocks. The indexer needs state of its own — a raw-key ring holding the keys it scores against, and a compressed-key side cache of the reduced representations — and neither lives in the attention KV cache.

For this port the indexer is the risk centre of P3 and P4. The roadmap rates sparse top-k as high graph-capture risk, and the reason is structural: which blocks survive, and how many, depend on tensor values, so the shapes and control flow downstream of selection are data-dependent. A captured HPU graph fixes shapes at capture time, so the region either fails to compile or must be rewritten to fixed-width selection with masking, and any host-side read of those values — `.item()`, boolean coercion of a tensor — synchronises the device mid-step. P4.4 exists to strip precisely those ops from the QSA and PLE hot paths, and the accepted outcome if it fails is a hybrid: compiled graph everywhere else, eager for the QSA region only.

Two further consequences follow from the same design. The side caches are module-allocated, so they are invisible to KV block accounting and scale with concurrency. And their contents are position-indexed rather than content-keyed, so prefix reuse is unsound while they exist.
