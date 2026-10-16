---
id: task-p3-2-ple-dilated-conv-kernel
title: Single CustomOp for PLE Dilated Short-Conv
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Author one TPC CustomOp for the PLE dilated short-conv; medium graph-capture risk; accepted only when byte-equal to the eager reference on Gaudi 2.
auto_inject: false
applicable_when: P3 custom kernels is active on the recommended order — P1 exit criterion met and the P4 pin check (P4.1-P4.2) already run
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If plugin v0.30.0's TPC-native causal_conv1d lineage exactly covers the PLE dilated short-conv, this task shrinks to adoption plus the byte-equality check instead of kernel authoring"
tags: ["roadmap-task", "p3", "custom-op", "tpc", "ple", "dilated-conv"]
edges: [
  {"target": "cust-phase-p3-custom-kernels", "type": "part_of", "weight": 0.9, "note": "P3 primitive P3.ple_conv; the dilated short-conv CustomOp of the three-primitive phase"},
  {"target": "concept-ple-dilated-conv-ngram", "type": "depends_on", "weight": 0.9, "note": "The kernel implements the PLE dilated short-conv and its carried state; the concept is its specification"},
  {"target": "playbook-tpc-customop-authoring", "type": "depends_on", "weight": 0.85, "note": "Same authoring procedure as the other two primitives"},
  {"target": "fact-plugin-0-30-0-features", "type": "related_to", "weight": 0.7, "note": "Release lineage ships TPC-native causal_conv1d — check reuse before authoring a new kernel"},
  {"target": "task-p4-4-eliminate-host-coercing-ops", "type": "followed_by", "weight": 0.7, "note": "P4.4 afterwards removes host-coercing ops in the PLE hot path, such as .nonzero in _pool_and_store"}
]
related: ["[[concept-ple-dilated-conv-ngram]]", "[[playbook-tpc-customop-authoring]]", "[[task-p4-4-eliminate-host-coercing-ops]]"]
source_url: "Empty"
---
# Single CustomOp for PLE Dilated Short-Conv

Author one TPC CustomOp for the PLE dilated short-conv, replacing the eager fallback: kernel body in TPC-C via the TPC SDK, registered with registerUserCustomOp under the custom_op namespace with a Meta impl, one TPC kernel per descriptor — a multi-op Python decomposition would recreate the eager dispatch cost the phase removes. Plugin v0.30.0's release lineage includes TPC-native causal_conv1d, so check reuse before authoring. Graph-capture risk for this primitive is medium. Acceptance is byte-equality: output must be byte-equal to the eager reference on Gaudi 2; speed is judged only after correctness. Done when: this primitive is a single CustomOp byte-equal to eager on Gaudi 2 and per-step dispatch count drops versus eager.
