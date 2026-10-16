---
id: task-p0-4-set-required-flags
title: "Set the Required Runtime Flags"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Fix the P0 runtime flag set: --kv-cache-dtype auto, VLLM_SKIP_WARMUP=true, --enforce-eager and --language-model-only, applied identically across all runs."
auto_inject: false
applicable_when: "P0, before the first checkpoint load, and re-checked before any P4 capture experiment changes the set"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "Once P4b removes --enforce-eager, this flag set is deliberately superseded; any P4 result recorded with the original set must be re-validated under the new one"
tags: ["roadmap-task", "p0", "configuration", "runtime-flags"]
edges: [
  {"target": "cust-phase-p0-platform-gate", "type": "part_of", "weight": 0.9, "note": "Small but load-bearing P0 task: every other P0 measurement depends on a consistent flag set"},
  {"target": "concept-graph-capture-vs-eager", "type": "depends_on", "weight": 0.7, "note": "--enforce-eager is the deliberate eager baseline that P4 later removes"},
  {"target": "fact-target-stack-versions", "type": "related_to", "weight": 0.7, "note": "Flag availability is version-dependent; the set is asserted for plugin 0.30.0 on suite 1.24.2"},
  {"target": "task-p0-1-load-fp8-on-eager", "type": "related_to", "weight": 0.7, "note": "The checkpoint load runs with these flags, not with a default invocation"}
]
related: ["[[cust-phase-p0-platform-gate]]", "[[concept-graph-capture-vs-eager]]"]
source_url: "Empty"
---

# Set the Required Runtime Flags

Set and hold constant the flag set the roadmap requires for this enablement: `--kv-cache-dtype auto`, `VLLM_SKIP_WARMUP=true`, `--enforce-eager`, and `--language-model-only`.

Each flag is doing a specific job. `--kv-cache-dtype auto` lets the cache dtype follow what the stack can actually support rather than asserting one Gaudi 2 may not accept. `VLLM_SKIP_WARMUP=true` skips a warmup path that costs startup time and can fail before any real request runs. `--enforce-eager` keeps execution out of the compiler, which is where the synapse `compileGraph` failure family lives — during P0 the compiler is not the subject, so it stays out of the experiment. `--language-model-only` restricts the run to the language stack, matching the scope of the reference port, which excluded the vision tower.

Why it matters: P0 produces the numbers every later phase reasons from. If two runs in the same phase differ by an unstated flag, the difference is unreproducible and the phase's exit criteria are effectively unmeasured. Keep the set in one place, echo it in every benchmark record, and change exactly one flag at a time when P4 deliberately lifts the eager constraint.

Done when: the four flags are applied identically across P0 runs and recorded alongside every measurement produced by the phase.
