---
id: source-vllm-gaudi-pr1829
title: vllm-gaudi PR #1829 — Qwen4Exp on Gaudi 3
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "vllm-gaudi PR #1829, the eager-only Gaudi 3 Qwen4Exp port (~2.4k lines) the roadmap names as P1's reuse base; known only through the roadmap's account, its diff is not in raw/."
auto_inject: false
applicable_when: "When retargeting the port in P1 or judging which problems PR #1829 has already solved"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the archived diff shows scope, pins or dropped heads different from the roadmap's summary, or the PR is merged or rebased onto plugin 0.30.0, fact-pr1829-scope-and-limits needs rework"
tags: ["vllm-gaudi", "pr-1829", "reuse", "gaudi-3", "eager", "qwen4-exp"]
edges: [
  {"target": "fact-pr1829-scope-and-limits", "type": "supports", "weight": 0.9, "note": "The ~2.4k-line scope, eager-only status, missing vision tower, dropped mtp.* head and dd3bc9c72faf pin are all reported from this PR"},
  {"target": "decision-reuse-pr1829-as-base", "type": "supports", "weight": 0.9, "note": "The decision to retarget rather than re-derive rests on this port existing and working in eager"},
  {"target": "bookmark-pr1829-diff", "type": "followed_by", "weight": 0.7, "note": "The description and diff still need dropping into raw/; until then every claim here is the roadmap's secondhand account"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "supports", "weight": 0.9, "note": "P1 is defined as retargeting this PR to Gaudi 2 and plugin 0.30.0, not authoring a new model"}
]
related: ["[[fact-pr1829-scope-and-limits]]", "[[cust-phase-p1-reuse-pr1829]]", "[[decision-reuse-pr1829-as-base]]", "[[bookmark-pr1829-diff]]"]
source_url: "Empty"
---
# vllm-gaudi PR #1829 — Qwen4Exp on Gaudi 3

The reference port the roadmap names as the reuse base: vllm-gaudi pull request #1829, a Qwen4Exp implementation for Gaudi 3 that runs eager-only. The roadmap records its scope and limits — roughly 2.4k lines in `vllm_gaudi/models/qwen4_exp.py`, GDN via `HPUGatedDeltaNetAttention` (48 value heads / 16 QK heads / 128 head dim), QSA indexer plus attention, PLE norm and n-gram embedding, `HpuGatedResidual`, no compiled-mode support, no vision tower, the `mtp.*` head dropped at load, pinned to `dd3bc9c72faf`, and built against Gaudi 3's 128 GB / 3.7 TB/s part.

It grounds `cust-phase-p1-reuse-pr1829`, `fact-pr1829-scope-and-limits`, `fact-model-architecture-blocks` and `decision-reuse-pr1829-as-base`. Only the roadmap's summary is in this vault: no PR description or diff has been dropped into `raw/`, so every detail is secondhand and tracked by `bookmark-pr1829-diff`. The roadmap gives no URL for the PR, so none is recorded here; PR number and pin hash are the handles to re-check on landing.
