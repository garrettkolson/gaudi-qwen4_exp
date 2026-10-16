---
id: cust-phase-p0-platform-gate
title: "P0 — Platform Feasibility & Memory Planning (Gating)"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Gating phase: confirm FP8 is a real runtime path on Gaudi 2 and size TP, max-model-len and memory utilization from measured numbers before anything else proceeds."
auto_inject: false
applicable_when: "When planning or executing roadmap phase P0 — the gate every later phase waits on"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the FP8 checkpoint fails to load on Gaudi 2 eager, or a TP/memory config fits only by contradicting the sizing method here, re-open this phase"
tags: ["roadmap-phase", "p0", "gating", "fp8", "memory-planning", "hccl"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P0 — goal, tasks, exit criteria and gating flag"},
  {"target": "pillar-measured-before-default", "type": "supports", "weight": 0.9, "note": "Operationalises the pillar: TP degree, context length and utilization come from measured numbers, not the Gaudi 3 defaults"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "followed_by", "weight": 0.9, "note": "P1 reuse work starts only after this gate passes"},
  {"target": "cust-risk-r2-hbm-side-cache-pressure", "type": "related_to", "weight": 0.8, "note": "P0.3 sizing of the 96GB HBM budget is the first line of defence against R2 workspace pressure"},
  {"target": "cust-risk-r6-hccl-all2all-bandwidth", "type": "related_to", "weight": 0.9, "note": "P0.5 all2all measurement is the stated mitigation for R6 before any TP/EP topology is fixed"},
  {"target": "cust-risk-r1-fp8-mme-throughput", "type": "related_to", "weight": 0.8, "note": "P0.2 micro-benchmark is the mitigation for R1 — a performance question, not feasibility"},
  {"target": "question-what-tp-degree-fits-gaudi2", "type": "related_to", "weight": 0.9, "note": "This phase's exit criteria answer the question with a measured config"}
]
related: ["[[question-what-tp-degree-fits-gaudi2]]", "[[playbook-hccl-collective-benchmark]]", "[[decision-fp8-no-requantization]]", "[[decision-eager-first-compiled-later]]"]
source_url: "Empty"
---

# P0 — Platform Feasibility & Memory Planning (Gating)

Gating: yes

## Goal
Confirm FP8 is a real runtime path on Gaudi 2 and size HBM/TP correctly. FP8 E4M3/E5M2 is supported, so no re-quantization fork — but throughput is unverified. Everything inherited from the Gaudi 3 reference (TP4, 0.80 util, 128GB) is a starting hypothesis against Gaudi 2's 96GB HBM2E at 2.45 TB/s.

## Depends on
Nothing — this is the first phase and the plan's gate. Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5, with the cheap pin check placed before heavy kernel authoring.

## Tasks
- [[task-p0-1-load-fp8-on-eager]] — load the Qwen3.8-Flash-Next-FP8 checkpoint on Gaudi 2 eager.
- [[task-p0-2-fp8-mme-benchmark]] — benchmark FP8 MME throughput vs the Gaudi 3 1.8 PFlops reference.
- [[task-p0-3-resize-tp-and-memory]] — re-derive TP degree, --max-model-len and --gpu-memory-utilization for 96GB/2.45TB/s.
- [[task-p0-4-set-required-flags]] — set --kv-cache-dtype auto, VLLM_SKIP_WARMUP=true, --enforce-eager, --language-model-only.
- [[task-p0-5-benchmark-hccl-collectives]] — measure allreduce/allgather/all2all bandwidth on the Gaudi 2 fabric before fixing a TP/EP topology.

## Exit criteria
FP8 checkpoint loads and produces deterministic single-token probes on Gaudi 2 eager; a TP + max-model-len + memory-utilization config fits without OOM; measured allreduce/allgather/all2all bandwidth recorded, with TP/EP target chosen from those numbers.
