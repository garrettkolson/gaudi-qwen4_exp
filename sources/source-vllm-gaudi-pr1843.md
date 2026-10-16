---
id: source-vllm-gaudi-pr1843
title: vllm-gaudi PR #1843 — Capture Mitigations
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "vllm-gaudi PR #1843, source of the four graph-capture mitigations P4b must integrate: DS=0 concrete plan, host-side decode count, bmm score contraction, flat index_copy_ store."
auto_inject: false
applicable_when: "When integrating capture mitigations in P4b or triaging a capture failure in the QSA or PLE path"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the archived PR #1843 diff shows fixes different from the roadmap's four named items, or the mitigations land in a plugin release so integration becomes a version bump, this source and its task change scope"
tags: ["vllm-gaudi", "pr-1843", "graph-capture", "compiled-mode", "qsa"]
edges: [
  {"target": "task-p4-3-apply-pr1843-mitigations", "type": "supports", "weight": 0.9, "note": "The task is the integration of exactly this PR's four mitigations into the port"},
  {"target": "cust-phase-p4-capture", "type": "supports", "weight": 0.8, "note": "P4b's exit depends on these mitigations: first-request survival and removal of host-coercing behaviour"},
  {"target": "ref-pr1843-mitigations", "type": "related_to", "weight": 0.9, "note": "The reference node carries the mitigation list as a checkable item; this source is where the list came from"},
  {"target": "bookmark-pr1843-diff", "type": "followed_by", "weight": 0.7, "note": "Description and diff still need dropping into raw/; recipe details are currently the roadmap's summary only"}
]
related: ["[[ref-pr1843-mitigations]]", "[[task-p4-3-apply-pr1843-mitigations]]", "[[cust-phase-p4-capture]]", "[[bookmark-pr1843-diff]]"]
source_url: "Empty"
---
# vllm-gaudi PR #1843 — Capture Mitigations

vllm-gaudi pull request #1843, the source of the graph-capture mitigations the roadmap schedules for P4b: the DS=0 concrete-plan recipe, a host-side decode count fix, a bmm score contraction fix, and a flat `index_copy_` store rewrite that restores first-request survival. All four appear in the roadmap's `evidence_grounded` list, so they are treated as sourced rather than inferred.

In this vault it grounds `task-p4-3-apply-pr1843-mitigations`, `ref-pr1843-mitigations` and the P4b capture phase, and it feeds `playbook-graph-capture-triage` as known-good answers to recurring failure signatures.

What is *not* here is the PR itself. The roadmap supplies a four-item summary, not the diff, so the exact conditions each mitigation addresses — shape guards, kernel signatures, plugin version the fixes target — remain unverified until the description and diff land in `raw/` (`bookmark-pr1843-diff`). The roadmap gives no URL for the PR, so none is recorded.
