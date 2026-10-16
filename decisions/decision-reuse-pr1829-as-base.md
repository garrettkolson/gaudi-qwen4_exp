---
id: decision-reuse-pr1829-as-base
title: Base the Port on vllm-gaudi PR #1829 Rather Than a Fresh Implementation
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Base the Gaudi 2 port on vllm-gaudi PR #1829's qwen4_exp.py (~2.4k lines) and retarget it to plugin 0.30.0, rather than a fresh implementation or upstreaming to core vLLM first.
auto_inject: false
applicable_when: When starting P1 port work, or when a component rewrite is proposed that the PR already implements
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PR #1829's port fails to boot on plugin 0.30.0 for reasons unfixable within P1's scope, the reuse base fails and the fresh-implementation alternative must be reopened"
tags: ["decision", "pr-1829", "reuse", "port-strategy", "p1"]
edges: [
  {"target": "pillar-reuse-over-rederivation", "type": "supports", "weight": 0.95, "note": "The pillar supplies the standing rationale; this decision is its one-time application to the port's base"},
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.9, "note": "The decision is made about this specific source: its scope, ~2.4k lines, and eager-only limits"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "related_to", "weight": 0.9, "note": "P1 is the phase that executes this decision end to end"},
  {"target": "fact-pr1829-scope-and-limits", "type": "depends_on", "weight": 0.85, "note": "The choice is only rational given the fact: what the PR does cover and what it excludes (vision tower, mtp.* head, compiled mode)"}
]
related: ["[[pillar-reuse-over-rederivation]]", "[[cust-phase-p1-reuse-pr1829]]", "[[fact-pr1829-scope-and-limits]]", "[[task-p1-3-retarget-pin-to-0-30-0]]"]
source_url: "Empty"
---

# Base the Port on vllm-gaudi PR #1829 Rather Than a Fresh Implementation

## Context

Qwen3.8-Flash-Next (qwen4_exp) combines GDN linear attention (48 value heads / 16 QK heads / 128 head dim), a QSA indexer with sparse attention, PLE norm plus n-gram embedding, gated-residual HyperConnection, and an FP8 sparse-MoE stack. vllm-gaudi PR #1829 already implements all of these in eager mode for Gaudi 3 — roughly 2.4k lines in `vllm_gaudi/models/qwen4_exp.py` — with a passing smoke battery. The target hardware is different: 4x Gaudi 2, plugin 0.30.0.

## Alternatives considered

A fresh implementation from the model config, re-deriving every block against the plugin API. Upstreaming to core vLLM first, then adapting, which puts an external review dependency in front of the enablement milestone.

## Decision

Base the port on `vllm_gaudi/models/qwen4_exp.py`. Retarget the pin from `dd3bc9c72faf` to plugin 0.30.0 (satisfying `c05d75a`+), register `Qwen4ExpForCausalLM` and `Qwen4ExpForConditionalGeneration`, carry the FP8 MoE block-grid fix from `extension/ops.py`, honour `modules_to_not_convert`, and drop the `mtp.*` head at load.

## Consequence

P1's scope becomes retargeting plus reproducing the smoke battery (arithmetic, geography, code, needle retrieval) on Gaudi 2, not authoring a model. Known PR limits — no compiled mode, no vision tower, dropped MTP head — become tracked gaps (P4, P6) rather than surprises discovered mid-port.
