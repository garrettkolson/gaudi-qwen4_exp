---
id: task-p2-1-side-caches-to-kv-blocks
title: Move Side Caches onto Scheduler-Owned KV Blocks
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Move the QSA raw-key ring, compressed-key side cache, PLE dilated-conv state and n-gram trailing-token history from module-allocated buffers onto scheduler-owned KV blocks.
auto_inject: false
applicable_when: P2 cache and memory plumbing is active; precondition met when the P1 exit criterion holds — the PR #1829 smoke battery reproduces on Gaudi 2 after the 0.30.0 retarget
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If an upstream vllm-gaudi release ships scheduler-owned block management for these four side caches, this task becomes an adoption of that mechanism rather than an authoring migration"
tags: ["roadmap-task", "p2", "hbm", "kv-blocks", "side-caches"]
edges: [
  {"target": "cust-phase-p2-cache-plumbing", "type": "part_of", "weight": 0.9, "note": "P2 task P2.1; the core migration of the cache and memory plumbing phase"},
  {"target": "concept-kv-block-ownership", "type": "depends_on", "weight": 0.95, "note": "Migration target is scheduler-owned KV blocks; without that ownership model the buffers have nowhere to move to"},
  {"target": "hyp-side-caches-oom-at-concurrency", "type": "related_to", "weight": 0.85, "note": "Success at concurrency 8+ on 96GB tests the hypothesis that module-allocated side caches OOM at target concurrency"},
  {"target": "cust-risk-r2-hbm-side-cache-pressure", "type": "related_to", "weight": 0.9, "note": "Implements the R2 mitigation — block-managed side caches against eager sparse-MoE workspace pressure on 96GB/2.45TB/s"},
  {"target": "task-p6-3-enable-prefix-caching", "type": "followed_by", "weight": 0.8, "note": "The P6 prefix-caching re-enablement is gated on this migration landing first"}
]
related: ["[[concept-kv-block-ownership]]", "[[cust-risk-r2-hbm-side-cache-pressure]]", "[[task-p6-3-enable-prefix-caching]]"]
source_url: "Empty"
---
# Move Side Caches onto Scheduler-Owned KV Blocks

Migrate the four module-allocated side caches — QSA raw-key ring, compressed-key side cache, PLE dilated-conv state, n-gram trailing-token history — from per-state-slot buffers to scheduler-owned KV blocks. On Gaudi 2's 96GB HBM this matters more than on the Gaudi 3 reference the port came from: module-allocated buffers grow with concurrency outside scheduler control, and the roadmap flags the eager sparse-MoE workspace plus these side caches as the highest-probability HBM pressure. The migration is a tracked follow-up of PR #1829, retargeted to 4x Gaudi 2. Done when: stable at concurrency 8+ without side-cache OOM.
