---
id: bookmark-pr1829-diff
title: "Unprocessed: PR #1829 Description and Diff"
type: bookmark
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Un-ingested pointer to vllm-gaudi PR 1829's description and diff — the ~2.4k-line qwen4_exp.py that P1 retargets. Held as a bookmark, not converted."
auto_inject: false
applicable_when: "Before starting P1.1, when the port needs the actual PR text and code rather than the roadmap's summary of it"
confidence: 0.3
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the PR is merged, closed, or updated after capture, the stored description and diff no longer match what P1 must retarget — re-capture before porting"
tags: ["bookmark", "unprocessed", "pr-1829", "qwen4-exp", "raw-inbox"]
edges: [
  {"target": "source-vllm-gaudi-pr1829", "type": "derived_from", "weight": 0.8, "note": "Bookmark for the material the source node stands in for; the source exists, its diff does not live in raw/ yet"},
  {"target": "task-p1-1-port-qwen4-exp-model", "type": "related_to", "weight": 0.8, "note": "P1.1 bases the port on this file, so the diff is the primary input it is currently missing"},
  {"target": "note-seed-coverage-and-gaps", "type": "related_to", "weight": 0.8, "note": "Named in the seed gap list as a raw/ input that would close an open coverage hole"}
]
related: ["[[source-vllm-gaudi-pr1829]]", "[[fact-pr1829-scope-and-limits]]", "[[note-seed-coverage-and-gaps]]"]
source_url: "Empty"
---

# Unprocessed: PR #1829 Description and Diff

Pointer: pull request #1829 in the vllm-gaudi tracker — its description and full diff, whose centre is the ~2.4k-line `vllm_gaudi/models/qwen4_exp.py`. It matters because P1 is a retarget of exactly this code: every claim in the vault about the PR's scope, its pin `dd3bc9c72faf`, the dropped `mtp.*` head, and the excluded vision tower currently rests on the roadmap's summary rather than the source.

Ingesting it into `raw/` and converting would update `fact-pr1829-scope-and-limits`, `fact-model-architecture-blocks`, and `fact-target-stack-versions` at code level, likely create a fact for the HPU block APIs the port reuses, and retire one entry in `note-seed-coverage-and-gaps`.
