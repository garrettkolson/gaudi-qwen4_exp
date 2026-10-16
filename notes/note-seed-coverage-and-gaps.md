---
id: note-seed-coverage-and-gaps
title: Seed Coverage and Known Gaps
type: note
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: What the seed converted from the roadmap, and the four inputs — PR diffs, release notes, HCCL table, measurements — that the conversion could not use.
auto_inject: false
applicable_when: When deciding whether the vault is authoritative on a topic, or before ingesting new material into raw/
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If any bookmarked raw/ input is ingested or a Gaudi 2 measurement lands, the matching gap entry here is obsolete and must be rewritten"
tags: ["seed-build", "coverage", "gaps", "raw-inputs", "audit"]
edges: [
  {"target": "event-2026-10-15-vault-seed-build", "type": "derived_from", "weight": 0.9, "note": "This note is the coverage report of the 111-node seed build event"},
  {"target": "bookmark-pr1829-diff", "type": "related_to", "weight": 0.85, "note": "Open gap: PR #1829 description and diff never ingested"},
  {"target": "bookmark-pr1843-diff", "type": "related_to", "weight": 0.85, "note": "Open gap: PR #1843 description and diff never ingested"},
  {"target": "bookmark-hccl-primitives-table", "type": "related_to", "weight": 0.85, "note": "Open gap: the primitives table 404'd, so all2all rests on secondary snippets"},
  {"target": "bookmark-tpc-sdk-kernel-guide", "type": "related_to", "weight": 0.8, "note": "Open gap: kernel-authoring guide held as a bookmark, not converted"},
  {"target": "note-provenance-register", "type": "related_to", "weight": 0.8, "note": "Gaps are what a source lacks; provenance is what a claim rests on — read together"}
]
related: ["[[note-provenance-register]]", "[[event-2026-10-15-vault-seed-build]]", "[[source-roadmap-qwen4-exp-gaudi2-v1-1]]"]
source_url: "Empty"
---
# Seed Coverage and Known Gaps

## Converted

The seed read `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json` and produced 111 nodes, counted off the Seed Manifest tables: 4 pillars, 14 custom (8 roadmap-phase, 6 roadmap-risk), 27 tasks, 7 decisions, 10 facts, 5 hypotheses, 5 questions, 11 concepts, 5 playbooks, 8 references, 7 sources, 4 bookmarks, 2 events, 2 notes. All 8 phases, all 27 tasks, all 6 risks, the target stack, the execution order and both provenance lists are represented. `patterns/` and `contacts/` are deliberately empty: no validated solution yet, no named owners.

## Gaps and the input that closes each

- **PR #1829 description and diff not ingested.** The vault knows the ~2.4k-line `qwen4_exp.py`, the pin `dd3bc9c72faf` and the exclusions only as the roadmap summarised them; P1 effort estimates rest on that summary. Closes with `raw/2026-10-15-vllm-gaudi-pr1829-description-and-diff.md`.
- **PR #1843 description and diff not ingested.** Four mitigations are named without their code, so P4b scope is unverified. Closes with `raw/2026-10-15-vllm-gaudi-pr1843-description-and-diff.md`.
- **Plugin v0.30.0 release notes not ingested.** Gathered-expert MoE combine, clamped decode buckets and TPC-native `causal_conv1d` are asserted, not read; P5.1 and P2.3 hang off them. Closes with `raw/2026-10-15-vllm-gaudi-release-notes-v0.24.0-v0.30.0.md`.
- **HCCL supported-primitives table returned 404 under `latest`.** all2all existence rests on secondary snippets and per-primitive dtype/topology caveats are unknown. Closes with `raw/2026-10-15-hccl-supported-primitives-table-v1.24.2.md`, fetched from the versioned docs path.
- **Zero measurements taken on Gaudi 2 hardware.** Every `hyp-*` node, the P0 exit criteria, the TP/context fit and all throughput claims are asserted; `verified_at` is Empty vault-wide. Closes with the P0 artifacts as raw inputs: `raw/2026-10-15-p0-2-fp8-mme-benchmark.md`, `raw/2026-10-15-p0-5-hccl-collective-bandwidth.md` and the P0.3 config-fit log.
