---
id: decision-defer-feature-parity-p6
title: Defer MTP, Vision, and Prefix Caching Behind Text-Only Serving
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: MTP drafter, vision tower, and prefix-caching re-enablement are deferred to P6: product-driven features, not required for text-only serving enablement on 4x Gaudi 2.
auto_inject: false
applicable_when: When a multimodal, speculative-decoding, or cache-hit feature is proposed while text-only serving is not yet done
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the product requires multimodal input or speculative-decode latency before text-only serving completes, deferral of that specific item stops being tenable"
tags: ["decision", "scope", "feature-parity", "deferral", "p6"]
edges: [
  {"target": "cust-phase-p6-feature-parity", "type": "related_to", "weight": 0.9, "note": "P6 is the roadmap's deferral container: deferred flag set, exit criteria per-feature and not required for enablement"},
  {"target": "task-p6-1-hpu-mtp-drafter", "type": "related_to", "weight": 0.8, "note": "Deferred item one: build an HPU MTP drafter (only ngram/eagle/medusa exist today) or accept the dropped mtp.* head"},
  {"target": "task-p6-2-vision-tower", "type": "related_to", "weight": 0.8, "note": "Deferred item two: the ForConditionalGeneration vision stack, which PR #1829 excluded from its port"},
  {"target": "task-p6-3-enable-prefix-caching", "type": "related_to", "weight": 0.8, "note": "Deferred item three: re-enable prefix caching with regression coverage, but only after P2.1 lands"}
]
related: ["[[cust-phase-p6-feature-parity]]", "[[task-p6-1-hpu-mtp-drafter]]", "[[task-p6-3-enable-prefix-caching]]", "[[concept-mtp-speculative-decoding]]"]
source_url: "Empty"
---

# Defer MTP, Vision, and Prefix Caching Behind Text-Only Serving

## Context

The roadmap's goal is text-only serving of Qwen3.8-Flash-Next on 4x Gaudi 2, ending in a documented cost-per-token curve (P5). Three capabilities sit outside that goal: MTP speculative decoding (the port drops the `mtp.*` head, and HPU has only ngram/eagle/medusa drafters today), the vision tower for `ForConditionalGeneration` (excluded from PR #1829 entirely), and prefix caching re-enablement (blocked on P2.1 block-managed side caches). Each is substantial engineering with no bearing on whether text-only serving works.

## Alternatives considered

Pull the MTP drafter forward for decode speed before the MoE economics are even measured. Port the vision stack for multimodal parity "while we are in there". Re-enable prefix caching without the P2.1 plumbing or regression coverage.

## Decision

Defer all three to P6, marked product-driven and not required for enablement. P6's exit criteria are per-feature, so each item is pulled forward only by an explicit product requirement, never by opportunism.

## Consequence

Roadmap completion means: eager correctness, cache plumbing stability at concurrency 8+, capture-mode serving, and a cost-per-token curve — with text-only scope stated. P6 items stay scheduled with named tasks, so the deferral is visible and reversible rather than a silent deletion of requirements.
