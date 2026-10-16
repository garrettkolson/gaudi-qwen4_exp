---
id: task-p6-1-hpu-mtp-drafter
title: Implement an HPU MTP Drafter (or Accept the Dropped Head)
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Deferred, not required for text-only serving. Implement an HPU MTP drafter in hpu_model_runner.py — only ngram/eagle/medusa exist — or formally accept the dropped mtp.* head.
auto_inject: false
applicable_when: P6 (cust-phase-p6-feature-parity) — deferred and product-driven; live only if the product requires MTP speculative decoding on top of completed text-only serving.
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If vllm-gaudi gains an HPU MTP drafter upstream, or the product formally rejects speculative decoding, the implement branch of this task is obsolete and only the accept-the-head decision remains."
tags: ["roadmap-task", "p6", "deferred", "mtp", "speculative-decoding"]
edges: [
  {"target": "cust-phase-p6-feature-parity", "type": "part_of", "weight": 0.9, "note": "P6 task, explicitly deferred and not part of text-only serving enablement"},
  {"target": "concept-mtp-speculative-decoding", "type": "depends_on", "weight": 0.9, "note": "The drafter implements the MTP draft/verify pattern this concept defines"},
  {"target": "question-mtp-drafter-on-hpu", "type": "related_to", "weight": 0.9, "note": "Whether an HPU drafter pays for itself against the dropped head is the open question gating this task"},
  {"target": "task-p1-5-honor-not-convert-drop-mtp", "type": "preceded_by", "weight": 0.8, "note": "P1.5 already drops the mtp.* head at load; this task decides whether to bring that capability back"}
]
related: ["[[cust-phase-p6-feature-parity]]", "[[question-mtp-drafter-on-hpu]]", "[[concept-mtp-speculative-decoding]]", "[[decision-defer-feature-parity-p6]]"]
source_url: "Empty"
---
# Implement an HPU MTP Drafter (or Accept the Dropped Head)

Deferred — not required for text-only serving. Either implement MTP speculative decoding via an HPU drafter in hpu_model_runner.py, where only ngram, eagle, and medusa drafters exist today, or formally accept the dropped mtp.* head from P1.5 and serve without MTP. The choice is product-driven: a drafter buys decode-side speed but adds new kernel surface on Gaudi 2, and the open question of whether it pays for itself is unresolved.

Done when: the per-feature criterion is met — the drafter drafts and verifies correctly, or accepting the dropped head is the recorded decision; text-only serving enablement does not wait for this.
