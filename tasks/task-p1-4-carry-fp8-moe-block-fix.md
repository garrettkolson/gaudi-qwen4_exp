---
id: task-p1-4-carry-fp8-moe-block-fix
title: "Carry the FP8 MoE Block-Grid Fix"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Carry the _effective_moe_block_size fix from the PR's extension/ops.py into the 0.30.0 build so FP8 MoE weight grids are sized correctly."
auto_inject: false
applicable_when: "P1, alongside the pin retarget; the fix must be present before any MoE correctness or throughput measurement"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If plugin 0.30.0 already contains an equivalent block-size correction upstream, this task becomes a verification that the fix is present rather than a port"
tags: ["roadmap-task", "p1", "fp8", "moe", "bug-fix"]
edges: [
  {"target": "cust-phase-p1-reuse-pr1829", "type": "part_of", "weight": 0.9, "note": "One of the specific PR changes the roadmap requires be carried forward"},
  {"target": "fact-plugin-0-30-0-features", "type": "related_to", "weight": 0.8, "note": "The target release's FP8 and MoE work determines whether the fix is still needed or already upstream"},
  {"target": "concept-moe-expert-parallel-vs-tp", "type": "related_to", "weight": 0.7, "note": "Correct block sizing is a precondition for any meaningful statement about MoE sharding strategy"},
  {"target": "task-p1-3-retarget-pin-to-0-30-0", "type": "depends_on", "weight": 0.8, "note": "Whether the fix is still required is only answerable once the build sits on 0.30.0"}
]
related: ["[[cust-phase-p1-reuse-pr1829]]", "[[task-p1-3-retarget-pin-to-0-30-0]]"]
source_url: "Empty"
---

# Carry the FP8 MoE Block-Grid Fix

The PR carries a correction in `extension/ops.py` centred on `_effective_moe_block_size`. Carry it into the 0.30.0 build and confirm it is still doing work there.

Why it matters: FP8 MoE weights are laid out in blocks, and the block grid the stack computes has to agree with the grid the checkpoint was quantized with. When those disagree the damage is quiet — the wrong block is addressed for a slice of experts, so output is wrong only for some tokens on some experts. That failure mode hides behind plausible text and only shows up as degraded quality on a needle-retrieval or arithmetic probe, or as a mismatch under a byte-equality check.

Because this is a fix inside plugin internals, it is exactly the kind of change that vanishes silently during a version bump. Treat the task as two steps: check whether 0.30.0 already corrects the same behaviour upstream, and if not, reapply the fix and note where it had to move. If it turns out to be redundant upstream, say so explicitly — a fix nobody can find in the diff later is indistinguishable from a fix that was lost.

Done when: FP8 MoE block sizing is confirmed correct on 0.30.0, either by carrying the fix or by showing the upstream release already handles it.
