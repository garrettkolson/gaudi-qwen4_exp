---
id: concept-ple-dilated-conv-ngram
title: PLE Dilated Short-Conv and N-gram Embedding State
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Short dilated causal conv plus an n-gram table lookup; cheap math whose per-request state and data-dependent pooling break capture and escape memory accounting.
auto_inject: false
applicable_when: When writing the PLE conv or FP8 n-gram kernels, or moving PLE and n-gram state onto scheduler-owned blocks
confidence: 0.75
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P3.2 or P3.3 shows the conv pooling expressible with fixed output widths, the .nonzero capture failure mode and any eager fallback reserved for PLE stop applying"
tags: ["ple", "dilated-conv", "n-gram", "fp8", "state-cache", "graph-capture"]
edges: [
  {"target": "fact-model-architecture-blocks", "type": "related_to", "weight": 0.9, "note": "Names the two classes this node explains, HpuQwen4ExpPLENorm and HpuQwen4ExpNGramEmbedding, as ported blocks"},
  {"target": "task-p3-2-ple-dilated-conv-kernel", "type": "related_to", "weight": 0.9, "note": "The fused target for the dilated short-conv described here; byte-equality to eager is the exit condition"},
  {"target": "task-p3-3-fp8-ngram-gather-kernel", "type": "related_to", "weight": 0.9, "note": "The gather-then-dequant kernel for the n-gram table; this node states why the table stays FP8 rather than INT8"},
  {"target": "task-p4-4-eliminate-host-coercing-ops", "type": "related_to", "weight": 0.85, "note": "Its target list names PLE _pool_and_store .nonzero and _expand_plan torch.minimum, the ops this node explains as value-dependent"},
  {"target": "concept-kv-block-ownership", "type": "related_to", "weight": 0.8, "note": "Conv taps and trailing-token history are per-sequence buffers, so they are part of the unaccounted state P2.1 migrates"}
]
related: ["[[fact-model-architecture-blocks]]", "[[task-p3-3-fp8-ngram-gather-kernel]]", "[[concept-kv-block-ownership]]", "[[task-p4-4-eliminate-host-coercing-ops]]"]
source_url: "Empty"
---

# PLE Dilated Short-Conv and N-gram Embedding State

Per-layer embedding adds cheap token-level mixing to the transformer block: a short depthwise causal convolution with dilation, where each output taps a small window spread across several positions, combined with an n-gram embedding — a lookup over the trailing token history that gives the block an explicit short-range feature. Both are elementwise-scale operations, but each needs per-sequence state: conv taps spanning the last positions, and the token history feeding the gather.

In the Gaudi 2 port these two small pieces account for three tasks. P3 authorises one fused TPC CustomOp for the dilated short-conv and one for the n-gram gather-then-dequant, where the n-gram table is gathered in FP8 and dequantised on the compute path — it stays FP8 on the Gaudi 2 matrix engine, with no INT8 re-expression. The conv state and the trailing-token history are among the buffers P2.1 moves onto scheduler-owned blocks, since both are per-request and both were sized for a card with more memory.

The failure mode is capture and memory, not arithmetic. PLE's `_pool_and_store` uses `.nonzero`, whose output length depends on the data, so it is host-coercing and ends a graph recording; `_expand_plan`'s `torch.minimum` on tensor values has the same character. And per-state-slot conv and history tensors allocated inside the module grow with concurrency outside the scheduler's accounting on a 96 GB card.
