---
id: hyp-sparse-topk-not-capturable
title: Sparse Top-k Stays Uncapturable Even as a Single CustomOp
type: hypothesis
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Fusing the QSA sparse top-k into one TPC kernel may still block HPU graph capture, because its data-dependent control flow may be a compiler-layer limit.
auto_inject: false
applicable_when: When deciding whether P4b exits with full compiled serving or with an eager fallback around the QSA indexer
confidence: 0.5
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P4.2 boots without --enforce-eager and the fused sparse top-k subgraph captures, this hypothesis is falsified"
tags: ["sparse-topk", "qsa-indexer", "graph-capture", "hpu-graph", "unverified", "author-inference"]
edges: [
  {"target": "cust-risk-r3-sparse-topk-uncapturable", "type": "supports", "weight": 0.9, "note": "R3 is the exposure this hypothesis explains; its stated mitigation is hybrid compiled+eager for the QSA region only"},
  {"target": "task-p3-1-sparse-topk-kernel", "type": "related_to", "weight": 0.85, "note": "P3.1 produces the single CustomOp whose capturability is in question"},
  {"target": "task-p4-2-boot-without-enforce-eager", "type": "related_to", "weight": 0.85, "note": "P4.2's recorded failure list is the observation that decides the hypothesis"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.6, "note": "Same synapse compileGraph family, but #1734 was about layer boundaries, not data-dependent control flow"},
  {"target": "decision-eager-first-compiled-later", "type": "contradicts", "weight": 0.5, "note": "Weakly: if true it bounds how far removing --enforce-eager can go, leaving a permanent eager island"}
]
related: ["[[cust-phase-p4-capture]]", "[[concept-qsa-indexer]]", "[[playbook-graph-capture-triage]]"]
source_url: "Empty"
---

# Sparse Top-k Stays Uncapturable Even as a Single CustomOp

## Claim

The QSA indexer's sparse top-k selection branches on tensor contents, so the roadmap rates its capture risk "high". Fusing it into one TPC kernel removes dispatch cost, but this hypothesis says the data-dependent control flow sits below the CustomOp boundary — a compiler-layer limit a wrapper cannot lift. That reading is the author's: nothing in the roadmap records Intel saying the `custom_op` namespace makes arbitrary control flow capturable. Until P4.2 runs, treat this as a reason to keep a hybrid path planned, not as a settled ceiling.

## Test that settles it

`task-p3-1-sparse-topk-kernel` delivers the single, byte-equal CustomOp; `task-p4-2-boot-without-enforce-eager` then boots without `--enforce-eager` and records whether the QSA subgraph captures or falls back. A fused op that captures is a direct disproof.

## If it turns out false

If the fused op captures, the hybrid compiled+eager fallback for the QSA region is unnecessary, P4b meets its stronger exit branch (all TP workers serving without `--enforce-eager`), and P3's dispatch savings extend to the indexer rather than stopping at PLE and the n-gram gather.
