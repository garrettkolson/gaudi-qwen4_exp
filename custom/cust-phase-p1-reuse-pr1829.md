---
id: cust-phase-p1-reuse-pr1829
title: "P1 — Reuse PR #1829, Retarget to Gaudi 2 / Plugin 0.30.0"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Retarget the working eager PR #1829 port (~2.4k lines) from Gaudi 3 to Gaudi 2 on plugin 0.30.0 — reuse, not re-derivation, until the smoke battery reproduces."
auto_inject: false
applicable_when: "When executing roadmap phase P1, after the P0 gate has passed"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the PR #1829 smoke battery cannot reproduce on Gaudi 2 after the 0.30.0 retarget, or the pin diverges from plugin 0.30.0, re-scope this phase"
tags: ["roadmap-phase", "p1", "reuse", "porting", "pr1829"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P1 — goal, five tasks, exit criteria"},
  {"target": "cust-phase-p0-platform-gate", "type": "depends_on", "weight": 0.9, "note": "P1 begins only after the P0 gate passes and the Gaudi 2 sizing is established"},
  {"target": "pillar-reuse-over-rederivation", "type": "supports", "weight": 0.95, "note": "This phase is the pillar in practice: retarget the ~2.4k-line eager port instead of deriving the model fresh"},
  {"target": "cust-phase-p2-cache-plumbing", "type": "followed_by", "weight": 0.8, "note": "Cache plumbing operates on the port this phase produces"},
  {"target": "cust-phase-p3-custom-kernels", "type": "followed_by", "weight": 0.8, "note": "P3 replaces the eager fallbacks this phase first gets running correctly"},
  {"target": "cust-phase-p4-pin-check", "type": "followed_by", "weight": 0.8, "note": "The pin check runs against the retargeted build produced here"}
]
related: ["[[decision-reuse-pr1829-as-base]]", "[[fact-pr1829-scope-and-limits]]", "[[source-vllm-gaudi-pr1829]]", "[[ref-vllm-gaudi-plugin]]"]
source_url: "Empty"
---

# P1 — Reuse PR #1829, Retarget to Gaudi 2 / Plugin 0.30.0

## Goal
Correct eager forward via reuse, not re-derivation: base the port on `vllm_gaudi/models/qwen4_exp.py` (~2.4k lines covering GDN 48V/16QK/128, QSA, PLE and HyperConnection), register both model classes, retarget the pin, carry the FP8 MoE fix, and drop the head the plugin cannot serve.

## Depends on
P0 (gate passed, sizing established). Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5, with the cheap pin check placed before heavy kernel authoring.

## Tasks
- [[task-p1-1-port-qwen4-exp-model]] — base the port on qwen4_exp.py, reusing HpuGatedDeltaNetAttention, QSA, PLE and HpuGatedResidual.
- [[task-p1-2-register-model-and-runner]] — register Qwen4ExpForCausalLM and Qwen4ExpForConditionalGeneration; add the arch to maybe_set_mamba_kv_cache_groups_ids.
- [[task-p1-3-retarget-pin-to-0-30-0]] — move from pin dd3bc9c72faf to the plugin 0.30.0 stable pin, satisfying c05d75a+.
- [[task-p1-4-carry-fp8-moe-block-fix]] — carry the _effective_moe_block_size FP8 MoE block-grid fix from extension/ops.py.
- [[task-p1-5-honor-not-convert-drop-mtp]] — honour modules_to_not_convert and drop the mtp.* head at load.

## Exit criteria
The PR smoke battery — arithmetic, geography, code, needle retrieval — reproduces on Gaudi 2.
