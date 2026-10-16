---
id: cust-phase-p2-cache-plumbing
title: "P2 — Cache & Memory Plumbing (HBM Fit + Prefix Caching)"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Move module-allocated side caches (QSA rings, compressed keys, PLE state, n-gram history) onto scheduler-owned KV blocks; keep prefix caching off until that lands."
auto_inject: false
applicable_when: "When executing roadmap phase P2, after the P1 eager port reproduces"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If concurrency 8+ still OOMs after side caches are block-managed, or the v0.30.0 decode-bucket clamp proves inactive, re-open this phase"
tags: ["roadmap-phase", "p2", "kv-cache", "hbm", "prefix-caching"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P2 — goal, three tasks, exit criteria"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "depends_on", "weight": 0.9, "note": "Plumbing targets the running eager port P1 delivers"},
  {"target": "cust-risk-r2-hbm-side-cache-pressure", "type": "related_to", "weight": 0.95, "note": "P2.1 block-managed side caches are the stated mitigation for R2's high/high HBM pressure"},
  {"target": "hyp-side-caches-oom-at-concurrency", "type": "related_to", "weight": 0.9, "note": "The concurrency-8+ exit criterion is the test that settles the OOM hypothesis"},
  {"target": "concept-kv-block-ownership", "type": "depends_on", "weight": 0.8, "note": "The migration target — scheduler-owned KV blocks vs module-allocated buffers — is defined here"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.7, "note": "P5 depends on P2: usable throughput needs a stable memory footprint first"}
]
related: ["[[concept-kv-block-ownership]]", "[[decision-prefix-cache-off-until-p2-1]]", "[[cust-risk-r2-hbm-side-cache-pressure]]"]
source_url: "Empty"
---

# P2 — Cache & Memory Plumbing (HBM Fit + Prefix Caching)

## Goal
Stable under concurrency and correct prefix-cache semantics: migrate the module-allocated side caches onto scheduler-owned KV blocks — the PR's tracked follow-up, more urgent on Gaudi 2's smaller 96GB HBM — and keep prefix caching off until that migration lands.

## Depends on
P1 (eager port reproducing). Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5, with the cheap pin check placed before heavy kernel authoring; P2 rides in parallel after P1 ahead of P5.

## Tasks
- [[task-p2-1-side-caches-to-kv-blocks]] — migrate the QSA raw-key ring, compressed-key side cache, PLE dilated-conv state and n-gram trailing-token history onto scheduler-owned KV blocks.
- [[task-p2-2-keep-prefix-caching-off]] — keep prefix caching OFF until the P2.1 migration lands (hybrid default on HPU).
- [[task-p2-3-verify-decode-bucket-clamp]] — confirm the plugin v0.30.0 decode-block-bucket clamp to physical KV cache size is active.

## Exit criteria
Stable at concurrency 8+ without side-cache OOM; prefix cache correctness restored after P2.1.
