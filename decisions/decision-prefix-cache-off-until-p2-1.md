---
id: decision-prefix-cache-off-until-p2-1
title: Keep Prefix Caching Disabled Until Side Caches Are Block-Managed
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Prefix caching stays OFF until QSA, PLE and n-gram side caches move onto scheduler-owned KV blocks (P2.1) — correctness before a feature nobody can serve correctly yet.
auto_inject: false
applicable_when: When configuring prefix caching for any P2-era run on Gaudi 2, or when a cache-hit-rate optimisation is proposed
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If an audit shows the QSA/PLE/n-gram state caches are already position-reusable under prefix caching, the correctness premise for keeping it off weakens"
tags: ["decision", "prefix-caching", "correctness", "hbm", "kv-blocks"]
edges: [
  {"target": "concept-prefix-caching-semantics", "type": "depends_on", "weight": 0.9, "note": "The decision is an application of prefix-caching correctness semantics under hybrid state: understands what a stale hit means here"},
  {"target": "task-p2-2-keep-prefix-caching-off", "type": "related_to", "weight": 0.9, "note": "P2.2 is this decision expressed as a task: keep the flag off until P2.1 lands (hybrid default on HPU)"},
  {"target": "task-p2-1-side-caches-to-kv-blocks", "type": "depends_on", "weight": 0.85, "note": "The unblocking condition: migrate QSA ring, compressed-key cache, PLE state and n-gram history to scheduler-owned KV blocks"},
  {"target": "cust-risk-r2-hbm-side-cache-pressure", "type": "related_to", "weight": 0.8, "note": "The same 96GB pressure that makes side-cache migration urgent also makes uncontrolled per-request cache copies unacceptable"}
]
related: ["[[task-p2-2-keep-prefix-caching-off]]", "[[concept-prefix-caching-semantics]]", "[[task-p6-3-enable-prefix-caching]]", "[[concept-kv-block-ownership]]"]
source_url: "Empty"
---

# Keep Prefix Caching Disabled Until Side Caches Are Block-Managed

## Context

Qwen3.8-Flash-Next is a hybrid-state model. Beyond the scheduler-managed KV cache it carries module-allocated buffers: the QSA raw-key ring, a compressed-key side cache, PLE dilated-conv state, and n-gram trailing-token history. Prefix caching assumes reused prefixes imply reused state; with state living outside scheduler-owned KV blocks, a prefix hit can restore KV while the side caches do not correspond to the cached prefix — wrong context, silently. On 96GB Gaudi 2 HBM the side caches are also the pressure point (risk R2, high/high).

## Alternatives considered

Leave prefix caching on and treat incorrect hybrid hits as a known defect. Disable it permanently and forfeit the reuse benefit even after the plumbing is fixed.

## Decision

Keep prefix caching OFF until P2.1 lands — the roadmap's P2.2, noted as the hybrid default on HPU. Correctness before a feature nobody can serve correctly yet.

## Consequence

No cache-hit-rate gains in P2-era benchmarks, and benchmark baselines must state the flag. Re-enablement is a tracked P6 task with regression coverage after P2.1, so the deferral has an owner and an exit instead of becoming permanent drift.
