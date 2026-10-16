---
id: playbook-graph-capture-triage
title: "Triaging HPU Graph Capture Failures"
type: playbook
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Order of resolution for a failed boot without --enforce-eager: pin first, list failing subgraphs, then classify against #1843 mitigations, host-coercing ops and the CustomOp contract."
auto_inject: false
applicable_when: "When a boot without --enforce-eager fails or a subgraph fails to capture during P4a or P4b"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a build pin demonstrably at/after c05d75a plus the PR #1843 mitigations produces a different failing-subgraph list, this triage order and its categories are out of date"
tags: ["playbook", "p4", "graph-capture", "synstatus-26", "triage", "eager"]
edges: [
  {"target": "concept-graph-capture-vs-eager", "type": "depends_on", "weight": 0.9, "note": "Eager is the correctness baseline and capture is the later lever — the distinction this triage preserves"},
  {"target": "task-p4-2-boot-without-enforce-eager", "type": "related_to", "weight": 0.9, "note": "Steps 1 and 2 are that task: pin first, then boot without the flag and record which subgraphs still fail"},
  {"target": "task-p4-4-eliminate-host-coercing-ops", "type": "related_to", "weight": 0.9, "note": "Step 5 is that task — the named ops in the QSA/PLE hot paths are the fixes to apply"},
  {"target": "ref-pr1843-mitigations", "type": "related_to", "weight": 0.85, "note": "The four mitigations in step 4, including the flat index_copy_ store rewrite that restores first-request survival"},
  {"target": "cust-phase-p4-capture", "type": "related_to", "weight": 0.9, "note": "The phase this serves: serve without --enforce-eager, or with a documented per-subgraph eager fallback for the QSA region only"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.8, "note": "The known synStatus-26 / synapse compileGraph blocker whose family a persistent failure after the pin points to"}
]
related: ["[[task-p4-2-boot-without-enforce-eager]]", "[[task-p4-3-apply-pr1843-mitigations]]", "[[question-which-subgraphs-fail-capture]]", "[[cust-risk-r3-sparse-topk-uncapturable]]"]
source_url: "Empty"
---

# Triaging HPU Graph Capture Failures

1. **Confirm the pin before reading any error.** Verify the build pin is at or after `c05d75a` — that commit resolved synStatus-26 (#1734) for GDN hybrids with no plugin change. *Check:* the pin hash is recorded, and no failure in the log is of the class that pin already fixes. Triaging a stale build wastes the whole exercise.
2. **Boot without `--enforce-eager` and write down every subgraph that still fails.** *Check:* a written list of failing subgraphs exists — it is P4a's exit criterion and the input to every later step.
3. **Classify each entry** into: (a) a missing PR #1843 mitigation; (b) a host-coercing op in a hot path; (c) a P3 CustomOp that violates the capture contract; (d) unresolved. *Check:* every entry has exactly one category, or is explicitly marked unresolved with its error text attached.
4. **Work category (a):** integrate the #1843 mitigations — the DS=0 concrete-plan recipe, the host-side decode count fix, the bmm score contraction fix, and the flat `index_copy_` store rewrite. *Check:* the subgraph re-captures, and the first request survives, which is what the store rewrite is for.
5. **Work category (b):** remove host-coercing ops from the QSA/PLE hot paths — `.nonzero` in PLE `_pool_and_store`, `.item()`, `torch.minimum` in `_expand_plan`, `keep.any()` in the KV-store epilogue. *Check:* the op no longer appears in that path and the subgraph re-captures on the next attempt.
6. **Work category (c):** prove the CustomOp meets the capture contract — single TPC kernel per descriptor and registration in the `custom_op` namespace. *Check:* both hold; if either was the gap, this is also evidence on the hypothesis that the contract gates capture.
7. **Re-boot and settle the remainder.** *Check:* it boots and serves on all TP workers without `--enforce-eager`, or the only remaining eager fallback is the QSA indexer region and that fallback is documented per subgraph.

## Stop and escalate

Stop and report when: synStatus-26 / compileGraph persists on a pin demonstrably at/after `c05d75a` with the #1843 mitigations applied — that is a new blocker, not this procedure's; the eager fallback has to grow beyond the QSA region, which changes P4b's exit criterion rather than satisfying it; or `--enforce-eager` is being re-added so a run looks green. Re-adding the flag is a labelled, reported state, never an undocumented fix.
