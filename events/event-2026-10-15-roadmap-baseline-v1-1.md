---
id: event-2026-10-15-roadmap-baseline-v1-1
title: Roadmap v1.1 Adopted as Baseline
type: event
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "2026-10-15: roadmap v1.1 (schema 1.1) frozen as baseline in raw/processed; target stack, phase order, P0 gating and the provenance split become the project's plan of record."
auto_inject: false
applicable_when: "When deciding which roadmap version a claim belongs to, or when a change to the plan needs a newer baseline event to justify it"
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a roadmap newer than v1.1 is copied into raw/processed/, this baseline is superseded and phases, risks and provenance labels must be re-adopted before further work"
tags: ["event", "baseline", "roadmap", "v1-1", "plan-of-record"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "The event is the adoption of this file version; the immutable copy is its physical record"},
  {"target": "event-2026-10-15-vault-seed-build", "type": "followed_by", "weight": 0.9, "note": "The seed conversion runs against the frozen baseline, same day, after adoption"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.7, "note": "Adoption makes P0's gating status binding: no later phase proceeds without its exit criteria"}
]
related: ["[[source-roadmap-qwen4-exp-gaudi2-v1-1]]", "[[event-2026-10-15-vault-seed-build]]", "[[cust-phase-p0-platform-gate]]"]
source_url: "Empty"
---
# Roadmap v1.1 Adopted as Baseline

On 2026-10-15 the roadmap *Qwen3.8-Flash-Next (qwen4_exp) serving on Gaudi 2 via vllm-gaudi*, schema version 1.1, was frozen as the project baseline and written to `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json`. The working copy `qwen4_exp_gaudi2_roadmap.json` remains at the repository root under human ownership; the vault reads the frozen copy and edits neither.

What this makes true: the target stack (suite 1.24.2, PyTorch 2.13, plugin 0.30.0, upstream vLLM pinned at/after `c05d75a`, 4x Gaudi 2) is the fixed reference point; the execution order P0 → P1 → P4_pin_check → P3 → P4_capture → P5, with P2 branching off P1 and P6 deferred, is the plan of record; P0 is declared gating; and each claim carries the roadmap's own label — `evidence_grounded` or `author_inference_flagged` — which sets the confidence ceiling for everything derived from it.

What it triggers next: conversion of the baseline into typed nodes, then P0 measurements, the only events that can lift confidence above the inference ceiling.
