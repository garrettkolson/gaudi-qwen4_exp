---
id: task-p1-5-honor-not-convert-drop-mtp
title: "Honour modules_to_not_convert and Drop the mtp.* Head"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Respect the checkpoint's modules_to_not_convert list at load time and drop the mtp.* speculative head, which has no HPU drafter in this phase."
auto_inject: false
applicable_when: "P1, at load-path work; must be settled before output quality is judged, since an unconverted module changes numerics"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P6 implements an HPU MTP drafter, dropping the mtp.* head is no longer correct and this load-path behaviour must be reversed"
tags: ["roadmap-task", "p1", "fp8", "quantization", "load-path"]
edges: [
  {"target": "cust-phase-p1-reuse-pr1829", "type": "part_of", "weight": 0.9, "note": "A load-path correctness item inside the reuse-and-retarget phase"},
  {"target": "concept-mtp-speculative-decoding", "type": "related_to", "weight": 0.85, "note": "The dropped head is the MTP draft head; dropping it forfeits speculative decoding for now"},
  {"target": "question-mtp-drafter-on-hpu", "type": "related_to", "weight": 0.7, "note": "Dropping the head is the cheap branch of this open question"},
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "depends_on", "weight": 0.7, "note": "Which modules stay unconverted depends on what the card can actually execute in FP8"}
]
related: ["[[cust-phase-p1-reuse-pr1829]]", "[[concept-mtp-speculative-decoding]]"]
source_url: "Empty"
---

# Honour modules_to_not_convert and Drop the mtp.* Head

At load time, respect the checkpoint's `modules_to_not_convert` list rather than quantizing everything indiscriminately, and drop the `mtp.*` head.

The first half is a numerics question. A checkpoint's quantization recipe excludes specific modules precisely because quantizing them degrades quality — typically norms, embeddings or small projection layers where precision loss is disproportionate to the memory saved. Ignoring that list in the load path produces a model that runs fast and is quietly worse, and the degradation will be attributed to whatever else was being changed at the time.

The second half is a scope decision with a real cost. The `mtp.*` head drives multi-token-prediction speculative decoding, and only ngram, eagle and medusa drafters exist in the HPU model runner today. Dropping the head makes the load path clean and the model self-consistent, at the price of forfeiting that decoding path until P6 decides whether an HPU MTP drafter earns back its cost. Drop it at load rather than leaving it loaded and unused: an unrunnable head is a source of confusing shape errors and wasted memory.

Done when: excluded modules load unconverted as the checkpoint specifies, the `mtp.*` head is absent from the served model, and load logs show both decisions explicitly.
