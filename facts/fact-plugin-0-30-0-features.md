---
id: fact-plugin-0-30-0-features
title: Plugin v0.30.0 Ships Gathered-Expert MoE Combine and Clamped Decode Buckets
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: vllm-gaudi plugin v0.30.0 ships opt-in gathered-expert MoE combine for FP8 and decode block buckets clamped to physical KV; lineage from v0.24.0 added TPC-native causal_conv1d and FP8/INC stability.
auto_inject: false
applicable_when: "Empty"
confidence: 0.88
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the v0.30.0 release notes do not actually list gathered-expert MoE combine or clamped decode buckets, or a later plugin release removes or renames either feature, this statement is outdated"
tags: ["vllm-gaudi", "plugin-0-30-0", "moe", "release-notes", "decode-buckets"]
edges: [
  {"target": "source-vllm-gaudi-release-notes", "type": "derived_from", "weight": 0.85, "note": "The features are read from the v0.24.0 through v0.30.0 release notes"},
  {"target": "task-p5-1-gathered-expert-moe-combine", "type": "supports", "weight": 0.9, "note": "P5.1 applies the opt-in gathered-expert MoE combine because v0.30.0 ships it"},
  {"target": "task-p2-3-verify-decode-bucket-clamp", "type": "supports", "weight": 0.9, "note": "P2.3 confirms the clamped decode-bucket behaviour because v0.30.0 introduced it"},
  {"target": "ref-vllm-gaudi-plugin", "type": "related_to", "weight": 0.85, "note": "These are features of the vllm-gaudi plugin the target stack pins to"}
]
related: ["[[ref-vllm-gaudi-plugin]]", "[[task-p5-1-gathered-expert-moe-combine]]", "[[task-p2-3-verify-decode-bucket-clamp]]"]
source_url: "Empty"
---

# Plugin v0.30.0 Ships Gathered-Expert MoE Combine and Clamped Decode Buckets

vllm-gaudi plugin v0.30.0 ships two features this roadmap relies on: an opt-in gathered-expert MoE combine for FP8 (in the spirit of the Qwen3.5/3.6 MoE work, per P5.1), and decode block buckets clamped to the physical KV cache size (per P2.3). The release lineage from v0.24.0 onward also brought TPC-native `causal_conv1d` and FP8/INC stability. The roadmap lists these under `evidence_grounded` ("Plugin v0.24.0/v0.30.0 release notes (TPC-native causal_conv1d; FP8/INC stability; gathered-expert MoE combine)"), and release notes are externally checkable, so confidence is high.

These facts are the mechanical basis for two tasks: P5.1 turns on the gathered-expert combine as a throughput lever against the #1733 low-batch MoE slowness, and P2.3 verifies the clamped decode-bucket behaviour is active.

The node states what the release notes say the plugin contains. It does NOT assert the gathered-expert combine is enabled by default (the roadmap calls it opt-in), nor that it actually improves throughput on Gaudi 2 — that is P5's measurement. The plugin release notes themselves were not dropped into `raw/` for a full conversion, so this is asserted from the roadmap's evidence list, not a verified read, and `verified_at` is Empty.
