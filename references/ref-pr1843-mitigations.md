---
id: ref-pr1843-mitigations
title: "PR #1843 Capture Mitigations"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "vllm-gaudi PR 1843: four graph-capture fixes — DS=0 concrete-plan recipe, host-side decode count, bmm score contraction, flat index_copy_ store — for P4b."
auto_inject: false
applicable_when: "When integrating capture fixes into the ported model, or triaging a capture failure in the QSA/PLE hot paths"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PR 1843 is merged and all four changes are already present in the pinned plugin 0.30.0 build, task P4.3 becomes a presence check rather than a port"
tags: ["pr-1843", "graph-capture", "mitigations", "index-copy", "decode-count", "vllm-gaudi"]
edges: [
  {"target": "task-p4-3-apply-pr1843-mitigations", "type": "related_to", "weight": 0.95, "note": "P4.3 is the task that integrates these four mitigations into the port"},
  {"target": "source-vllm-gaudi-pr1843", "type": "related_to", "weight": 0.9, "note": "The source node is the PR itself; only its description is captured, not the diff"},
  {"target": "playbook-graph-capture-triage", "type": "related_to", "weight": 0.85, "note": "These four fixes are the known-good responses the triage playbook tries first"},
  {"target": "cust-phase-p4-capture", "type": "related_to", "weight": 0.85, "note": "P4b's exit criteria assume these mitigations are in the build being tested"}
]
related: ["[[task-p4-3-apply-pr1843-mitigations]]", "[[bookmark-pr1843-diff]]", "[[playbook-graph-capture-triage]]"]
source_url: "Empty"
---

# PR #1843 Capture Mitigations

Pull request number 1843 against vllm-gaudi. The roadmap grounds four concrete fixes in it and lists them as evidence-backed rather than inferred: a DS=0 concrete-plan recipe, a host-side decode count fix, a bmm score contraction fix, and a flat `index_copy_` store rewrite that restores first-request survival. Current known state in this vault is exactly that four-item list; the PR description and diff have not been ingested, so none of the four is understood at code level here, and the roadmap does not say whether the PR was merged or in which release it landed.

Before relying on this: read the PR (diff and review thread), record merge status and target release, check whether each of the four is already present in plugin 0.30.0 — duplicating an upstream fix is wasted work — and confirm the flat `index_copy_` rewrite interacts correctly with the ported QSA/PLE store paths rather than the PR author's model.
