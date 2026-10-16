---
id: task-p0-1-load-fp8-on-eager
title: "Load the FP8 Checkpoint on Gaudi 2 Eager"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Load Qwen3.8-Flash-Next-FP8 on Gaudi 2 in eager mode and prove it produces deterministic single-token probes, without any re-quantization fork."
auto_inject: false
applicable_when: "P0, immediately after the target stack (suite 1.24.2, plugin 0.30.0) is installed and the flags in task-p0-4 are set"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the FP8 checkpoint fails to load on Gaudi 2 eager, or Gaudi 2 FP8 support turns out to exclude the checkpoint's quantization format, this task's premise is void"
tags: ["roadmap-task", "p0", "fp8", "checkpoint-loading", "gaudi-2"]
edges: [
  {"target": "cust-phase-p0-platform-gate", "type": "part_of", "weight": 0.9, "note": "First task of the gating phase; nothing downstream starts until this load succeeds"},
  {"target": "fact-gaudi2-fp8-dtype-support", "type": "depends_on", "weight": 0.9, "note": "The task assumes E4M3/E5M2 support on Gaudi 2; that support is the reason no re-quantization fork is needed"},
  {"target": "decision-fp8-no-requantization", "type": "related_to", "weight": 0.85, "note": "Executes the decision to serve the FP8 weights directly rather than re-expressing them"},
  {"target": "task-p0-4-set-required-flags", "type": "depends_on", "weight": 0.7, "note": "The load run needs the required flag set, including --language-model-only and VLLM_SKIP_WARMUP"},
  {"target": "source-roadmap-qwen4-exp-gaudi2-v1-1", "type": "derived_from", "weight": 0.9, "note": "Task text comes from the roadmap P0.1 entry"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[fact-gaudi2-fp8-dtype-support]]"]
source_url: "Empty"
---

# Load the FP8 Checkpoint on Gaudi 2 Eager

Load the Qwen3.8-Flash-Next-FP8 checkpoint on Gaudi 2 with eager execution and confirm it runs. Gaudi 2 supports FP8 in both E4M3 and E5M2, so the checkpoint's quantization format is expected to load as-is — this task exists to confirm that on real hardware, not to author a conversion path.

Why it matters: it is the cheapest possible test of the whole plan's central assumption. Every later phase assumes FP8 is a live runtime path on this card. If the load succeeds and the probes are stable, the re-quantization fork stays closed and P1's reuse strategy is unobstructed. If it fails, the failure is far cheaper to absorb here than after kernel authoring.

Run it eager-only, with `--enforce-eager`, so no compile variable contaminates the result. Feed short, repeated prompts and check that single-token probes are deterministic across runs — non-determinism at this stage means a numerics or caching problem, not a performance problem, and it must be understood before anything is benchmarked.

Done when: the FP8 checkpoint loads on Gaudi 2 eager and produces deterministic single-token probes.
