---
id: pillar-reuse-over-rederivation
title: Reuse the Working Port, Do Not Re-Derive the Model
type: pillar
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: A working eager port exists in vllm-gaudi PR #1829 (~2.4k lines); the job is retargeting it to Gaudi 2 / plugin 0.30.0, not deriving the model from scratch.
auto_inject: false
applicable_when: When scoping the Qwen3.8-Flash-Next port onto vllm-gaudi, or when tempted to rewrite a component PR #1829 already implements
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PR #1829's qwen4_exp.py proves un-retargetable to plugin 0.30.0 within P1's scope, the reuse premise this pillar rests on no longer holds"
tags: ["strategy", "reuse", "pr-1829", "scope-control", "port-strategy"]
edges: [
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.9, "note": "The pillar names a concrete artifact: PR #1829's eager-only Qwen4Exp port in vllm_gaudi/models/qwen4_exp.py"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "related_to", "weight": 0.9, "note": "P1 operationalizes the pillar: base on the PR file, register classes, retarget the pin, carry the block-grid fix"},
  {"target": "decision-reuse-pr1829-as-base", "type": "supports", "weight": 0.95, "note": "The pillar is the standing rationale that grounds the decision to base the port on the PR rather than author anew"}
]
related: ["[[cust-phase-p1-reuse-pr1829]]", "[[decision-reuse-pr1829-as-base]]", "[[fact-pr1829-scope-and-limits]]"]
source_url: "Empty"
---

# Reuse the Working Port, Do Not Re-Derive the Model

**Principle.** A working eager forward for this architecture already exists: vllm-gaudi PR #1829, roughly 2.4k lines in `vllm_gaudi/models/qwen4_exp.py`, covering GDN, QSA, PLE, HyperConnection and the FP8 sparse-MoE stack. The roadmap's P1 goal is explicit — correct eager forward via reuse, not re-derivation. The work is retargeting: move from PR pin `dd3bc9c72faf` to plugin 0.30.0, register the model classes, carry the FP8 MoE block-grid fix, honour `modules_to_not_convert`, drop the `mtp.*` head.

**What this rules out.** Deriving Qwen3.8-Flash-Next from the model config on a new backend. That path burns time on problems the PR already solved — attention state shapes, the QSA indexer wiring, hyperconnection residuals — and re-introduces bugs whose fixes are already written.

**What it forces under time pressure.** When a deadline looms, rewriting a "small" module feels faster than reading someone else's 2.4k lines. The pillar forces the opposite instinct: read the port first, retarget second, and treat any from-scratch component as a scope deviation that must be justified against a specific limitation of the PR, not against impatience.
