---
id: task-p4-1-verify-pin-c05d75a
title: Verify the Build Pin is at/after c05d75a
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Confirm the build pin is at/after c05d75a, the upstream commit that resolved synStatus-26 #1734 for GDN hybrids with no plugin change — the cheapest capture test.
auto_inject: false
applicable_when: P4 pin-check phase is active; precondition is the P1 exit criterion — build retargeted to the plugin 0.30.0 pin satisfying c05d75a+
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the build pin is already verified at/after c05d75a on this machine the task is done; if a later pin regresses issue #1734, the check must be re-run before any capture result is trusted"
tags: ["roadmap-task", "p4-pin-check", "pin", "graph-capture"]
edges: [
  {"target": "cust-phase-p4-pin-check", "type": "part_of", "weight": 0.9, "note": "P4.1; the cheap pin check the roadmap sequences before heavy P3 kernel authoring"},
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "depends_on", "weight": 0.95, "note": "The check exists because c05d75a (keep Qwen3Next layer boundaries sequence parallel) resolved synStatus-26 #1734 for GDN hybrids"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.85, "note": "Issue #1734 is the synStatus-26 / compileGraph failure the pin resolves; its recurrence reopens this check"},
  {"target": "decision-pin-check-before-kernels", "type": "related_to", "weight": 0.9, "note": "Executes the decision to run the cheap check before committing to kernel authoring"}
]
related: ["[[fact-pin-c05d75a-resolves-1734]]", "[[ref-issue-1734-synstatus-26]]", "[[decision-pin-check-before-kernels]]"]
source_url: "Empty"
---
# Verify the Build Pin is at/after c05d75a

Verify the build pin resolves at or after c05d75a (keep Qwen3Next layer boundaries sequence parallel) — the upstream commit that resolved synStatus-26 issue #1734 for GDN hybrids with no plugin change. Record the commit the build actually resolves to, not the intended one; the P1.3 retarget to the plugin 0.30.0 stable pin is supposed to satisfy c05d75a+ but is asserted, not measured. On 4x Gaudi 2 this is the cheapest possible graph-capture test: a pin-only unblock for GDN/HyperConnection changes what P4b still must do before any P3 kernel investment pays off. Done when: the pin is documented at/after c05d75a, feeding the phase exit — a documented list of remaining capture-failing subgraphs after the pin fix.
