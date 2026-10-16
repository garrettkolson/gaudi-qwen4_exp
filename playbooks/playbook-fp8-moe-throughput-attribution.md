---
id: playbook-fp8-moe-throughput-attribution
title: "Attributing MoE Throughput Changes to One Lever"
type: playbook
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Pre-register the throughput protocol before each P5 lever, change one thing, re-run, and record cost-per-token deltas so each gain is attributable to a named lever."
auto_inject: false
applicable_when: "When applying any P5 throughput lever on Gaudi 2 — gathered-expert MoE combine, decode bucketing, or a TP/EP change — and the result has to be credited to that lever"
confidence: 0.8
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the throughput protocol stops mirroring PR seeds 301-303, or a baseline run repeats outside its recorded noise floor, the comparison method here no longer holds"
tags: ["playbook", "p5", "moe", "throughput", "attribution", "benchmark"]
edges: [
  {"target": "task-p5-2-preregister-throughput-protocol", "type": "depends_on", "weight": 0.95, "note": "Pre-registration is the task that makes this procedure possible — without it, step 5 attributes nothing"},
  {"target": "cust-phase-p5-moe-economics", "type": "related_to", "weight": 0.9, "note": "P5's exit is a documented cost-per-token curve with an identified saturation point, which is what this runbook produces"},
  {"target": "pillar-measured-before-default", "type": "related_to", "weight": 0.85, "note": "Every claim in the resulting curve traces to a number measured on this 4-card box, not inherited from the Gaudi 3 port"},
  {"target": "question-moe-saturation-point", "type": "related_to", "weight": 0.85, "note": "The open question step 6 answers: where cost-per-token stops falling as concurrency climbs"},
  {"target": "task-p5-1-gathered-expert-moe-combine", "type": "related_to", "weight": 0.8, "note": "A typical single lever — the opt-in FP8 gathered-expert combine is measured before and after, never bundled with another change"}
]
related: ["[[task-p5-3-tune-bucketing-and-tp-ep]]", "[[cust-risk-r4-1733-lowbatch-moe]]", "[[cust-phase-p5-moe-economics]]", "[[pillar-measured-before-default]]"]
source_url: "Empty"
---

# Attributing MoE Throughput Changes to One Lever

The failure mode in P5 is a speedup nobody can explain — a config changed in three places at once, so no later decision can reuse it. This procedure keeps each gain tied to one named lever.

1. **Pre-register the throughput protocol before touching anything**, mirroring PR seeds 301-303: workload, concurrency ladder from 1 to target, seeds, and the metric — cost per token. *Check:* the protocol exists as a dated artifact before the first post-lever run. A protocol written after the results is not a protocol.
2. **Take the baseline under that protocol.** *Check:* a repeat lands inside a stated spread at each concurrency point; that spread is the noise floor, and a later delta smaller than it is not a result.
3. **Apply exactly one lever.** Gathered-expert MoE combine for FP8 is one lever; decode bucketing is another; a TP or EP change is a third, available only if P0.5's measured all2all bandwidth supports it. *Check:* the config diff contains that lever and nothing else.
4. **Re-run the identical protocol on the changed build.** *Check:* same seeds, ladder and workload as step 1, so the comparison is like for like.
5. **Attribute the delta.** *Check:* the claim states the baseline and post-lever number for the same concurrency point from the same protocol, and the difference clears the step-2 noise floor. Anything that does not is recorded as no measurable effect, not as a win.
6. **Write the result into the graph.** *Check:* the number lands in a `fact-*` node, and the hypotheses and risks hanging off it update through their edges.
7. **Repeat per lever, then read the curve.** *Check:* a cost-per-token curve across concurrency 1 to target with the saturation point named — where cost per token stops falling — which answers the saturation question.

## Stop and escalate

Stop and report when: a config diff carries more than one lever, making the run unattributable and forcing it to be re-run split; the noise floor swallows the effect at every concurrency point, the R4 signature of #1733 low-batch slowness dominating end-to-end throughput; a TP or EP increase is proposed while P0.5's all2all measurement is absent, since higher parallelism is a measured decision, not a default lever; or the protocol is being edited after results were seen, which invalidates the comparison and is reported, not done quietly.
