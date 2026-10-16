---
id: source-gaudi2-spec-sheets
title: Gaudi 2 Hardware Specification Sources
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "Gaudi 2 datasheet claims the roadmap relies on: 96 GB HBM2E at 2.45 TB/s per card, 24x100 Gbps RoCE, FP8 E4M3 and E5M2. Capability stated; per-card FP8 rate is not."
auto_inject: false
applicable_when: "When sizing TP degree, context length or memory utilization for this 4-card box, or when a spec-derived number is quoted as if measured"
confidence: 0.9
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If vendor documentation for suite 1.24.2 states different HBM capacity, bandwidth, RoCE lanes or FP8 formats for Gaudi 2, or a P0 measurement contradicts the published figures, the facts derived here change"
tags: ["gaudi-2", "hardware-spec", "hbm", "fp8", "roce", "capacity"]
edges: [
  {"target": "fact-gaudi2-hbm-and-bandwidth", "type": "supports", "weight": 0.9, "note": "96 GB HBM2E at 2.45 TB/s per card and 24x100 Gbps RoCE are read directly from these spec sources"},
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "supports", "weight": 0.9, "note": "FP8 E4M3 and E5M2 support is a published capability claim; these sheets are its only basis in the vault"},
  {"target": "pillar-measured-before-default", "type": "related_to", "weight": 0.6, "note": "Spec sheets bound the design but are not measurements on this box — the pillar exists to keep that distinction"}
]
related: ["[[fact-gaudi2-hbm-and-bandwidth]]", "[[fact-gaudi2-fp8-dtype-support]]", "[[task-p0-3-resize-tp-and-memory]]", "[[fact-gaudi3-reference-specs]]"]
source_url: "Empty"
---
# Gaudi 2 Hardware Specification Sources

Vendor hardware documentation for the accelerator this project targets. The figures the roadmap takes from them: 96 GB HBM2E per card at 2.45 TB/s, on-chip 24x100 Gbps RoCE, and FP8 support in both E4M3 and E5M2 — against Gaudi 3's 128 GB / 3.7 TB/s / 1.8 PFlops FP8, which is the comparison point PR #1829 was built against. The roadmap lists these in `evidence_grounded`.

They are the basis of `fact-gaudi2-hbm-and-bandwidth` and `fact-gaudi2-fp8-dtype-support`, and through those the P0 sizing tasks, the FP8 no-re-quantization decision, and the R2 HBM pressure risk. `hyp-gaudi2-fp8-mme-throughput-gap` exists precisely because the spec sheet states FP8 capability without a Gaudi 2 PFlops figure to compare.

Currency: published datasheet values, stable across suite versions; not a measurement of this specific 4-card box. The roadmap cites no URL for these sheets, so none is recorded here — re-read the vendor spec page for Gaudi 2 before quoting the numbers as verified.
