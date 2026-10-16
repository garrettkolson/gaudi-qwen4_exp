---
id: concept-graph-capture-vs-eager
title: Eager Execution vs HPU Graph Capture
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Eager dispatches per operator and is the correctness baseline; captured HPU graphs replay per shape bucket but require static shapes and control flow.
auto_inject: false
applicable_when: When deciding whether a subgraph may leave --enforce-eager, or when reading a synapse compileGraph failure
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If boot without --enforce-eager succeeds on all four TP workers after the pin check, the eager-first framing becomes history and only the data-dependent-region caveat survives"
tags: ["graph-capture", "eager", "synapse", "shape-bucketing", "host-coercion", "dispatch-overhead"]
edges: [
  {"target": "task-p4-2-boot-without-enforce-eager", "type": "related_to", "weight": 0.9, "note": "P4.2 is the experiment that turns this distinction into a documented list of subgraphs that still fail capture"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.9, "note": "synStatus-26 from synapse compileGraph is the concrete failure signature of crossing this boundary too early"},
  {"target": "task-p0-4-set-required-flags", "type": "related_to", "weight": 0.8, "note": "--enforce-eager is one of the P0 flags, chosen precisely so the baseline is the mode whose semantics are guaranteed"},
  {"target": "concept-qsa-indexer", "type": "related_to", "weight": 0.8, "note": "The QSA region is the named case where data-dependent flow may make capture impossible rather than merely awkward"},
  {"target": "decision-eager-first-compiled-later", "type": "related_to", "weight": 0.9, "note": "That decision fixes the ordering this node explains: eager is the byte-equality reference, capture is the later lever"}
]
related: ["[[task-p4-2-boot-without-enforce-eager]]", "[[ref-issue-1734-synstatus-26]]", "[[concept-qsa-indexer]]", "[[decision-eager-first-compiled-later]]"]
source_url: "Empty"
---

# Eager Execution vs HPU Graph Capture

In eager mode every operator is dispatched to the device when Python reaches it. Shapes and control flow may vary per step; the price is a per-operator launch on top of a usually small amount of work. In compiled mode the step is recorded once per shape bucket into an HPU graph through synapse and replayed thereafter, which removes per-operator launch overhead — the dominant lever at decode, where a step is many short kernels and little arithmetic.

The trade is that a captured graph is a static artefact. Shapes and control flow must be settled at capture time, so anything that carries a device value into host control flow — `.item()`, `.nonzero`, boolean coercion of a tensor, a length read from a mask — synchronises the device and ends the recording. Captured graphs also pin the buffers they reference, so each bucket reserves memory, which interacts directly with a KV pool sized from measured free HBM on a 96 GB card.

For this port the split is a plan decision, not a preference. `--enforce-eager` is the P0 baseline because eager is the byte-equality reference every kernel is judged against, and capture is the later speed lever. The known blocker is synapse `compileGraph` synStatus-26, issue #1734, addressed for GDN hybrids by upstream pin `c05d75a`, with PR #1843 carrying further mitigations. Where a region genuinely requires data-dependent flow, the accepted outcome is a documented per-subgraph eager fallback rather than a compiler fix.
