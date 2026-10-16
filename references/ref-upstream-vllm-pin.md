---
id: ref-upstream-vllm-pin
title: "Upstream vLLM Pin `c05d75a`"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "The upstream vLLM 0.30.0 build pin required at or after commit c05d75a, the change that resolved synStatus-26 (#1734) for GDN hybrids with no plugin change."
auto_inject: false
applicable_when: "When verifying or changing the upstream vLLM commit the plugin build is pinned to, or when scoping P4a"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the resolved build commit predates c05d75a, or the upstream vLLM 0.30.0 tree no longer contains a commit with that hash and title, the pin requirement stated here is unmet or misstated"
tags: ["upstream-vllm", "pin", "commit", "graph-capture", "synstatus-26"]
edges: [
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "related_to", "weight": 0.9, "note": "The fact node states what the pinned commit changed; this reference is the pin itself"},
  {"target": "fact-target-stack-versions", "type": "related_to", "weight": 0.9, "note": "The stack records upstream vLLM 0.30.0 pinned at/after c05d75a as part of the target environment"},
  {"target": "task-p1-3-retarget-pin-to-0-30-0", "type": "related_to", "weight": 0.85, "note": "P1.3 moves the PR pin dd3bc9c72faf to the 0.30.0 stable pin that satisfies this requirement"},
  {"target": "cust-phase-p4-pin-check", "type": "related_to", "weight": 0.8, "note": "P4a is the cheap test of whether this pin alone unblocks capture for GDN/HyperConnection"}
]
related: ["[[fact-pin-c05d75a-resolves-1734]]", "[[cust-phase-p4-pin-check]]", "[[task-p4-1-verify-pin-c05d75a]]"]
source_url: "Empty"
---

# Upstream vLLM Pin `c05d75a`

A commit-level pin on upstream vLLM 0.30.0: the roadmap requires the build to sit at or after `c05d75a`, described as "Keep Qwen3Next layer boundaries sequence parallel", and credits it with resolving synStatus-26 (issue #1734) for GDN hybrids without any plugin change. Current known state per the roadmap: plugin 0.30.0's stable pin is expected to satisfy `c05d75a`+, while PR #1829's own pin `dd3bc9c72faf` predates the target and must be retargeted in P1.3. The roadmap supplies the hash, the commit title and the claimed effect — nothing more.

Before relying on this: resolve the hash in the upstream vLLM repository and read the diff, confirm the ordering against `dd3bc9c72faf` is real rather than assumed, confirm which commit the installed 0.30.0 build actually pins, and treat the capture benefit as unverified on Gaudi 2 until P4.1 verifies the pin and P4.2 boots without `--enforce-eager`.
