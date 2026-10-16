---
id: cust-risk-r2-hbm-side-cache-pressure
title: R2 — 96GB HBM Pressure From Eager Sparse-MoE Workspace
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Eager sparse-MoE workspace plus module-allocated side caches may not fit 96GB HBM at target concurrency on Gaudi 2.
auto_inject: false
applicable_when: When choosing max-model-len and memory utilization, or raising concurrency above single digits
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a concurrency ramp at target max-model-len on Gaudi 2 reaches the target load without side-cache OOM, this risk is retired"
tags: ["roadmap-risk", "r2", "high", "hbm", "kv-cache", "memory-planning"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.85, "note": "Roadmap risk R2, probability high, impact high, transcribed from the risks block"},
  {"target": "hyp-side-caches-oom-at-concurrency", "type": "depends_on", "weight": 0.9, "note": "The high probability assumes the four module-allocated caches grow past the budget at concurrency; untested"},
  {"target": "cust-phase-p2-cache-plumbing", "type": "related_to", "weight": 0.95, "note": "P2 exists to retire this risk by moving side caches onto scheduler-owned blocks"},
  {"target": "fact-gaudi2-hbm-and-bandwidth", "type": "derived_from", "weight": 0.9, "note": "96GB HBM2E at 2.45 TB/s per card is the budget the Gaudi 3 port was never sized against"},
  {"target": "task-p2-1-side-caches-to-kv-blocks", "type": "related_to", "weight": 0.9, "note": "The specific migration that removes uncontrolled growth from the HBM budget"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.8, "note": "P0.3 re-derives TP, max-model-len and utilization from this constraint before anything else is planned"}
]
related: ["[[hyp-side-caches-oom-at-concurrency]]", "[[task-p2-1-side-caches-to-kv-blocks]]", "[[fact-gaudi2-hbm-and-bandwidth]]"]
source_url: "Empty"
---
# R2 — 96GB HBM Pressure From Eager Sparse-MoE Workspace

## Exposure

high / high. The roadmap states the exposure as "Gaudi 2 HBM (96GB/2.45TB/s) pressures eager sparse-MoE workspace + QSA side caches." Four buffers are allocated per state slot by the modules rather than by the scheduler: the QSA raw-key ring, the compressed-key side cache, PLE dilated-conv state, and n-gram trailing-token history. They grow with concurrency outside scheduler control, on top of an eager sparse-MoE workspace, in a card with 32 GB less HBM and 1.25 TB/s less bandwidth than the Gaudi 3 box the port was written for. This is the roadmap's only high/high risk.

## Mitigation

P2.1 block-managed side caches; lower max-model-len/memory-util. Migrating those four buffers onto scheduler-owned KV blocks puts their growth inside the same accounting as the KV cache, which is also the precondition for prefix caching and for the decode bucket clamp to mean anything. Trimming context length and utilization is the immediate knob; block ownership is the real fix.

## Trigger to watch

Rising allocation failure or fragmentation as concurrency climbs, allocator growth that does not track batch size, or any preemption pattern in the logs before the KV cache reports full. A single OOM at concurrency 8+ with the KV cache under half its budget is the confirmation.
