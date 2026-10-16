---
id: task-p3-1-sparse-topk-kernel
title: Single CustomOp for Sparse Top-k / QSA Indexer
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Author one TPC CustomOp for the sparse top-k gather / QSA indexer; high graph-capture risk (data-dependent control flow); accepted only when byte-equal to eager on Gaudi 2.
auto_inject: false
applicable_when: P3 custom kernels is active on the recommended order — P1 exit criterion met and the P4 pin check (P4.1-P4.2) already run
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a native vllm-gaudi or Intel kernel for sparse top-k / QSA indexer selection ships, or the byte-equality acceptance rule is relaxed, this authoring task is obsolete or wrongly specified"
tags: ["roadmap-task", "p3", "custom-op", "tpc", "sparse-topk", "qsa-indexer", "graph-capture"]
edges: [
  {"target": "cust-phase-p3-custom-kernels", "type": "part_of", "weight": 0.9, "note": "P3 primitive P3.sparse_topk; one of the three CustomOp kernels replacing eager fallbacks"},
  {"target": "concept-qsa-indexer", "type": "depends_on", "weight": 0.9, "note": "The kernel implements the indexer's sparse selection; the concept is its specification"},
  {"target": "hyp-sparse-topk-not-capturable", "type": "related_to", "weight": 0.9, "note": "Whether a single CustomOp captures is decided here; the hypothesis expects data-dependent control flow to defeat capture"},
  {"target": "cust-risk-r3-sparse-topk-uncapturable", "type": "related_to", "weight": 0.9, "note": "This is the kernel R3 is about; mitigation if uncapturable is hybrid compiled+eager for the QSA region only"},
  {"target": "playbook-tpc-customop-authoring", "type": "depends_on", "weight": 0.9, "note": "Follows the TPC CustomOp authoring procedure end to end"},
  {"target": "fact-customop-single-kernel-contract", "type": "depends_on", "weight": 0.9, "note": "Hard limits bind here: one TPC kernel per descriptor and custom_op namespace registration, or P4 capture stays blocked"}
]
related: ["[[concept-qsa-indexer]]", "[[playbook-tpc-customop-authoring]]", "[[cust-risk-r3-sparse-topk-uncapturable]]", "[[task-p4-5-meet-customop-capture-contract]]"]
source_url: "Empty"
---
# Single CustomOp for Sparse Top-k / QSA Indexer

Replace the eager fallback for sparse top-k gather / QSA indexer with one TPC CustomOp per the integration contract: kernel body in TPC-C via the TPC SDK, registerUserCustomOp with schema, tpc_guid and OutputMetaFn, TORCH_LIBRARY with HPU dispatch and a Meta impl, registered in the custom_op namespace. No public Intel primitive roadmap covers this — it is in our control. Graph-capture risk for this primitive is high: data-dependent control flow, the worst of the three. Acceptance is byte-equality: the CustomOp must be byte-equal to the eager reference on Gaudi 2; a faster non-matching kernel is a bug, not an optimisation. Done when: this primitive is a single CustomOp byte-equal to eager on Gaudi 2 and per-step dispatch count drops versus eager.
