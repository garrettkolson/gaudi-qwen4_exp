---
id: task-p1-1-port-qwen4-exp-model
title: "Base the Port on qwen4_exp.py"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Take vllm_gaudi/models/qwen4_exp.py from PR #1829 (~2.4k lines) as the base: GDN, QSA, PLE and HyperConnection components already have HPU implementations to retarget."
auto_inject: false
applicable_when: "P1, once P0 has confirmed FP8 loads and a memory configuration fits"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If plugin 0.30.0 changed the interfaces these components subclass or call, the file will not retarget cleanly and the divergences must be enumerated before continuing"
tags: ["roadmap-task", "p1", "model-port", "reuse", "gaudi-2"]
edges: [
  {"target": "cust-phase-p1-reuse-pr1829", "type": "part_of", "weight": 0.9, "note": "The first and largest P1 task; the rest of the phase hangs off this file"},
  {"target": "fact-model-architecture-blocks", "type": "depends_on", "weight": 0.9, "note": "The component inventory (GDN 48V/16QK/128, QSA, PLE, HyperConnection) is what the file must implement"},
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.9, "note": "The port source is PR #1829, written for Gaudi 3 and eager-only"},
  {"target": "concept-gdn-gated-delta-net", "type": "related_to", "weight": 0.85, "note": "GDN reuses HPUGatedDeltaNetAttention with 48 value heads, 16 QK heads and head dim 128"},
  {"target": "concept-qsa-indexer", "type": "related_to", "weight": 0.85, "note": "QSA reuses HpuQSAIndexer and HpuQwen4ExpQSAAttention"}
]
related: ["[[cust-phase-p1-reuse-pr1829]]", "[[fact-model-architecture-blocks]]"]
source_url: "Empty"
---

# Base the Port on qwen4_exp.py

Start from `vllm_gaudi/models/qwen4_exp.py` from PR #1829, roughly 2.4k lines, rather than writing a fresh model implementation. The file already wires the hard components to HPU implementations: GDN via `HPUGatedDeltaNetAttention` (48 value heads, 16 QK heads, 128 head dim), QSA via `HpuQSAIndexer` and `HpuQwen4ExpQSAAttention`, PLE via `HpuQwen4ExpPLENorm` and `HpuQwen4ExpNGramEmbedding`, and HyperConnection via `HpuGatedResidual`.

Why it matters: the expensive part of this port is not the model wiring, it is the per-primitive behaviour on HPU. That work is already done once, in a file that runs. Re-deriving it would re-open solved questions — state layout, cache shapes, dtype handling — while producing nothing new.

Retargeting means reading each component against plugin 0.30.0's interfaces and deciding, per component, whether the Gaudi 3 code path applies unchanged or needs adjustment for Gaudi 2. Record the divergences as you find them: they are the real content of P1, and they tell P3 which primitives still fall back to eager.

Done when: the model file loads and constructs on Gaudi 2 with the four component families mapped to their HPU implementations, with any interface divergence from the PR pin listed.
