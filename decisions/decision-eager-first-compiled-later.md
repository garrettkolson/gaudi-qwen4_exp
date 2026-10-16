---
id: decision-eager-first-compiled-later
title: Serve Eager-First, Remove --enforce-eager Only After Capture Work
type: decision
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Eager is the correctness baseline and byte-equality reference; --enforce-eager is removed only via P4 capture work, ending at compiled mode or a documented hybrid for the QSA indexer.
auto_inject: false
applicable_when: When choosing execution mode for a run, or when removing --enforce-eager is proposed before P4 capture work is done
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P4.2 shows a Gaudi 2 boot without --enforce-eager succeeds out of the box after the c05d75a pin, the eager-first staging can be compressed"
tags: ["decision", "eager", "graph-capture", "execution-mode", "p4"]
edges: [
  {"target": "concept-graph-capture-vs-eager", "type": "depends_on", "weight": 0.9, "note": "The decision presumes the distinction: eager dispatches op-by-op, HPU graph capture replays a compiled graph, with different failure modes"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.85, "note": "P0.4 sets --enforce-eager as a required flag from the first boot, instantiating the eager baseline"},
  {"target": "cust-phase-p4-capture", "type": "related_to", "weight": 0.9, "note": "P4b is the authorized path off eager: PR #1843 mitigations, host-coercing op removal, CustomOp capture contract"},
  {"target": "ref-issue-1734-synstatus-26", "type": "related_to", "weight": 0.75, "note": "The known blocker behind the staging: synStatus-26 / synapse compileGraph, the issue #1734 family"}
]
related: ["[[concept-graph-capture-vs-eager]]", "[[cust-phase-p4-capture]]", "[[ref-issue-1734-synstatus-26]]", "[[pillar-correctness-gates-speed]]"]
source_url: "Empty"
---

# Serve Eager-First, Remove --enforce-eager Only After Capture Work

## Context

Gaudi 2 execution has two modes here: eager, where ops dispatch individually, and compiled HPU-graph mode, which replays captured graphs but has a known blocker in synStatus-26 / synapse `compileGraph` (issue #1734 family), only partially resolved upstream by pin `c05d75a`. Meanwhile P3 needs a stable reference to check byte-equality against, and P0.4 lists `--enforce-eager` among the required runtime flags alongside `--kv-cache-dtype auto`, `VLLM_SKIP_WARMUP=true` and `--language-model-only`.

## Alternatives considered

Compiled-first: chase capture speed before a correct eager forward exists. Eager-only forever: forfeit the dispatch-overhead savings graph capture buys, especially for the MoE-heavy decode path where issue #1733 low-batch slowness already hurts.

## Decision

Serve eager first. Eager mode is the correctness baseline and the byte-equality reference for every P3 CustomOp. Remove `--enforce-eager` only through the P4 sequence: pin check first, then capture work integrating PR #1843 mitigations and eliminating host-coercing ops in QSA/PLE hot paths.

## Consequence

P1, P2 and P3 all validate on eager, giving one trustworthy reference. P4b's exit is compiled mode on all TP workers, or a documented hybrid keeping eager only for the QSA indexer — speed arrives without ever losing the correctness anchor.
