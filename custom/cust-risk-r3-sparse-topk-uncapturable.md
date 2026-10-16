---
id: cust-risk-r3-sparse-topk-uncapturable
title: R3 — Sparse Top-k Not Graph-Capturable
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: The QSA sparse top-k selection may stay outside HPU graph capture even as a single CustomOp, bounding how far compiled mode can go.
auto_inject: false
applicable_when: When planning P4b compiled-mode scope or promising a fully captured graph on Gaudi 2
confidence: 0.6
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a P4.2 boot without --enforce-eager captures the QSA sparse top-k subgraph on Gaudi 2, this risk is retired"
tags: ["roadmap-risk", "r3", "medium-high", "graph-capture", "qsa", "sparse-topk"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Roadmap risk R3, probability medium-high, impact medium, transcribed from the risks block"},
  {"target": "hyp-sparse-topk-not-capturable", "type": "depends_on", "weight": 0.9, "note": "The probability is the roadmap's inference that data-dependent control flow is a compiler-layer limit"},
  {"target": "cust-phase-p4-capture", "type": "related_to", "weight": 0.9, "note": "P4b is where the risk materialises, as a per-subgraph eager fallback instead of a full compiled graph"},
  {"target": "task-p3-1-sparse-topk-kernel", "type": "related_to", "weight": 0.9, "note": "The single-CustomOp rewrite the roadmap rates high graph-capture risk before it even tests capture"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.6, "note": "Same synapse compileGraph family, but the pin fix that closed it did not touch this control-flow shape"}
]
related: ["[[hyp-sparse-topk-not-capturable]]", "[[task-p3-1-sparse-topk-kernel]]", "[[cust-phase-p4-capture]]"]
source_url: "Empty"
---
# R3 — Sparse Top-k Not Graph-Capturable

## Exposure

medium-high / medium. The roadmap states the exposure as "Sparse top-k not graph-capturable even as a single CustomOp (compiler-layer control-flow limit)." The QSA indexer's selection depends on tensor values, so its control flow is resolved at runtime; the roadmap rates this primitive's graph-capture risk high while rating the PLE conv and n-gram gathers medium. Impact is medium, not high: the primitive still runs correctly in eager, so the cost is dispatch overhead and a partial compiled graph, not a broken model. The probability itself is the roadmap's own inference, not a statement from Intel or the plugin.

## Mitigation

Hybrid compiled+eager for QSA region only. Keep everything else on captured graphs and let the QSA indexer fall back to eager, which P4b already lists as an acceptable exit criterion: a documented per-subgraph eager fallback for the QSA indexer. Authoring P3.1 as one CustomOp in the `custom_op` namespace is the attempt that could remove the fallback; the mitigation is the plan if the attempt fails.

## Trigger to watch

A P4.2 boot without `--enforce-eager` that fails inside the QSA selection or gather, any capture log mentioning dynamic shapes or host syncs in the indexer, or a fused top-k kernel that captures alone but breaks when its output feeds the attention mask.
