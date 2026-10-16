---
id: concept-gdn-gated-delta-net
title: Gated DeltaNet (GDN) Linear-Attention State
type: concept
namespace: qwen4-exp-gaudi2
visibility: public
summary: Linear-attention block carrying a fixed-size gated delta-rule state instead of growing KV; reused from the plugin, and the subgraph behind the #1734 capture failure.
auto_inject: false
applicable_when: When touching GDN attention layers, mamba-style cache groups, or layer-boundary sequence parallelism
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the build pin falls behind c05d75a, or a GDN layer boundary fails capture again on Gaudi 2, the assumption that the pin fix removed this class of failure no longer holds"
tags: ["gdn", "linear-attention", "recurrent-state", "sequence-parallel", "graph-capture"]
edges: [
  {"target": "fact-model-architecture-blocks", "type": "related_to", "weight": 0.9, "note": "That fact carries the GDN head geometry this node explains: 48 value heads, 16 QK heads, 128 head dim"},
  {"target": "task-p1-1-port-qwen4-exp-model", "type": "related_to", "weight": 0.85, "note": "P1.1 reuses HPUGatedDeltaNetAttention rather than re-deriving the block, so this node is the reading aid for that reuse"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.8, "note": "The synStatus-26 compileGraph failures were reported on GDN hybrids, which is why GDN is a capture suspect"},
  {"target": "concept-kv-block-ownership", "type": "related_to", "weight": 0.7, "note": "GDN state is mutated in place, so it needs cache-group handling rather than append-only KV block semantics"},
  {"target": "fact-pin-c05d75a-resolves-1734", "type": "depends_on", "weight": 0.7, "note": "The claim that GDN layer boundaries capture cleanly rests on this pin being present in the build"}
]
related: ["[[fact-model-architecture-blocks]]", "[[concept-kv-block-ownership]]", "[[ref-issue-1734-synstatus-26]]", "[[task-p1-1-port-qwen4-exp-model]]"]
source_url: "Empty"
---

# Gated DeltaNet (GDN) Linear-Attention State

Gated DeltaNet is a linear-attention recurrent block. Instead of appending a key and value per token, each layer keeps a fixed-size matrix state updated once per token. The update is a delta rule: the state is read along the current key direction, the difference between that read-out and the incoming value is written back, and a data-dependent gate decays the state so older associations fade. Cost per token is constant and state size does not grow with context length, which is what makes a hybrid model with only a few softmax layers affordable.

In this port the block is reused, not re-authored: PR #1829 builds on the plugin's `HPUGatedDeltaNetAttention` with 48 value heads, 16 QK heads and 128-dimensional heads. The consequence for the runner is that GDN state is not append-only KV. It is a mutable per-sequence state, which is why the architecture has to be registered as mamba-like in `maybe_set_mamba_kv_cache_groups_ids` to get its own cache-group handling, and why its state cannot be treated as a shareable immutable prefix.

The failure mode it explains is capture, not arithmetic. GDN hybrids were the family hit by synapse `compileGraph` synStatus-26 in issue #1734, where sequence-parallel boundaries split a layer's state handoff. Upstream pin `c05d75a` — keep Qwen3Next layer boundaries sequence parallel — resolved that with no plugin change, which is exactly why the cheap pin check is scheduled before heavy kernel authoring.
