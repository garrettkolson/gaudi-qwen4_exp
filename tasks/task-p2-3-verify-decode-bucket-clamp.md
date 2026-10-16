---
id: task-p2-3-verify-decode-bucket-clamp
title: Confirm Decode Block Buckets Clamp to Physical KV Size
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Verify the plugin v0.30.0 decode block bucket clamp to physical KV cache size is active, so decode buckets cannot oversubscribe the 96GB Gaudi 2 HBM.
auto_inject: false
applicable_when: P2 cache and memory plumbing is active; precondition is the P1.3 retarget having installed plugin v0.30.0, checked before the concurrency ramp
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the pinned plugin moves off v0.30.0, or the clamped-decode-bucket release-note feature does not hold in the installed build, this confirmation's specification is stale"
tags: ["roadmap-task", "p2", "decode-bucketing", "kv-cache", "plugin-0-30-0"]
edges: [
  {"target": "cust-phase-p2-cache-plumbing", "type": "part_of", "weight": 0.9, "note": "P2 task P2.3; the cheap confirmation that decode buckets respect physical KV size under load"},
  {"target": "fact-plugin-0-30-0-features", "type": "depends_on", "weight": 0.9, "note": "The clamp is a plugin v0.30.0 feature; that release-line claim is the check's entire basis"},
  {"target": "ref-vllm-gaudi-plugin", "type": "related_to", "weight": 0.7, "note": "The clamp ships in the vllm-gaudi plugin the build was retargeted to in P1"}
]
related: ["[[fact-plugin-0-30-0-features]]", "[[ref-vllm-gaudi-plugin]]"]
source_url: "Empty"
---
# Confirm Decode Block Buckets Clamp to Physical KV Size

Confirm the decode block bucket clamp to physical KV cache size — a plugin v0.30.0 feature — is actually active on the retargeted stack. Verification means observing that decode block buckets never exceed the physical KV allocation at target max-model-len on 4x Gaudi 2, under a load ramp rather than at idle. This matters because 96GB cards leave no overshoot margin: an unclamped bucket oversubscribes HBM at exactly the concurrency P2 must sustain, and the failure looks like the side-cache OOM P2.1 is fixing. Cheap check, large blast radius if skipped. Done when: stable at concurrency 8+ without side-cache OOM, with the clamped decode buckets confirmed active.
