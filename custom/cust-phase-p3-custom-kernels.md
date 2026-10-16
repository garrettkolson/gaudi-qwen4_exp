---
id: cust-phase-p3-custom-kernels
title: "P3 — Custom Kernels for Three Hard Primitives (CustomOp/TPC)"
type: custom
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Replace eager fallbacks with fused TPC kernels for sparse top-k/QSA, PLE dilated conv and FP8 n-gram gather — each one CustomOp, byte-equal to eager on Gaudi 2."
auto_inject: false
applicable_when: "When executing roadmap phase P3, after P1 runs eagerly and the P4a pin check has been run"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a primitive cannot be expressed as a single TPC kernel without multi-op Python decomposition, or stays non-byte-equal to eager, re-scope this phase and the P4 capture plan"
tags: ["roadmap-phase", "p3", "custom-op", "tpc", "kernels", "capture-risk"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Phase transcribed from roadmap phases[].P3 — primitives, integration contract, exit criteria"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "depends_on", "weight": 0.9, "note": "Kernels replace the eager fallbacks P1 first makes correct — correctness gates speed"},
  {"target": "cust-phase-p4-pin-check", "type": "preceded_by", "weight": 0.8, "note": "Recommended order runs the cheap pin check (P4a) before this heavy kernel authoring"},
  {"target": "pillar-correctness-gates-speed", "type": "supports", "weight": 0.9, "note": "Byte-equality to the eager reference is the exit gate — a faster non-matching kernel is a bug generator"},
  {"target": "cust-risk-r3-sparse-topk-uncapturable", "type": "related_to", "weight": 0.9, "note": "The sparse top-k primitive carries high graph-capture risk (data-dependent control flow)"},
  {"target": "cust-risk-r5-no-intel-primitive-roadmap", "type": "related_to", "weight": 0.9, "note": "Confirmed risk: no public Intel roadmap — P3 is in our control via the TPC SDK and CustomOp contract"},
  {"target": "playbook-tpc-customop-authoring", "type": "related_to", "weight": 0.9, "note": "The authoring procedure each of the three kernels follows"},
  {"target": "concept-tpc-customop-integration", "type": "depends_on", "weight": 0.85, "note": "The integration path — TPC-C kernel, registerUserCustomOp, custom_op namespace — defines what a compliant kernel is"}
]
related: ["[[playbook-tpc-customop-authoring]]", "[[concept-tpc-customop-integration]]", "[[cust-risk-r5-no-intel-primitive-roadmap]]", "[[cust-phase-p4-pin-check]]"]
source_url: "Empty"
---

# P3 — Custom Kernels for Three Hard Primitives (CustomOp/TPC)

## Goal
Replace eager fallbacks with fused TPC kernels — in our control, not Intel-gated. Each primitive becomes one CustomOp via the PyTorch CustomOp API + TPC SDK: single TPC kernel per op (multi-op Python decomposition recreates eager dispatch cost) and custom_op namespace registration for full torch.compile support, which the roadmap reads as the gate for P4 capture.

## Depends on
P1 (eager fallbacks running and correct); recommended to run after the P4a pin check. Ordering: recommended sequence is P0 → P1 → P4_pin_check → P3 → P4_capture → P5, with the cheap pin check placed before heavy kernel authoring.

## Tasks
- [[task-p3-1-sparse-topk-kernel]] — single CustomOp for sparse top-k / QSA indexer; high capture risk from data-dependent control flow.
- [[task-p3-2-ple-dilated-conv-kernel]] — single CustomOp for the PLE dilated short-conv; medium capture risk.
- [[task-p3-3-fp8-ngram-gather-kernel]] — single CustomOp for FP8 n-gram gather-then-dequant; stays FP8 on Gaudi 2 MME, no INT8 re-expression.

## Exit criteria
Each primitive is a single CustomOp, byte-equal to the eager reference on Gaudi 2, and the per-step dispatch count drops versus eager.
