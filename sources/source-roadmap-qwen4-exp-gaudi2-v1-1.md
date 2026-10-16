---
id: source-roadmap-qwen4-exp-gaudi2-v1-1
title: Roadmap JSON v1.1 (qwen4_exp on Gaudi 2)
type: source
namespace: qwen4-exp-gaudi2
visibility: public
summary: "Seeded origin of this vault: roadmap v1.1 (schema 1.1) for serving Qwen3.8-Flash-Next on 4x Gaudi 2 via vllm-gaudi; immutable copy in raw/processed, human owns the root working copy."
auto_inject: false
applicable_when: "When checking where a seeded claim came from, or before re-seeding after a roadmap version bump"
confidence: 0.95
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If a dated copy of a roadmap with schema newer than 1.1 lands in raw/processed/, or the root working copy diverges from this copy on its provenance lists, every derived node needs re-seeding"
tags: ["roadmap", "source", "provenance", "gaudi-2", "vllm-gaudi", "seed-origin"]
edges: [
  {"target": "cust-phase-p0-platform-gate", "type": "related_to", "weight": 0.9, "note": "P0 is the roadmap's declared gating phase; its exit criteria are quoted from this document"},
  {"target": "note-provenance-register", "type": "related_to", "weight": 0.9, "note": "The roadmap's provenance block splits evidence_grounded from author_inference_flagged; the register carries it verbatim"},
  {"target": "event-2026-10-15-roadmap-baseline-v1-1", "type": "related_to", "weight": 0.8, "note": "The baseline event adopts this exact file version as the plan of record"}
]
related: ["[[note-provenance-register]]", "[[event-2026-10-15-roadmap-baseline-v1-1]]", "[[cust-phase-p0-platform-gate]]"]
source_url: "Empty"
---
# Roadmap JSON v1.1 (qwen4_exp on Gaudi 2)

The origin document of this vault: `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json`, schema version 1.1, `generated_for: agent-execution`. It fixes the target stack (Gaudi software suite 1.24.2, PyTorch 2.13, vllm-gaudi plugin 0.30.0, upstream vLLM 0.30.0 pinned at/after `c05d75a`, 4x Gaudi 2 at 96 GB HBM2E @ 2.45 TB/s, FP8 E4M3 and E5M2), defines eight phases P0–P6 with their tasks and exit criteria, six risks with probability, impact and mitigation, a recommended execution order (P0 → P1 → P4_pin_check → P3 → P4_capture → P5, P0 gating), and a `provenance` block separating `evidence_grounded` from `author_inference_flagged`.

Every seeded node here descends from it: the phase, risk, task, decision, fact, hypothesis and provenance nodes cite it as their grounding. The live working copy is `qwen4_exp_gaudi2_roadmap.json` at the repository root, owned by the human; the vault reads the immutable copy above and edits neither. Currency: 2026-10-15, superseded only by a dated copy of a higher schema version.
