---
id: concept-mtp-speculative-decoding
title: MTP Multi-Token-Prediction Speculative Decoding
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Extra heads draft k tokens verified in one pass. The checkpoint's mtp.* head is dropped because no HPU drafter exists, so the lever is deferred rather than rejected.
auto_inject: false
applicable_when: When evaluating decode-throughput levers, or deciding whether to rebuild the dropped mtp.* head against the HPU runner
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If an HPU MTP drafter lands in hpu_model_runner.py and is measured against the low-batch MoE baseline, this node's deferred framing is replaced by measured acceptance-rate and draft-cost numbers"
tags: ["mtp", "speculative-decoding", "decode-throughput", "drafter", "deferred-feature"]
edges: [
  {"target": "task-p6-1-hpu-mtp-drafter", "type": "related_to", "weight": 0.9, "note": "That deferred task is the only route to using the head: a drafter in the HPU runner, or an explicit acceptance of the dropped weights"},
  {"target": "task-p1-5-honor-not-convert-drop-mtp", "type": "related_to", "weight": 0.85, "note": "P1.5 drops mtp.* at load, which is what makes the head inert until a drafter exists"},
  {"target": "question-mtp-drafter-on-hpu", "type": "related_to", "weight": 0.9, "note": "That question holds the open decision this node cannot close without measured acceptance and draft cost"},
  {"target": "ref-vllm-gaudi-plugin", "type": "related_to", "weight": 0.7, "note": "The plugin's runner ships ngram, eagle and medusa drafters only, which is the constraint that forces the drop"}
]
related: ["[[task-p6-1-hpu-mtp-drafter]]", "[[question-mtp-drafter-on-hpu]]", "[[task-p1-5-honor-not-convert-drop-mtp]]", "[[ref-vllm-gaudi-plugin]]"]
source_url: "Empty"
---

# MTP Multi-Token-Prediction Speculative Decoding

Multi-token prediction attaches extra head or heads to the model that predict several future tokens from the current hidden state. Serving uses them as a drafter: the head proposes k tokens, the target model scores all k positions in a single forward pass, and the longest accepted prefix is committed — one verification step buying several committed tokens. Acceptance is probabilistic, so the benefit is an average, and the cost is the drafter's own forward work plus a wider verification slot, both charged to the same engine.

In this project the checkpoint carries an `mtp.*` head that PR #1829 drops at load, and the vllm-gaudi runner supports only ngram, eagle and medusa drafters — there is no HPU MTP drafter. P1.5 therefore drops the head while honouring `modules_to_not_convert`, and building one is a deferred P6 item rather than enablement work.

The failure mode the deferral avoids is paying for a speculative path that does not pay for itself. Decode here is already dominated by the low-batch MoE slowness of issue #1733, so speculative decoding must beat that baseline rather than beat eager in the abstract: draft cost, the choice of k, and per-step verification overhead all consume the constrained matrix-engine time, and without a measured acceptance rate the net effect is a guess rather than a curve. Whether an HPU MTP drafter earns back its cost against the dropped head is tracked as an open question, and P6 is product-driven.
