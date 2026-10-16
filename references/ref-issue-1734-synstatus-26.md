---
id: ref-issue-1734-synstatus-26
title: "vllm-gaudi Issue #1734 — synStatus-26 / compileGraph"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "Upstream vllm-gaudi issue 1734: synapse compileGraph fails with synStatus-26 during HPU graph capture; named known blocker of the compiled-mode path."
auto_inject: false
applicable_when: "When booting without --enforce-eager, or triaging a capture failure that mentions synStatus-26 or compileGraph"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the pin at/after c05d75a is verified and P4.2 boots without --enforce-eager with no synStatus-26 in any worker log, this issue is no longer the blocker for the path in question"
tags: ["issue-1734", "synstatus-26", "compile-graph", "graph-capture", "gdn", "upstream-issue"]
edges: [
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "related_to", "weight": 0.95, "note": "The fact node records that this issue was resolved for GDN hybrids by the upstream pin, with no plugin change"},
  {"target": "cust-phase-p4-capture", "type": "related_to", "weight": 0.9, "note": "The roadmap names the #1734 family as P4b's known_blocker"},
  {"target": "concept-graph-capture-vs-eager", "type": "related_to", "weight": 0.9, "note": "This is the concrete failure mode that keeps the plan on eager until capture work lands"},
  {"target": "concept-gdn-gated-delta-net", "type": "related_to", "weight": 0.8, "note": "GDN hybrids are the reported class of affected subgraph, via Qwen3Next layer boundaries"},
  {"target": "hyp-sparse-topk-not-capturable", "type": "related_to", "weight": 0.6, "note": "Weak link: whether the sparse top-k region fails for the same reason or a different one is unmeasured"}
]
related: ["[[fact-pin-c05d75a-resolves-1734]]", "[[cust-phase-p4-capture]]", "[[question-which-subgraphs-fail-capture]]"]
source_url: "Empty"
---

# vllm-gaudi Issue #1734 — synStatus-26 / compileGraph

Issue number 1734 in the vllm-gaudi tracker, and by extension the family of failures the roadmap calls "synStatus-26 / synapse compileGraph": the synapse compiler refuses to build a graph and the HPU-graph capture step aborts. The roadmap lists it as P4b's known blocker and, in the same breath, as evidence that an upstream vLLM change titled "Keep Qwen3Next layer boundaries sequence parallel" (commit `c05d75a`) resolved it for GDN hybrids with no plugin change. That dual status — open blocker for the phase, resolved by a pin for a class of subgraphs — is the roadmap's own framing.

Before relying on this: open the thread and check which subgraphs it actually covers, confirm the reported Suite/synapse version matches 1.24.2, verify the `c05d75a` claim by reading the commit, and treat "resolved" as scoped to GDN/HyperConnection only until P4.2 records which subgraphs still fail on Gaudi 2.
