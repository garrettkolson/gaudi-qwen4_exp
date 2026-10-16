---
id: task-p3-3-fp8-ngram-gather-kernel
title: Single CustomOp for FP8 N-gram Gather-Then-Dequant
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Author one TPC CustomOp for FP8 n-gram gather-then-dequant, staying FP8 on Gaudi 2 MME; medium capture risk; byte-equality to eager is the acceptance rule.
auto_inject: false
applicable_when: P3 custom kernels is active on the recommended order — P1 exit criterion met and the P4 pin check (P4.1-P4.2) already run
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a re-quantization of the n-gram table to INT8 or BF16 is proposed, this task is wrongly specified — the roadmap pins this path to FP8 on Gaudi 2 MME with no re-expression fork"
tags: ["roadmap-task", "p3", "custom-op", "tpc", "fp8", "n-gram"]
edges: [
  {"target": "cust-phase-p3-custom-kernels", "type": "part_of", "weight": 0.9, "note": "P3 primitive P3.ple_ngram_fp8; the n-gram gather-then-dequant CustomOp of the three-primitive phase"},
  {"target": "concept-ple-dilated-conv-ngram", "type": "depends_on", "weight": 0.85, "note": "The kernel gathers over the n-gram embedding state the PLE concept defines"},
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "depends_on", "weight": 0.8, "note": "The design is pinned to FP8 because E4M3/E5M2 are supported on Gaudi 2 — no INT8 re-expression"},
  {"target": "playbook-tpc-customop-authoring", "type": "depends_on", "weight": 0.85, "note": "Same authoring procedure as the other two primitives"},
  {"target": "fact-customop-single-kernel-contract", "type": "depends_on", "weight": 0.85, "note": "One TPC kernel, custom_op namespace registration; gather and dequant must fuse into the single kernel body"}
]
related: ["[[concept-ple-dilated-conv-ngram]]", "[[fact-gaudi2-fp8-dtype-support]]", "[[decision-fp8-no-requantization]]"]
source_url: "Empty"
---
# Single CustomOp for FP8 N-gram Gather-Then-Dequant

Author one TPC CustomOp for the FP8 n-gram gather-then-dequant path. The primitive stays FP8 on Gaudi 2 MME — E4M3/E5M2 are supported and the roadmap rules out an INT8 re-expression fork — so the kernel gathers FP8 entries and dequantizes in-kernel rather than re-expressing the table. Follow the single-kernel contract: one TPC kernel via the TPC SDK, custom_op namespace registration, Meta impl for torch.compile. Graph-capture risk for this primitive is medium. Acceptance is byte-equality: output must be byte-equal to the eager reference on Gaudi 2 before it counts. Done when: this primitive is a single CustomOp byte-equal to eager on Gaudi 2 and per-step dispatch count drops versus eager.
