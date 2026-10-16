---
id: bookmark-pr1843-diff
title: "Unprocessed: PR #1843 Description and Diff"
type: bookmark
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Un-ingested pointer to vllm-gaudi PR 1843's description and diff — the four capture mitigations P4.3 integrates. Held as a bookmark, not converted."
auto_inject: false
applicable_when: "Before starting P4.3, when integrating the mitigations needs the actual code rather than the roadmap's four-item list"
confidence: 0.3
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If PR 1843 merges into the pinned 0.30.0 build after this capture, the diff no longer describes work to port — P4.3 becomes a presence check"
tags: ["bookmark", "unprocessed", "pr-1843", "graph-capture", "raw-inbox"]
edges: [
  {"target": "source-vllm-gaudi-pr1843", "type": "derived_from", "weight": 0.8, "note": "Bookmark for the PR text and diff the source node stands in for; neither is in raw/ yet"},
  {"target": "task-p4-3-apply-pr1843-mitigations", "type": "related_to", "weight": 0.8, "note": "P4.3 ports these fixes, so the diff is the missing primary input for that task"},
  {"target": "note-seed-coverage-and-gaps", "type": "related_to", "weight": 0.8, "note": "Listed in the seed gap register as a raw/ input that would close a known hole"}
]
related: ["[[source-vllm-gaudi-pr1843]]", "[[ref-pr1843-mitigations]]", "[[playbook-graph-capture-triage]]"]
source_url: "Empty"
---

# Unprocessed: PR #1843 Description and Diff

Pointer: pull request #1843 in the vllm-gaudi tracker — description plus diff. It matters because P4.3 is defined entirely by this PR's four changes (DS=0 concrete-plan recipe, host-side decode count fix, bmm score contraction fix, flat `index_copy_` store rewrite), and the vault knows them only as a four-line list: no merge status, no target release, no code, and no statement of whether they already ship in plugin 0.30.0.

Ingesting and converting would expand `ref-pr1843-mitigations` into per-mitigation detail, sharpen `task-p4-3-apply-pr1843-mitigations` into verifiable steps, feed concrete responses into `playbook-graph-capture-triage`, and likely create a fact recording the PR's merge state.
