---
id: task-p1-3-retarget-pin-to-0-30-0
title: "Retarget from the PR Pin to Plugin 0.30.0"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Move the build off PR #1829's pinned dd3bc9c72faf onto the stable plugin 0.30.0 pin, which also satisfies the c05d75a-or-later requirement for capture."
auto_inject: false
applicable_when: "P1, early — before broad model edits, so later work is written against the interfaces that will actually ship"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a plugin release newer than 0.30.0 becomes the target, re-check that the new pin still contains c05d75a and that the interfaces this port touches have not moved again"
tags: ["roadmap-task", "p1", "dependency-pin", "versioning"]
edges: [
  {"target": "cust-phase-p1-reuse-pr1829", "type": "part_of", "weight": 0.9, "note": "Retargeting the dependency is the definitional work of this phase's title"},
  {"target": "fact-target-stack-versions", "type": "depends_on", "weight": 0.9, "note": "The target stack fixes plugin 0.30.0 and upstream vLLM at or after c05d75a"},
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "supports", "weight": 0.85, "note": "The stable pin is what carries the upstream change that resolved synStatus-26 for GDN hybrids"},
  {"target": "ref-upstream-vllm-pin", "type": "related_to", "weight": 0.85, "note": "The pin is the concrete upstream commit this task moves the build onto"}
]
related: ["[[cust-phase-p1-reuse-pr1829]]", "[[fact-pin-c05d75a-resolves-1734]]"]
source_url: "Empty"
---

# Retarget from the PR Pin to Plugin 0.30.0

PR #1829 was built against a specific upstream pin, `dd3bc9c72faf`. Move the build onto the stable plugin 0.30.0 pin, which satisfies the roadmap's requirement of `c05d75a` or later.

Why it matters twice over. First, shipping against a PR's personal pin is a slow leak: the pin stops moving, and every later fix has to be back-ported by hand. Second, and more immediately, the commit range the roadmap relies on contains the change that resolved synStatus-26 (#1734) for GDN hybrids with no plugin change at all. Taking the stable pin now means the P4 pin check starts from a position where the cheap capture win is already available, instead of being discovered late as an excuse to redo work.

Do this before broad model edits, not after: the value is in writing P1's changes against the interfaces that will actually ship. When the bump breaks something, record exactly which interface moved and in which direction — that list is what tells you whether the port's abstractions are holding or whether the PR was leaning on internals.

Done when: the build resolves plugin 0.30.0, the resulting upstream pin is confirmed at or after `c05d75a`, and P1 work continues against it.
