---
id: cust-phase-p6-feature-parity
title: "P6 — Feature Parity (Deferred, Product-Driven)"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Deferred, product-driven work beyond text-only serving: an HPU MTP drafter or accepting the dropped head, the vision tower, and re-enabled prefix caching."
auto_inject: false
applicable_when: "When a product decision requests MTP, multimodal, or prefix caching after text-only serving is enabled"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a product decision makes MTP, vision, or prefix caching mandatory before text-only serving lands, this phase stops being deferrable and must be re-planned"
tags: ["roadmap-phase", "p6", "feature-parity", "deferred", "mtp", "vision"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P6 — deferred flag, three tasks, per-feature exit criteria"},
  {"target": "cust-phase-p5-moe-economics", "type": "depends_on", "weight": 0.8, "note": "Feature parity is only worth spending on after text-only serving economics are proven"},
  {"target": "decision-defer-feature-parity-p6", "type": "supports", "weight": 0.9, "note": "The deferral decision — P6 is product-driven, not required for enablement"},
  {"target": "concept-mtp-speculative-decoding", "type": "depends_on", "weight": 0.8, "note": "The MTP drafter task presumes the speculative-decoding concept and the dropped mtp.* head"},
  {"target": "question-mtp-drafter-on-hpu", "type": "related_to", "weight": 0.85, "note": "Whether an HPU MTP drafter pays for itself is open; only ngram/eagle/medusa exist today"},
  {"target": "task-p6-3-enable-prefix-caching", "type": "related_to", "weight": 0.8, "note": "Prefix caching re-enables here but is gated on the P2.1 block migration having landed"}
]
related: ["[[decision-defer-feature-parity-p6]]", "[[question-mtp-drafter-on-hpu]]", "[[concept-mtp-speculative-decoding]]", "[[task-p6-3-enable-prefix-caching]]"]
source_url: "Empty"
---

# P6 — Feature Parity (Deferred, Product-Driven)

## Goal
Optional capabilities beyond text-only language serving, pulled only when product asks: an HPU MTP drafter in hpu_model_runner.py — only ngram, eagle and medusa drafters exist today — or accepting the dropped `mtp.*` head; the vision stack for `ForConditionalGeneration` if multimodal is required (PR #1829 excluded the vision tower); and re-enabling prefix caching with regression coverage after the P2.1 block migration.

## Depends on
P5 (text-only serving economics proven first). Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5 — the cheap pin check precedes heavy kernel authoring — and P6 trails that chain, deferred by decision.

## Tasks
- [[task-p6-1-hpu-mtp-drafter]] — implement an HPU MTP drafter, or formally accept the dropped mtp.* head.
- [[task-p6-2-vision-tower]] — build the vision stack for conditional generation if multimodal is required.
- [[task-p6-3-enable-prefix-caching]] — re-enable prefix caching with regression coverage, gated on P2.1.

## Exit criteria
Per-feature criteria; none of this is required for text-only serving enablement.
