---
id: cust-phase-p4-pin-check
title: "P4a — Cheap Graph-Capture Win (Pin Check Before Heavy P3)"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Verify the build pin is at/after c05d75a and boot without --enforce-eager, recording which subgraphs still fail — a cheap check before heavy kernel authoring."
auto_inject: false
applicable_when: "When executing roadmap phase P4a, after P1 lands and before committing to heavy P3 kernel work"
confidence: 0.7
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the pin at/after c05d75a turns out not to cover GDN/HyperConnection hybrids on Suite 1.24.2, the 'cheap win' premise fails and P3 ordering must be re-decided"
tags: ["roadmap-phase", "p4a", "graph-capture", "pin", "ordering"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P4_pin_check — goal, two tasks, exit criteria"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "depends_on", "weight": 0.9, "note": "The check runs against the P1 build retargeted to plugin 0.30.0"},
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "derived_from", "weight": 0.9, "note": "Premise of the check: c05d75a resolved synStatus-26 #1734 for GDN hybrids with no plugin change"},
  {"target": "decision-pin-check-before-kernels", "type": "supports", "weight": 0.9, "note": "This phase is that decision executed — cheap check first because it may remove part of P3's motivation for free; roadmap flags the ordering as judgment, hence confidence 0.7"},
  {"target": "question-which-subgraphs-fail-capture", "type": "related_to", "weight": 0.9, "note": "The documented failure list this phase produces is the evidence that answers the question"},
  {"target": "cust-phase-p4-capture", "type": "followed_by", "weight": 0.9, "note": "Whatever survives the pin check defines P4b's remaining work"}
]
related: ["[[fact-pin-c05d75a-resolves-1734]]", "[[decision-pin-check-before-kernels]]", "[[question-which-subgraphs-fail-capture]]", "[[ref-upstream-vllm-pin]]"]
source_url: "Empty"
---

# P4a — Cheap Graph-Capture Win (Pin Check Before Heavy P3)

## Goal
Determine whether the upstream pin alone unblocks compiled mode for the GDN/HyperConnection regions: verify the build pin is at/after `c05d75a` — which resolved synStatus-26 issue #1734 for GDN hybrids with no plugin change — then boot without `--enforce-eager` and record exactly which subgraphs still fail. The roadmap explicitly flags this ordering as judgment on leverage, not a sourced claim: a cheap check before investing heavy effort in P3 kernel authoring.

## Depends on
P1 (build pinned at/after c05d75a). Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5 — the cheap pin check deliberately precedes heavy P3 kernel authoring.

## Tasks
- [[task-p4-1-verify-pin-c05d75a]] — confirm the build pin contains the sequence-parallel layer-boundary fix.
- [[task-p4-2-boot-without-enforce-eager]] — boot without --enforce-eager and record which subgraphs still fail to capture.

## Exit criteria
A documented list of remaining capture-failing subgraphs after the pin fix — this scopes P4b and may shrink P3.
