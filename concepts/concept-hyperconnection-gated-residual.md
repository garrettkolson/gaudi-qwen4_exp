---
id: concept-hyperconnection-gated-residual
title: "HyperConnection Gated Residual (`HpuGatedResidual`)"
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Multi-stream residual with learned input-dependent gates; trivially static math, but layer-boundary glue that appears in the #1734 capture family.
auto_inject: false
applicable_when: When triaging capture failures at layer boundaries, or counting per-block elementwise dispatch in eager mode
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a P4.2 boot without --enforce-eager shows HyperConnection regions capturing cleanly after the pin fix, this node's status as a capture suspect should be dropped"
tags: ["hyperconnection", "gated-residual", "layer-boundary", "eager-dispatch", "residual-stream"]
edges: [
  {"target": "fact-model-architecture-blocks", "type": "related_to", "weight": 0.85, "note": "Lists gated-residual HyperConnection as one of the five ported blocks, under the name HpuGatedResidual"},
  {"target": "task-p1-1-port-qwen4-exp-model", "type": "related_to", "weight": 0.8, "note": "P1.1 reuses the plugin's HpuGatedResidual, so this block arrives with the port rather than being authored in P3"},
  {"target": "concept-graph-capture-vs-eager", "type": "related_to", "weight": 0.6, "note": "Its gate chain is static in shape but is a long run of small kernels, which is an eager-dispatch cost rather than a capture blocker"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.7, "note": "The pin check targets capture for GDN and HyperConnection together, so this block is named as a suspect boundary"}
]
related: ["[[fact-model-architecture-blocks]]", "[[ref-issue-1734-synstatus-26]]", "[[concept-graph-capture-vs-eager]]", "[[task-p1-1-port-qwen4-exp-model]]"]
source_url: "Empty"
---

# HyperConnection Gated Residual (`HpuGatedResidual`)

HyperConnection generalises the additive residual stream. The residual becomes several parallel streams, and learned input-dependent coefficients decide how the sublayer output and the streams are recombined at each block: width-wise mixing across streams plus a gated depth-wise contribution. Against a plain `x + f(x)` it adds a handful of elementwise multiply and add ops and small gate computations per boundary, and it changes optimisation behaviour without touching the sublayers themselves.

In this port the boundary is implemented by the plugin's `HpuGatedResidual` and comes along with PR #1829; nothing in P3 has to be authored for it. What earns it a node is where it sits. It is the inter-block glue on the same path where GDN layer boundaries produced the synapse `compileGraph` synStatus-26 failures of the issue #1734 family — a boundary whose stream handoff was split by sequence parallelism, not a defect in the gate arithmetic. The upstream pin addressed that class of boundary.

The constraint it explains is dispatch cost. Gated-residual mixing is a chain of small elementwise kernels, so in eager decode every block pays per-op launch overhead on top of a small amount of work, across all layers and all four cards. That is why removing `--enforce-eager` is the throughput lever for this model, and why residual glue appears on P4 triage lists as a suspect even though its shapes are statically known.
