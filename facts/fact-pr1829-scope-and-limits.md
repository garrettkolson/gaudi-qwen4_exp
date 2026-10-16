---
id: fact-pr1829-scope-and-limits
title: "PR #1829 Is a Gaudi 3, Eager-Only Qwen4Exp Port"
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: PR #1829 is a Gaudi 3, eager-only Qwen4Exp port (~2.4k lines in qwen4_exp.py): no compiled mode, no vision tower, mtp.* head dropped, pinned to dd3bc9c72faf.
auto_inject: false
applicable_when: "Empty"
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PR #1829's diff is read and shows compiled-mode support, a vision tower, a retained mtp.* head, a line count far from ~2.4k, or a pin other than dd3bc9c72faf, this scope statement is wrong"
tags: ["pr-1829", "vllm-gaudi", "eager-only", "scope", "reuse-base"]
edges: [
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.9, "note": "Scope and limitations are read from PR #1829, the reuse base the roadmap grounds P1 on"},
  {"target": "decision-reuse-pr1829-as-base", "type": "supports", "weight": 0.85, "note": "The known scope/limits are what make reuse-a-base a reasoned choice rather than a fresh build"},
  {"target": "fact-model-architecture-blocks", "type": "related_to", "weight": 0.85, "note": "The port implements the architecture blocks catalogued in the companion architecture fact"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "supports", "weight": 0.9, "note": "P1 retargets this specific PR, so its scope and limits define the starting point"}
]
related: ["[[source-vllm-gaudi-pr1829]]", "[[decision-reuse-pr1829-as-base]]", "[[fact-model-architecture-blocks]]", "[[cust-phase-p1-reuse-pr1829]]"]
source_url: "https://github.com/HabanaAI/vllm-gaudi/pull/1829"
---

# PR #1829 Is a Gaudi 3, Eager-Only Qwen4Exp Port

vllm-gaudi PR #1829 is a Gaudi 3, eager-only port of Qwen4Exp. Its body is roughly 2.4k lines in `vllm_gaudi/models/qwen4_exp.py`. Its limitations are explicit: no compiled-mode (HPU-graph) support, no vision tower for `ForConditionalGeneration`, the `mtp.*` head dropped at load, and a pin to upstream `dd3bc9c72faf`. The roadmap grounds these in `evidence_grounded` ("PR #1829 scope/limitations/failure sites") and in P1.3 ("Retarget from PR pin dd3bc9c72faf ...") and P1.5 ("drop mtp.* head at load"). PR contents are externally checkable, so confidence is high; the PR URL is recorded as `source_url` (path to verify on landing).

The scope matters because P1's job is retargeting this port to Gaudi 2 / plugin 0.30.0, not authoring the model — the reuse-over-re-derivation pillar rests on this artifact existing.

This node states what the PR contains and omits. It does NOT establish that the port runs correctly on Gaudi 2 — the eager smoke-battery reproduction on Gaudi 2 is P1's exit criterion, still open. The PR diff was not dropped into `raw/` for a full conversion (tracked as `bookmark-pr1829-diff`), so the figures are the roadmap's, not a line-by-line read, and `verified_at` is Empty.
