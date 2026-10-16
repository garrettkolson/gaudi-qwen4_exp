---
id: question-mtp-drafter-on-hpu
title: Is an HPU MTP Drafter Worth Building Against the Dropped Head?
type: question
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: The port drops the mtp.* head and only ngram/eagle/medusa drafters exist on HPU; whether a custom MTP drafter earns back its cost on Gaudi 2 is unmeasured.
auto_inject: false
applicable_when: When P6 is taken up, or if a measured P5 curve shows decode latency as the binding constraint
confidence: 0.4
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "Once a measured P5 decode-cost baseline is compared against draft-plus-verify overhead and the mtp head's acceptance rate, this question is answered"
tags: ["mtp", "speculative-decoding", "hpu", "feature-parity", "open-question"]
edges: [
  {"target": "task-p6-1-hpu-mtp-drafter", "type": "related_to", "weight": 0.9, "note": "P6.1 is the build-or-accept choice this question decides"},
  {"target": "concept-mtp-speculative-decoding", "type": "depends_on", "weight": 0.85, "note": "The mechanism: draft tokens from the model's own MTP head, verify them against the target model"},
  {"target": "cust-phase-p6-feature-parity", "type": "related_to", "weight": 0.85, "note": "P6 is deferred and product-driven, so this stays open without blocking text-only serving"}
]
related: ["[[task-p1-5-honor-not-convert-drop-mtp]]", "[[decision-defer-feature-parity-p6]]", "[[question-moe-saturation-point]]"]
source_url: "Empty"
---

# Is an HPU MTP Drafter Worth Building Against the Dropped Head?

## The question

The port drops the `mtp.*` head at load and the plugin ships only ngram, eagle and medusa drafters. Does writing an MTP drafter in `hpu_model_runner.py` — one that restores the head the model was trained with — earn back its cost in Gaudi 2 decode throughput?

## Why it blocks the plan

It does not block text-only serving, which is why P6 is deferred. But it bounds what P5's curve can later be improved by, and the trade is hardware-shaped: on a 96GB card already carrying HBM pressure from the side caches, the MTP head's weights plus the verification pass compete for the same memory P2 is rationing, and speculative decoding only pays when drafts are accepted often enough to beat the extra work. Accepting the dropped head is a real option, not a failure state.

## What answers it

A measured P5 cost-per-token baseline plus a cost model for speculative decoding on this box: acceptance rate and tokens per step from the model's own `mtp.*` head, against draft-generation and verification overhead on HPU. `task-p6-1-hpu-mtp-drafter` stays unbuilt until that comparison shows a win over the existing drafters.
