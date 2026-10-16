---
id: fact-pin-c05d75a-resolves-1734
title: "Upstream Pin c05d75a Resolved synStatus-26 for GDN Hybrids"
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Upstream vLLM pin c05d75a ("Keep Qwen3Next layer boundaries sequence parallel") resolved synStatus-26 issue #1734 for GDN hybrids with no plugin change.
auto_inject: false
applicable_when: "Empty"
confidence: 0.88
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If issue #1734 is reopened, or a boot on Gaudi 2 at a pin at/after c05d75a still raises synStatus-26 / compileGraph for GDN hybrids, this resolution no longer holds"
tags: ["upstream-pin", "c05d75a", "synstatus-26", "issue-1734", "gdn", "graph-capture"]
edges: [
  {"target": "ref-issue-1734-synstatus-26", "type": "derived_from", "weight": 0.85, "note": "The resolution claim is about issue #1734, the synStatus-26 / compileGraph family"},
  {"target": "ref-upstream-vllm-pin", "type": "related_to", "weight": 0.9, "note": "c05d75a is the upstream vLLM pin this stack and P4.1 verify against"},
  {"target": "task-p4-1-verify-pin-c05d75a", "type": "supports", "weight": 0.9, "note": "P4.1 checks the build pin is at/after c05d75a precisely because that pin carries this resolution"},
  {"target": "cust-phase-p4-pin-check", "type": "supports", "weight": 0.85, "note": "The whole cheap P4a pin-check phase rests on this pin having resolved #1734"}
]
related: ["[[ref-upstream-vllm-pin]]", "[[ref-issue-1734-synstatus-26]]", "[[task-p4-1-verify-pin-c05d75a]]", "[[cust-phase-p4-pin-check]]"]
source_url: "Empty"
---

# Upstream Pin c05d75a Resolved synStatus-26 for GDN Hybrids

Upstream vLLM commit `c05d75a`, described as "Keep Qwen3Next layer boundaries sequence parallel," resolved the synStatus-26 graph-capture failure tracked as issue #1734 for Gated-DeltaNet hybrid models — and it did so with no vllm-gaudi plugin change. The roadmap states this in P4.1 ("Verify build pin is at/after c05d75a ... resolved synStatus-26 #1734 for GDN hybrids with NO plugin change") and lists it under `evidence_grounded` ("#1734 resolution via upstream pin c05d75a"). As a PR/issue-content claim it is externally checkable, so confidence is high.

This is the load-bearing fact behind the cheap P4a pin check: if the build pin already sits at/after `c05d75a`, part of the #1734-family blocker for compiled mode may already be gone for free, before any heavy P3 kernel authoring. P1.3's retarget to plugin 0.30.0 is noted as satisfying the `c05d75a`+ requirement.

This node states that the pin resolved #1734 for GDN hybrids. It does NOT claim compiled mode now boots cleanly on this Gaudi 2 box — which subgraphs still fail capture is open (P4.2 / `question-which-subgraphs-fail-capture`), and nothing has been measured here, so `verified_at` is Empty.
