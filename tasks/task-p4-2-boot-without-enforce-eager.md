---
id: task-p4-2-boot-without-enforce-eager
title: Boot Without --enforce-eager and Record Failures
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Boot without --enforce-eager after the pin check and document which subgraphs still fail HPU graph capture; the failure list is P4b's input.
auto_inject: false
applicable_when: P4 pin-check phase is active; precondition is P4.1 having verified the build pin at/after c05d75a
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the boot is run before the P4.1 pin is verified, or on a build whose P1 smoke battery has not reproduced, the recorded failures are unattributable and the subgraph list is stale"
tags: ["roadmap-task", "p4-pin-check", "graph-capture", "enforce-eager"]
edges: [
  {"target": "cust-phase-p4-pin-check", "type": "part_of", "weight": 0.9, "note": "P4.2; produces the phase's artifact — the documented list of capture-failing subgraphs"},
  {"target": "concept-graph-capture-vs-eager", "type": "depends_on", "weight": 0.85, "note": "Reading the outcome requires the eager versus HPU-graph-capture distinction"},
  {"target": "question-which-subgraphs-fail-capture", "type": "related_to", "weight": 0.9, "note": "The recorded failure list is the measured answer to which subgraphs still fail after the pin fix"},
  {"target": "task-p4-1-verify-pin-c05d75a", "type": "depends_on", "weight": 0.8, "note": "The boot test is only attributable once the pin is verified; otherwise failures reflect a known-resolved issue"},
  {"target": "playbook-graph-capture-triage", "type": "related_to", "weight": 0.8, "note": "Classify each captured failure with the graph-capture triage procedure"}
]
related: ["[[question-which-subgraphs-fail-capture]]", "[[playbook-graph-capture-triage]]", "[[concept-graph-capture-vs-eager]]"]
source_url: "Empty"
---
# Boot Without --enforce-eager and Record Failures

Boot the server on Gaudi 2 without --enforce-eager and record, per subgraph, which graph captures still fail after the pin fix. Run it only after P4.1 confirms the pin is at/after c05d75a — otherwise every failure re-reports the already-resolved synStatus-26 issue instead of the model's real capture limits. The failure list is P4b's input: it decides whether compiled mode is achievable as-is or still needs the PR #1843 mitigations, host-coercing-op removal, and the P3 CustomOps meeting the capture contract. Triage with the capture playbook. Done when: a documented list of remaining capture-failing subgraphs after the pin fix exists.
