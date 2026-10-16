---
id: note-provenance-register
title: Provenance Register — What Is Sourced and What Is Inference
type: note
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: The roadmap's evidence_grounded and author_inference_flagged lists, item by item, each mapped to the vault nodes that depend on it.
auto_inject: false
applicable_when: Before trusting any roadmap-derived claim, and when setting confidence on a new node built from the roadmap
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the roadmap is revised to v1.2 or the provenance block changes, this register is stale and every confidence derived from it needs a re-read"
tags: ["provenance", "evidence", "inference", "audit", "seed-build"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.95, "note": "Both lists transcribed verbatim from the provenance block of the roadmap JSON"},
  {"target": "pillar-provenance-discipline", "type": "related_to", "weight": 0.9, "note": "This note is the operational form of the pillar that keeps evidence and inference apart"},
  {"target": "hyp-customop-gates-compile-capture", "type": "related_to", "weight": 0.85, "note": "The P3 to P4 ordering inference is flagged here, which is why the hypothesis sits at low confidence"},
  {"target": "fact-hccl-includes-all2all", "type": "related_to", "weight": 0.85, "note": "Its all2all entry is corroborated by snippets, not the primitives table — the register records the difference"},
  {"target": "question-hccl-primitive-caveats", "type": "related_to", "weight": 0.8, "note": "The open question the fourth flagged inference leaves behind"},
  {"target": "decision-pin-check-before-kernels", "type": "related_to", "weight": 0.85, "note": "A decision resting on flagged judgment about leverage, not on a source claim"}
]
related: ["[[pillar-provenance-discipline]]", "[[source-roadmap-qwen4-exp-gaudi2-v1-1]]", "[[note-seed-coverage-and-gaps]]"]
source_url: "Empty"
---

# Provenance Register — What Is Sourced and What Is Inference

Both lists quoted exactly from the roadmap's provenance block; each entry names the nodes that depend on it.

## Evidence grounded

1. "PR #1829 scope/limitations/failure sites" — reuse base and limits: `fact-pr1829-scope-and-limits`, `decision-reuse-pr1829-as-base`, `cust-phase-p1-reuse-pr1829`.
2. "#1734 resolution via upstream pin c05d75a" — the pin fix: `fact-pin-c05d75a-resolves-1734`, `cust-phase-p4-pin-check`.
3. "PR #1843 mitigations (DS=0 recipe, flat index_copy_ rewrite)" — the capture fixes: `ref-pr1843-mitigations`, `task-p4-3-apply-pr1843-mitigations`.
4. "Plugin v0.24.0/v0.30.0 release notes (TPC-native causal_conv1d; FP8/INC stability; gathered-expert MoE combine)" — plugin capability: `fact-plugin-0-30-0-features`, `task-p5-1-gathered-expert-moe-combine`.
5. "Software Suite / TPC SDK kernel-authoring description" — the kernel path: `ref-tpc-sdk`, `playbook-tpc-customop-authoring`.
6. "PyTorch CustomOp API contract incl. single-kernel + custom_op namespace limits" — the integration contract: `fact-customop-single-kernel-contract`, `ref-pytorch-customop-api`.
7. "Gaudi 2 FP8 E4M3/E5M2 support; Gaudi 2 96GB/2.45TB/s; Gaudi 3 128GB/3.7TB/s/1.8PFlops FP8" — the hardware budget: `fact-gaudi2-fp8-dtype-support`, `fact-gaudi2-hbm-and-bandwidth`, `fact-gaudi3-reference-specs`.
8. "HCCL = Gaudi's NCCL emulation layer, includes Supported Collective Primitives + Testing/Benchmarking (index). Collectives incl. allreduce/allgather/reducescatter/all2all corroborated via search snippets." — the collective layer: `fact-hccl-includes-all2all`, `concept-hccl-collective-layer`.

## Author inference flagged

1. "P3->P4 dependency ordering (single-kernel + namespace gate compile capture) - reading of contract, not stated by Intel" — `hyp-customop-gates-compile-capture`, `cust-phase-p4-capture`: an ordering bet, not a vendor rule.
2. "Residual Gaudi 2 FP8 throughput concern (existence confirmed; throughput unverified)" — `hyp-gaudi2-fp8-mme-throughput-gap`, `cust-risk-r1-fp8-mme-throughput`: R1 is performance, not feasibility.
3. "'P4 pin check before heavy P3' ordering = judgment on leverage, not a source claim" — `decision-pin-check-before-kernels`, `cust-phase-p4-pin-check`: sequencing advice, cap 0.65.
4. "HCCL Supported_Primitives authoritative table returned 404 under 'latest'; all2all-existence is corroborated by secondary search snippets, NOT the primitives table itself. Per-primitive dtype/topology caveats UNVERIFIED. Re-read on the v1.24.2 path if it matters to P5." — `question-hccl-primitive-caveats`, `cust-risk-r6-hccl-all2all-bandwidth`: existence is not throughput.

The block holds eight `evidence_grounded` items, four flagged inferences; item 7 bundles three hardware claims.
