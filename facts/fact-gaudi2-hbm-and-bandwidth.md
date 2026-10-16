---
id: fact-gaudi2-hbm-and-bandwidth
title: Gaudi 2 Has 96GB HBM2E at 2.45 TB/s per Card
type: fact
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: Gaudi 2: 96GB HBM2E @ 2.45 TB/s per card, on-chip 24x100 Gbps RoCE, 4 cards in target. TP degree and context length must be derived from these numbers, not Gaudi 3 defaults.
auto_inject: false
applicable_when: "Empty"
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a Gaudi 2 SKU or HBM firmware revision reports HBM capacity or bandwidth other than 96GB HBM2E @ 2.45 TB/s, or a RoCE link report shows fewer than 24x100 Gbps lanes, re-derive the memory plan"
tags: ["gaudi-2", "hbm", "memory-bandwidth", "roce", "hardware-spec"]
edges: [
  {"target": "source-gaudi2-spec-sheets", "type": "derived_from", "weight": 0.9, "note": "Capacity, bandwidth, and RoCE lanes come from the Gaudi 2 hardware specification sources"},
  {"target": "fact-gaudi3-reference-specs", "type": "related_to", "weight": 0.8, "note": "96GB/2.45TB/s is the smaller target that Gaudi 3's 128GB/3.7TB/s reference does not transfer to"},
  {"target": "decision-tp-ep-measured-not-default", "type": "supports", "weight": 0.8, "note": "The 96GB budget is the constraint that forces TP/EP to be measured rather than copied from the TP4 reference"},
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.85, "note": "P0 sizes HBM and TP directly from the 96GB / 2.45 TB/s figures"}
]
related: ["[[fact-gaudi3-reference-specs]]", "[[task-p0-3-resize-tp-and-memory]]", "[[cust-risk-r2-hbm-side-cache-pressure]]"]
source_url: "Empty"
---

# Gaudi 2 Has 96GB HBM2E at 2.45 TB/s per Card

Each Gaudi 2 accelerator in this target carries 96GB of HBM2E with 2.45 TB/s of memory bandwidth, and exposes on-chip 24x100 Gbps RoCE for inter-card traffic. The serving target is 4 such cards. These figures are stated in the roadmap's `target_stack` (`gaudi2_hbm: "96 GB HBM2E @ 2.45 TB/s per card"`) and the P0.5 task note ("Gaudi 2: 2.4 TB/s HBM, on-chip 24x100 Gbps RoCE"), and are corroborated by Intel's Gaudi 2 hardware specification sheets. They are externally checkable, so confidence is high.

The number is load-bearing because PR #1829 was built against Gaudi 3's 128GB / 3.7 TB/s; its TP4 and 0.80 memory-utilization settings were chosen for that larger, faster budget and cannot be assumed to fit here. This node states what is known about capacity and bandwidth per card; it does NOT establish that any particular TP degree, max-model-len, or memory-utilization actually fits, nor the achievable allreduce/all2all throughput on the RoCE fabric — those are measurement outcomes for P0.3 and P0.5, not hardware specs. No measurement on this 4-card box has been taken, so `verified_at` is Empty.
