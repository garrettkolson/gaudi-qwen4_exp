---
id: source-vllm-gaudi-release-notes
title: vllm-gaudi Release Notes v0.24.0 → v0.30.0
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "vllm-gaudi release lineage v0.24.0 through v0.30.0: TPC-native causal_conv1d, FP8/INC stability, gathered-expert MoE combine, clamped decode buckets. Grounds what the pinned plugin ships."
auto_inject: false
applicable_when: "When relying on a plugin 0.30.0 feature in P2.3 or P5.1, or when a version bump might make a feature default rather than opt-in"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If plugin 0.30.0 release notes do not list the gathered-expert MoE combine or clamped decode buckets, or a later release changes their defaults, fact-plugin-0-30-0-features and P5.1 need re-reading"
tags: ["vllm-gaudi", "release-notes", "plugin-0-30-0", "fp8", "moe", "causal-conv1d"]
edges: [
  {"target": "fact-plugin-0-30-0-features", "type": "supports", "weight": 0.9, "note": "The feature list attributed to v0.30.0 and the v0.24.0-onward stability line come from this release lineage"},
  {"target": "ref-vllm-gaudi-plugin", "type": "related_to", "weight": 0.85, "note": "The plugin reference node is the object these notes version"},
  {"target": "cust-phase-p5-moe-economics", "type": "supports", "weight": 0.7, "note": "P5's first lever, gathered-expert MoE combine, exists only because the release notes say the plugin ships it opt-in"}
]
related: ["[[fact-plugin-0-30-0-features]]", "[[ref-vllm-gaudi-plugin]]", "[[task-p5-1-gathered-expert-moe-combine]]", "[[task-p2-3-verify-decode-bucket-clamp]]"]
source_url: "Empty"
---
# vllm-gaudi Release Notes v0.24.0 → v0.30.0

The plugin release lineage the roadmap lists in `evidence_grounded` as "Plugin v0.24.0/v0.30.0 release notes". Three things in the plan depend on it: TPC-native `causal_conv1d`, FP8/INC quantization stability work from v0.24.0 onward, and the opt-in gathered-expert MoE combine plus decode block buckets clamped to physical KV cache size in v0.30.0.

It is the grounding for `fact-plugin-0-30-0-features`, which in turn supports `task-p5-1-gathered-expert-moe-combine` — the roadmap's main lever against issue #1733 low-batch MoE slowness — and `task-p2-3-verify-decode-bucket-clamp`, a check that a claimed v0.30.0 behaviour is actually active.

Currency caveat: the roadmap summarises the notes; the notes themselves are not in `raw/`, so "opt-in" versus "default" and the exact release a feature landed in are asserted, not read. The roadmap gives no URL, so none is recorded; re-check the release page and the plugin source at the 0.30.0 pin before treating a feature as available.
