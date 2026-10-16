---
id: question-which-subgraphs-fail-capture
title: Which Subgraphs Still Fail to Capture After the Pin Fix?
type: question
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Unknown which parts of the qwen4_exp forward still fail HPU graph capture once the build pin is at/after c05d75a; P4a exists to produce that list.
auto_inject: false
applicable_when: Before committing P3 kernel effort, and when choosing which P4b exit branch applies
confidence: 0.4
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "Once P4.2's boot without --enforce-eager yields a documented list of remaining capture-failing subgraphs, this question is answered"
tags: ["graph-capture", "hpu-graph", "enforce-eager", "p4a", "open-question"]
edges: [
  {"target": "task-p4-2-boot-without-enforce-eager", "type": "related_to", "weight": 0.9, "note": "P4.2 is the observation: boot without --enforce-eager and record which subgraphs fail"},
  {"target": "cust-phase-p4-pin-check", "type": "related_to", "weight": 0.9, "note": "The documented failing-subgraph list is literally P4a's exit criterion"},
  {"target": "hyp-sparse-topk-not-capturable", "type": "related_to", "weight": 0.8, "note": "Whether the QSA indexer appears in the list is the direct test of that hypothesis"},
  {"target": "playbook-graph-capture-triage", "type": "related_to", "weight": 0.8, "note": "The triage procedure that turns raw synapse failures into a classified per-subgraph list"}
]
related: ["[[fact-pin-c05d75a-resolves-1734]]", "[[decision-pin-check-before-kernels]]", "[[ref-issue-1734-synstatus-26]]"]
source_url: "Empty"
---

# Which Subgraphs Still Fail to Capture After the Pin Fix?

## The question

With the build pin at or after `c05d75a`, which subgraphs of the Qwen3.8-Flash-Next forward still fail HPU graph capture, and which now capture?

## Why it blocks the plan

The pin is the cheap lever: it resolved synStatus-26 for GDN hybrids with no plugin change, which is precisely why the pin check runs before heavy P3 kernel authoring. Without the post-pin failure list, the P3 work queue is guesswork — kernels get written for primitives that may already capture, while the actual blocker stays unfused and the P3 effort is spent in the wrong order. P4b also has two exit branches, full compiled serving or a documented per-subgraph eager fallback for the QSA indexer only, and this list is what decides which one is the target.

## What answers it

`task-p4-2-boot-without-enforce-eager`: after `task-p4-1-verify-pin-c05d75a` confirms the pin, boot without `--enforce-eager` on all TP workers and record failing subgraphs following the capture-triage playbook. That documented list is P4a's exit criterion and the input that confirms or reorders P3.
