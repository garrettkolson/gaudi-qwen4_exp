---
id: fact-target-stack-versions
title: "Target Stack: Suite 1.24.2, PyTorch 2.13, Plugin 0.30.0, 4x Gaudi 2"
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Target stack: Gaudi Software Suite 1.24.2, PyTorch 2.13, vllm-gaudi plugin 0.30.0, upstream vLLM pinned at/after c05d75a, on 4x Gaudi 2.
auto_inject: false
applicable_when: "Empty"
confidence: 0.95
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the deployed environment runs a Suite, PyTorch, or plugin version other than 1.24.2 / 2.13 / 0.30.0, or the upstream vLLM pin predates c05d75a, this stack statement no longer describes the target"
tags: ["target-stack", "versions", "vllm-gaudi", "gaudi-suite", "pin"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Every version here is read verbatim from the roadmap's target_stack block"},
  {"target": "ref-vllm-gaudi-plugin", "type": "related_to", "weight": 0.9, "note": "Plugin 0.30.0 is the vllm-gaudi release this stack pins to"},
  {"target": "ref-upstream-vllm-pin", "type": "related_to", "weight": 0.9, "note": "The upstream vLLM 0.30.0 pin at/after c05d75a is part of this stack"},
  {"target": "task-p1-3-retarget-pin-to-0-30-0", "type": "supports", "weight": 0.9, "note": "P1.3 retargets the PR pin to 0.30.0 because this stack names 0.30.0 as the target"}
]
related: ["[[ref-vllm-gaudi-plugin]]", "[[ref-upstream-vllm-pin]]", "[[task-p1-3-retarget-pin-to-0-30-0]]"]
source_url: "Empty"
---

# Target Stack: Suite 1.24.2, PyTorch 2.13, Plugin 0.30.0, 4x Gaudi 2

The roadmap's `target_stack` names the exact environment for this enablement: Gaudi software suite 1.24.2, PyTorch 2.13, vllm-gaudi plugin 0.30.0, upstream vLLM 0.30.0 pinned at/after commit `c05d75a`, on 4x Gaudi 2 (96GB HBM2E @ 2.45 TB/s per card, FP8 E4M3/E5M2). The reference port source is named as vllm-gaudi PR #1829 (Gaudi 3, eager-only). These are version strings stated directly in the roadmap and echoed in CLAUDE.md, and each is externally checkable against the relevant release, so confidence is at the top of the externally-checkable band.

This node records what the target versions are. It does NOT assert that the environment is currently installed at these levels, nor that plugin 0.30.0 is actually running anywhere — the roadmap describes the destination stack, and P1.3 exists precisely to move the PR's pin `dd3bc9c72faf` to the 0.30.0 stable pin that satisfies the `c05d75a`+ requirement. No environment has been verified against these versions on the target box, so `verified_at` is Empty.
