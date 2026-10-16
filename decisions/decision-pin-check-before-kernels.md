---
id: decision-pin-check-before-kernels
title: Run the Cheap Pin Check Before Committing to Kernel Authoring
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Verify the build pin includes c05d75a and boot without --enforce-eager before heavy P3 kernel authoring. The roadmap flags this ordering as judgment on leverage, not a sourced claim.
auto_inject: false
applicable_when: Between P1 and P3, before committing engineering effort to TPC kernel authoring
confidence: 0.65
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P4.2 shows the pin changes nothing about capture failures on Gaudi 2, the cheap-win premise of this ordering fails and P3 becomes the unqualified next step"
tags: ["decision", "sequencing", "pin-c05d75a", "graph-capture", "author-inference"]
edges: [
  {"target": "cust-phase-p4-pin-check", "type": "related_to", "weight": 0.9, "note": "P4a is this decision made operational: verify the pin, boot without --enforce-eager, record failing subgraphs"},
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "supports", "weight": 0.8, "note": "The evidence side: c05d75a resolved synStatus-26 #1734 for GDN hybrids with no plugin change, so the check may be free progress"},
  {"target": "hyp-customop-gates-compile-capture", "type": "related_to", "weight": 0.7, "note": "Related inference also flagged by the roadmap: if single-kernel CustomOps gate capture, the pin check may shrink what P3 must deliver"},
  {"target": "task-p4-1-verify-pin-c05d75a", "type": "related_to", "weight": 0.85, "note": "The concrete check: confirm the build pin is at/after c05d75a before anything else"}
]
related: ["[[cust-phase-p4-pin-check]]", "[[fact-pin-c05d75a-resolves-1734]]", "[[task-p4-1-verify-pin-c05d75a]]", "[[question-which-subgraphs-fail-capture]]"]
source_url: "Empty"
---

# Run the Cheap Pin Check Before Committing to Kernel Authoring

## Context

Upstream vLLM pin `c05d75a` ("Keep Qwen3Next layer boundaries sequence parallel") resolved issue #1734 — synStatus-26 / synapse `compileGraph` — for GDN hybrids with no plugin change. P3's TPC kernel authoring is the expensive part of the roadmap. The recommended execution order therefore inserts the cheap P4 pin check between P1 and P3: verify the pin, then boot without `--enforce-eager` and record which subgraphs still fail capture. The roadmap explicitly flags this ordering as "judgment on leverage, not a source claim", which is why this node's confidence is capped at 0.65.

## Alternatives considered

Author all three P3 kernels first, then revisit capture. Skip eager validation and target compiled mode directly, contradicting the eager-first baseline.

## Decision

Run the pin check before heavy P3. Verify the build pin is at/after `c05d75a`, boot without `--enforce-eager` on Gaudi 2, and produce a documented list of remaining capture-failing subgraphs.

## Consequence

If the pin alone unblocks capture for GDN/HyperConnection regions, part of P3's motivation disappears for free and kernel effort narrows to what actually fails. If it changes nothing, the cost is one boot-and-record cycle, and P3 proceeds with a better-scoped target list.
