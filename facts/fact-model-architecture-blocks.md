---
id: fact-model-architecture-blocks
title: "Qwen3.8-Flash-Next Composition: GDN, QSA, PLE, HyperConnection, MoE"
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Qwen3.8-Flash-Next: GDN (48V/16QK/128), QSA indexer+attention, PLE norm + n-gram embedding, gated-residual HyperConnection, FP8 sparse MoE, plus a dropped mtp.* head.
auto_inject: false
applicable_when: "Empty"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the model config or PR #1829's qwen4_exp.py shows GDN head counts or head dim other than 48 value / 16 QK / 128, or a different block set, this composition is wrong"
tags: ["model-architecture", "gdn", "qsa", "ple", "hyperconnection", "moe"]
edges: [
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.85, "note": "The block set and head dimensions are read from PR #1829's qwen4_exp.py as the roadmap records them"},
  {"target": "concept-gdn-gated-delta-net", "type": "related_to", "weight": 0.9, "note": "GDN is the linear-attention block, detailed in its concept node"},
  {"target": "concept-qsa-indexer", "type": "related_to", "weight": 0.9, "note": "The QSA indexer + attention block is detailed in its concept node"},
  {"target": "concept-ple-dilated-conv-ngram", "type": "related_to", "weight": 0.9, "note": "PLE norm + n-gram embedding state is detailed in its concept node"},
  {"target": "concept-hyperconnection-gated-residual", "type": "related_to", "weight": 0.85, "note": "The gated-residual HyperConnection (HpuGatedResidual) is detailed in its concept node"}
]
related: ["[[concept-gdn-gated-delta-net]]", "[[concept-qsa-indexer]]", "[[concept-ple-dilated-conv-ngram]]", "[[concept-hyperconnection-gated-residual]]"]
source_url: "https://github.com/HabanaAI/vllm-gaudi/pull/1829"
---

# Qwen3.8-Flash-Next Composition: GDN, QSA, PLE, HyperConnection, MoE

Qwen3.8-Flash-Next (qwen4_exp) is composed of five block families plus a dropped head. GDN (Gated DeltaNet) linear attention with 48 value heads, 16 QK heads, and 128 head dim, reusing `HPUGatedDeltaNetAttention`. QSA: `HpuQSAIndexer` plus `HpuQwen4ExpQSAAttention`. PLE: `HpuQwen4ExpPLENorm` plus `HpuQwen4ExpNGramEmbedding`. HyperConnection: gated-residual `HpuGatedResidual`. Plus an FP8 sparse MoE and an `mtp.*` head that PR #1829 drops at load. The roadmap records these in P1.1 and P1.5, grounded in `evidence_grounded` ("PR #1829 scope/limitations/failure sites"). As PR/model-config contents they are externally checkable, so confidence sits at the lower bound of the checkable band because the line-level detail is the roadmap's reading of the port rather than a fresh config parse.

This catalogue is the inventory P1.1 ports and the per-block concept nodes expand.

This node states the block composition and the head dimensions the roadmap names. It does NOT establish correct forward numerics on Gaudi 2, nor the runtime cost of any block — those are P1/P3 outcomes. The `mtp.*` head is described, not implemented: the port drops it. Nothing is measured, so `verified_at` is Empty.
