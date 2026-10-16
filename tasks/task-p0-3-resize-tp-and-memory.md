---
id: task-p0-3-resize-tp-and-memory
title: "Re-derive TP Degree, Max-Model-Len and Memory Utilization"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Recompute tensor-parallel degree, max model length and GPU memory utilization for Gaudi 2's 96GB/2.45TB/s instead of inheriting the Gaudi 3 reference values."
auto_inject: false
applicable_when: "P0, after the FP8 load succeeds and weights footprint is known; before any concurrency or throughput claim is made"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the side-cache migration in P2.1 changes how much memory the KV and side caches consume, these numbers must be re-derived rather than reused"
tags: ["roadmap-task", "p0", "memory-planning", "tensor-parallel", "configuration"]
edges: [
  {"target": "cust-phase-p0-platform-gate", "type": "part_of", "weight": 0.9, "note": "The sizing task that closes P0's second exit criterion"},
  {"target": "fact-gaudi2-hbm-and-bandwidth", "type": "depends_on", "weight": 0.9, "note": "96GB HBM2E at 2.45 TB/s per card is the budget this task re-plans around"},
  {"target": "question-what-tp-degree-fits-gaudi2", "type": "related_to", "weight": 0.9, "note": "The recorded configuration is the answer to this open question"},
  {"target": "pillar-measured-before-default", "type": "related_to", "weight": 0.9, "note": "Inheriting the reference config is exactly the failure mode this pillar forbids"},
  {"target": "cust-risk-r2-hbm-side-cache-pressure", "type": "related_to", "weight": 0.8, "note": "Undersizing here is what makes the side-cache pressure risk bite at low concurrency"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[question-what-tp-degree-fits-gaudi2]]"]
source_url: "Empty"
---

# Re-derive TP Degree, Max-Model-Len and Memory Utilization

The reference port was tuned on Gaudi 3: 128GB per card, 3.7 TB/s, TP4, 0.80 memory utilization. Gaudi 2 gives 96GB at 2.45 TB/s. Recompute tensor-parallel degree, `--max-model-len` and `--gpu-memory-utilization` for the actual card, on 4 devices.

Why it matters: those three values are not independent knobs. Model weight footprint, KV cache capacity and the eager sparse-MoE workspace all have to fit inside the same 96GB, and the side caches that P2 later migrates are outside scheduler accounting today. A config copied from the Gaudi 3 run does not just run out of memory — it fails in whatever way is hardest to read, usually under load rather than at boot.

Work the budget explicitly: weight footprint from the FP8 checkpoint, then what remains for KV cache at the candidate context length, then the headroom needed for eager workspace and activations. Sweep TP degree and context length as a pair and record the largest configuration that stays clear of OOM with margin. Do not treat 0.80 utilization as a default — on a smaller card it is a guess with someone else's risk tolerance baked in.

Done when: a TP degree, max-model-len and memory-utilization combination is recorded that fits without OOM, with the reasoning for each value.
