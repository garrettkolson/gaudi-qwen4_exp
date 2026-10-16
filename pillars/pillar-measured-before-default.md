---
id: pillar-measured-before-default
title: Topology and Limits Come From Measured Numbers
type: pillar
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Topology and limits are set by numbers measured on the 4x Gaudi 2 box; the Gaudi 3 reference config (TP4, 0.80 util, 128GB) is a starting hypothesis, never a target.
auto_inject: false
applicable_when: When choosing TP degree, max-model-len, memory-utilization, or whether to adopt expert-parallelism for the 4x Gaudi 2 target
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If P0 measurements show the Gaudi 3 reference numbers (TP4, 0.80 util, 128GB) already fit 4x Gaudi 2 unchanged, the re-derivation this pillar demands is unnecessary"
tags: ["strategy", "measured-numbers", "topology", "gaudi-2", "memory-planning"]
edges: [
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Roadmap P0.3/P0.5 require re-deriving TP, max-model-len and util, and measuring HCCL collectives before fixing topology"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.9, "note": "P0 is where this pillar is executed: its exit criteria are all measured, not inherited"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.8, "note": "P5.3 treats higher TP/EP as a measured decision gated on P0.5 all2all bandwidth, not a default lever"},
  {"target": "decision-tp-ep-measured-not-default", "type": "supports", "weight": 0.9, "note": "This pillar is the strategic ground for that decision: the decision inherits its 'measure first' rule"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[decision-tp-ep-measured-not-default]]", "[[fact-gaudi2-hbm-and-bandwidth]]"]
source_url: "Empty"
---

# Topology and Limits Come From Measured Numbers

**Principle.** PR #1829 was built for Gaudi 3: 128GB at 3.7 TB/s, TP4, 0.80 memory-utilization. This target is 4x Gaudi 2 at 96GB HBM2E and 2.45 TB/s per card. Every inherited number — TP degree, `--max-model-len`, `--gpu-memory-utilization`, and any move to expert-parallelism — is a starting hypothesis that only a measurement on this box can promote to a target.

**What this rules out.** Copying the Gaudi 3 config and hoping it fits 96GB. Treating the existence of an HCCL primitive as feasibility: expert-parallel MoE is an all-to-all dispatch/combine pattern over the interconnect, so its viability depends on measured all2all throughput on the Gaudi 2 fabric (24x100 Gbps on-chip RoCE), not on the primitive being listed in documentation.

**What it forces under time pressure.** Deadlines make inherited defaults tempting. This pillar forces the cheaper order anyway: re-derive TP and sizing (P0.3) and benchmark allreduce/allgather/all2all (P0.5) before any topology-dependent work commits. A config that ships late and measured beats a config that ships on time from someone else's hardware and OOMs at concurrency 8.
