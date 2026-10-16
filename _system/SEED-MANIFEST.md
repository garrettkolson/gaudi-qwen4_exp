# Seed Manifest — Roadmap → Graph Mapping

Build artifact of the seed conversion of `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json` (schema 1.1) on 10/15/2026.

This file is the **id registry** for the vault. It exists so nodes written by different agents at different times wire to the same targets. If you add a node, add a row here first.

Namespace for every node below: `qwen4-exp-gaudi2`. Visibility: `namespace` unless stated. Filename is always `<id>.md`.

Edge notation: three items separated by `·` — a target id, an edge type, and a weight, optionally followed by `— reason`. Most rows read `target · type · weight`, some read `type · target · weight`. Read them as unordered triples: exactly one item is a legal edge type from `_system/EDGE-TYPES.md`, one is an id present in this file, one is the weight. Direction is always **the node owning the row → the target id**. `python _system/lint_vault.py` rejects any edge whose type is not one of the ten or whose target id does not exist, so a misread here fails loudly rather than silently.

---

## Confidence Policy (applies to every seeded node)

The roadmap splits its own provenance into `evidence_grounded` and `author_inference_flagged`. Seed confidence follows that split:

| Kind of claim | Confidence | Example |
|---|---|---|
| Stated in roadmap, externally checkable (specs, versions, PR contents) | 0.85–0.95 | `fact-gaudi2-hbm-and-bandwidth` |
| Stated in roadmap, corroborated by secondary sources only | 0.6–0.75 | `fact-hccl-includes-all2all` |
| Author inference flagged by the roadmap itself | 0.5–0.7 | `hyp-customop-gates-compile-capture` |
| Anything needing a Gaudi 2 measurement | ≤ 0.7 and `verified_at: "Empty"` | every `hyp-*` node |

Nothing seeded is `verified_at` — no claim in the roadmap has been measured on this hardware. `verified_by` for seeded nodes is `"Empty"`. Set `verified_by: "Roadmap v1.1"` nowhere; a document is not a verification.

---

## pillars/ (4)

| id | title | spec | edges |
|---|---|---|---|
| `pillar-measured-before-default` | Topology and Limits Come From Measured Numbers | Config inherited from the Gaudi 3 reference (TP4, 0.80 util, 128GB) is a starting hypothesis, never a target. TP degree, max-model-len, memory-utilization, and any move to expert-parallelism must come from numbers measured on the 4x Gaudi 2 box. | `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.9`; `cust-phase-p0-platform-gate · related_to · 0.9`; `cust-phase-p5-moe-economics · related_to · 0.8`; `decision-tp-ep-measured-not-default · supports · 0.9` (reverse: the decision is grounded here — express as `supports` from pillar) |
| `pillar-reuse-over-rederivation` | Reuse the Working Port, Do Not Re-Derive the Model | A working eager port exists in vllm-gaudi PR #1829 (~2.4k lines). Deriving Qwen3.8-Flash-Next from scratch on a new backend burns time on problems already solved; the work is retargeting, not authoring. | `source-vllm-gaudi-pr1829 · derived_from · 0.9`; `cust-phase-p1-reuse-pr1829 · related_to · 0.9`; `decision-reuse-pr1829-as-base · supports · 0.95` |
| `pillar-correctness-gates-speed` | Correctness Gates Speed | A kernel that is faster and not byte-equal to the eager reference is a bug generator, not an optimisation. Nothing counts as done until it matches eager; nothing is optimised before it is correct. | `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.8`; `cust-phase-p3-custom-kernels · related_to · 0.9`; `cust-phase-p5-moe-economics · related_to · 0.7` |
| `pillar-provenance-discipline` | Separate Evidence From Inference | The roadmap's value is that it labels which claims are sourced and which are its author's reading. An agent that flattens that distinction turns an inference into a constraint and plans around a wall that may not exist. | `note-provenance-register · related_to · 0.9`; `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.9`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.8` |

---

## custom/ — roadmap-phase (8)

All phases: `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.9`, tags include `roadmap-phase`, `visibility: namespace`, and body sections `Goal`, `Depends on`, `Tasks`, `Exit criteria`.

| id | title | spec | extra edges |
|---|---|---|---|
| `cust-phase-p0-platform-gate` | P0 — Platform Feasibility & Memory Planning (Gating) | Gating phase. Confirm FP8 is a real runtime path on Gaudi 2 and size HBM/TP correctly. Exit: FP8 checkpoint loads and gives deterministic single-token probes; a TP + max-model-len + util config fits without OOM; measured allreduce/allgather/all2all bandwidth recorded and TP/EP chosen from the numbers. | `pillar-measured-before-default · supports · 0.9`; `cust-phase-p1-reuse-pr1829 · followed_by · 0.9`; `cust-risk-r2-hbm-side-cache-pressure · related_to · 0.8`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.9`; `cust-risk-r1-fp8-mme-throughput · related_to · 0.8`; `question-what-tp-degree-fits-gaudi2 · related_to · 0.9` |
| `cust-phase-p1-reuse-pr1829` | P1 — Reuse PR #1829, Retarget to Gaudi 2 / Plugin 0.30.0 | Correct eager forward via reuse. Base on `vllm_gaudi/models/qwen4_exp.py`, register both model classes, retarget the pin from `dd3bc9c72faf` to plugin 0.30.0, carry the fp8 MoE block-grid fix, honour `modules_to_not_convert` and drop the `mtp.*` head. Exit: PR smoke battery (arithmetic, geography, code, needle retrieval) reproduces on Gaudi 2. | `depends_on · cust-phase-p0-platform-gate · 0.9`; `pillar-reuse-over-rederivation · supports · 0.95`; `cust-phase-p2-cache-plumbing · followed_by · 0.8`; `cust-phase-p3-custom-kernels · followed_by · 0.8`; `cust-phase-p4-pin-check · followed_by · 0.8` |
| `cust-phase-p2-cache-plumbing` | P2 — Cache & Memory Plumbing (HBM Fit + Prefix Caching) | Migrate module-allocated side caches (QSA raw-key ring, compressed-key side cache, PLE dilated-conv state, n-gram trailing-token history) onto scheduler-owned KV blocks; keep prefix caching off until that lands; confirm decode block buckets clamp to physical KV size. Exit: stable at concurrency 8+ without side-cache OOM. | `depends_on · cust-phase-p1-reuse-pr1829 · 0.9`; `cust-risk-r2-hbm-side-cache-pressure · related_to · 0.95`; `hyp-side-caches-oom-at-concurrency · related_to · 0.9`; `concept-kv-block-ownership · depends_on · 0.8`; `cust-phase-p5-moe-economics · related_to · 0.7` |
| `cust-phase-p3-custom-kernels` | P3 — Custom Kernels for Three Hard Primitives (CustomOp/TPC) | Replace eager fallbacks with fused TPC kernels for sparse top-k/QSA indexer (high capture risk), PLE dilated short-conv (medium), FP8 n-gram gather-then-dequant (medium, stays FP8 on Gaudi 2 MME). Not Intel-gated: in our control via CustomOp + TPC SDK. Exit: each primitive is a single CustomOp, byte-equal to eager on Gaudi 2; per-step dispatch count drops. | `depends_on · cust-phase-p1-reuse-pr1829 · 0.9`; `preceded_by · cust-phase-p4-pin-check · 0.8`; `pillar-correctness-gates-speed · supports · 0.9`; `cust-risk-r3-sparse-topk-uncapturable · related_to · 0.9`; `cust-risk-r5-no-intel-primitive-roadmap · related_to · 0.9`; `playbook-tpc-customop-authoring · related_to · 0.9`; `concept-tpc-customop-integration · depends_on · 0.85` |
| `cust-phase-p4-pin-check` | P4a — Cheap Graph-Capture Win (Pin Check Before Heavy P3) | Cheap check before expensive kernel authoring: verify the build pin is at/after `c05d75a` (which resolved synStatus-26 #1734 for GDN hybrids with no plugin change), then boot without `--enforce-eager` and record which subgraphs still fail. Exit: documented list of remaining capture-failing subgraphs. | `depends_on · cust-phase-p1-reuse-pr1829 · 0.9`; `fact-pin-c05d75a-resolves-1734 · derived_from · 0.9`; `decision-pin-check-before-kernels · supports · 0.9`; `question-which-subgraphs-fail-capture · related_to · 0.9`; `followed_by · cust-phase-p4-capture · 0.9` |
| `cust-phase-p4-capture` | P4b — Compiled (HPU-Graph) Mode: Off Eager-Only | Serve with `--enforce-eager` removed, or hybrid compiled+eager. Integrate PR #1843 mitigations (DS=0 concrete-plan recipe, host-side decode count fix, bmm score contraction fix, flat `index_copy_` store rewrite), eliminate host-coercing ops in QSA/PLE hot paths, ensure P3 CustomOps meet the capture contract. Known blocker: synStatus-26 / synapse `compileGraph` (#1734 family). Exit: boots/serves on all TP workers without `--enforce-eager`, or documented per-subgraph eager fallback for the QSA indexer only. | `depends_on · cust-phase-p4-pin-check · 0.9`; `depends_on · cust-phase-p3-custom-kernels · 0.7`; `ref-issue-1734-synstatus-26 · related_to · 0.9`; `hyp-customop-gates-compile-capture · related_to · 0.85`; `hyp-sparse-topk-not-capturable · related_to · 0.9`; `playbook-graph-capture-triage · related_to · 0.9`; `preceded_by · cust-phase-p4-pin-check · 0.9`; `followed_by · cust-phase-p5-moe-economics · 0.9` |
| `cust-phase-p5-moe-economics` | P5 — Throughput for Gaudi 2 MoE Economics | Usable serving speed given #1733 low-batch MoE slowness. Apply opt-in gathered-expert MoE combine for FP8, pre-register the throughput protocol (mirroring PR seeds 301-303) before/after each lever, tune decode bucketing with higher TP/EP as a measured decision gated on P0.5 all2all. Exit: documented cost-per-token curve across concurrency 1→target with an identified saturation point. | `depends_on · cust-phase-p4-capture · 0.9`; `depends_on · cust-phase-p2-cache-plumbing · 0.8`; `cust-risk-r4-1733-lowbatch-moe · related_to · 0.9`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.85`; `question-moe-saturation-point · related_to · 0.9`; `playbook-fp8-moe-throughput-attribution · related_to · 0.9`; `followed_by · cust-phase-p6-feature-parity · 0.7` |
| `cust-phase-p6-feature-parity` | P6 — Feature Parity (Deferred, Product-Driven) | Deferred, product-driven. HPU MTP drafter (only ngram/eagle/medusa exist today) or accept the dropped `mtp.*` head; vision tower for `ForConditionalGeneration` if multimodal is required; enable prefix caching with regression coverage after P2.1. Exit criteria are per-feature and not required for text-only serving enablement. | `depends_on · cust-phase-p5-moe-economics · 0.8`; `decision-defer-feature-parity-p6 · supports · 0.9`; `concept-mtp-speculative-decoding · depends_on · 0.8`; `question-mtp-drafter-on-hpu · related_to · 0.85`; `task-p6-3-enable-prefix-caching · related_to · 0.8` |

---

## custom/ — roadmap-risk (6)

All risks: `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.85`, tags include `roadmap-risk` and the probability. Body sections: `Exposure`, `Mitigation`, `Trigger to watch`.

| id | title | probability/impact | edges |
|---|---|---|---|
| `cust-risk-r1-fp8-mme-throughput` | R1 — Gaudi 2 FP8 MME Throughput Below Gaudi 3 | medium / medium | `hyp-gaudi2-fp8-mme-throughput-gap · depends_on · 0.85`; `cust-phase-p0-platform-gate · related_to · 0.8`; `fact-gaudi3-reference-specs · derived_from · 0.7`; `task-p0-2-fp8-mme-benchmark · related_to · 0.9`; mitigation = the P0.2 micro-benchmark; treat as performance, not feasibility |
| `cust-risk-r2-hbm-side-cache-pressure` | R2 — 96GB HBM Pressure From Eager Sparse-MoE Workspace | high / high | `hyp-side-caches-oom-at-concurrency · depends_on · 0.9`; `cust-phase-p2-cache-plumbing · related_to · 0.95`; `fact-gaudi2-hbm-and-bandwidth · derived_from · 0.9`; `task-p2-1-side-caches-to-kv-blocks · related_to · 0.9`; `cust-phase-p0-platform-gate · related_to · 0.8` |
| `cust-risk-r3-sparse-topk-uncapturable` | R3 — Sparse Top-k Not Graph-Capturable | medium-high / medium | `hyp-sparse-topk-not-capturable · depends_on · 0.9`; `cust-phase-p4-capture · related_to · 0.9`; `task-p3-1-sparse-topk-kernel · related_to · 0.9`; `ref-issue-1734-synstatus-26 · related_to · 0.6`; mitigation = hybrid compiled+eager for the QSA region only |
| `cust-risk-r4-1733-lowbatch-moe` | R4 — Issue #1733 Low-Batch MoE Slowness Dominates | medium / high | `ref-issue-1733-low-batch-moe · derived_from · 0.9`; `cust-phase-p5-moe-economics · related_to · 0.95`; `task-p5-1-gathered-expert-moe-combine · related_to · 0.85`; `question-moe-saturation-point · related_to · 0.8`; mitigation = gathered-expert combine, higher concurrency, market for high-concurrency only |
| `cust-risk-r5-no-intel-primitive-roadmap` | R5 — No Public Roadmap for the Remaining Primitives | confirmed / medium | `cust-phase-p3-custom-kernels · related_to · 0.9`; `ref-tpc-sdk · related_to · 0.85`; `playbook-tpc-customop-authoring · related_to · 0.9`; `fact-customop-single-kernel-contract · derived_from · 0.8`; mitigation = use the TPC SDK + PyTorch CustomOp contract ourselves |
| `cust-risk-r6-hccl-all2all-bandwidth` | R6 — Expert-Parallel MoE Hinges on HCCL All2All Bandwidth | medium / medium-high | `hyp-all2all-enables-expert-parallel · depends_on · 0.9`; `fact-hccl-includes-all2all · derived_from · 0.7`; `cust-phase-p0-platform-gate · related_to · 0.9`; `cust-phase-p5-moe-economics · related_to · 0.85`; `question-hccl-primitive-caveats · related_to · 0.85`; `task-p0-5-benchmark-hccl-collectives · related_to · 0.9`; note: primitive existence corroborated by secondary snippets, the authoritative table 404'd — existence is not throughput |

---

## tasks/ (27)

All tasks: `part_of · <owning phase> · 0.9`, tags include `roadmap-task` and the phase id, `applicable_when` names the phase and precondition, body 50-150 words: what to do, why it matters on Gaudi 2, what "done" looks like. Status language: no task is started; state the precondition.

### P0 — `cust-phase-p0-platform-gate`

| id | title | extra edges |
|---|---|---|
| `task-p0-1-load-fp8-on-eager` | Load the FP8 Checkpoint on Gaudi 2 Eager | `fact-gaudi2-fp8-dtype-support · supports · 0.9`; `task-p0-4-set-required-flags · depends_on · 0.7` |
| `task-p0-2-fp8-mme-benchmark` | Benchmark FP8 MME Throughput vs Gaudi 3 | `hyp-gaudi2-fp8-mme-throughput-gap · related_to · 0.9`; `cust-risk-r1-fp8-mme-throughput · related_to · 0.9`; `fact-gaudi3-reference-specs · related_to · 0.7` |
| `task-p0-3-resize-tp-and-memory` | Re-derive TP Degree, Max-Model-Len, Memory Utilization | `fact-gaudi2-hbm-and-bandwidth · depends_on · 0.9`; `question-what-tp-degree-fits-gaudi2 · related_to · 0.9`; `pillar-measured-before-default · related_to · 0.9`; `cust-risk-r2-hbm-side-cache-pressure · related_to · 0.8` |
| `task-p0-4-set-required-flags` | Set the Required Runtime Flags | `concept-graph-capture-vs-eager · depends_on · 0.7`; `fact-target-stack-versions · related_to · 0.7`. Flags: `--kv-cache-dtype auto`, `VLLM_SKIP_WARMUP=true`, `--enforce-eager`, `--language-model-only` |
| `task-p0-5-benchmark-hccl-collectives` | Benchmark HCCL Collective Bandwidth Before Fixing Topology | `playbook-hccl-collective-benchmark · related_to · 0.9`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.9`; `concept-hccl-collective-layer · depends_on · 0.8`; `ref-hccl-benchmarking-docs · related_to · 0.8`. Measures allreduce/allgather/all2all before TP/EP topology is chosen |

### P1 — `cust-phase-p1-reuse-pr1829`

| id | title | extra edges |
|---|---|---|
| `task-p1-1-port-qwen4-exp-model` | Base the Port on `qwen4_exp.py` (~2.4k lines) | `fact-model-architecture-blocks · depends_on · 0.9`; `concept-gdn-gated-delta-net · related_to · 0.85`; `concept-qsa-indexer · related_to · 0.85`; `concept-ple-dilated-conv-ngram · related_to · 0.85`; `concept-hyperconnection-gated-residual · related_to · 0.8`; `source-vllm-gaudi-pr1829 · derived_from · 0.9` |
| `task-p1-2-register-model-and-runner` | Register the Model Classes and Runner Hooks | `ref-vllm-gaudi-plugin · related_to · 0.8`; `fact-model-architecture-blocks · depends_on · 0.8`. Registers `Qwen4ExpForCausalLM` + `Qwen4ExpForConditionalGeneration`, adds arch to `maybe_set_mamba_kv_cache_groups_ids` |
| `task-p1-3-retarget-pin-to-0-30-0` | Retarget from PR Pin `dd3bc9c72faf` to Plugin 0.30.0 | `fact-target-stack-versions · depends_on · 0.9`; `fact-pin-c05d75a-resolves-1734 · supports · 0.85`; `ref-upstream-vllm-pin · related_to · 0.85` |
| `task-p1-4-carry-fp8-moe-block-fix` | Carry the FP8 MoE Block-Grid Fix | `fact-plugin-0-30-0-features · related_to · 0.8`; `concept-moe-expert-parallel-vs-tp · related_to · 0.7`. Carries `_effective_moe_block_size` from `extension/ops.py` |
| `task-p1-5-honor-not-convert-drop-mtp` | Honour `modules_to_not_convert`, Drop the `mtp.*` Head | `concept-mtp-speculative-decoding · related_to · 0.85`; `question-mtp-drafter-on-hpu · related_to · 0.7` |

### P2 — `cust-phase-p2-cache-plumbing`

| id | title | extra edges |
|---|---|---|
| `task-p2-1-side-caches-to-kv-blocks` | Move Side Caches onto Scheduler-Owned KV Blocks | `concept-kv-block-ownership · depends_on · 0.95`; `hyp-side-caches-oom-at-concurrency · related_to · 0.85`; `cust-risk-r2-hbm-side-cache-pressure · related_to · 0.9`; `task-p6-3-enable-prefix-caching · followed_by · 0.8`. Covers QSA raw-key ring, compressed-key side cache, PLE dilated-conv state, n-gram trailing-token history |
| `task-p2-2-keep-prefix-caching-off` | Keep Prefix Caching OFF Until P2.1 Lands | `concept-prefix-caching-semantics · depends_on · 0.9`; `decision-prefix-cache-off-until-p2-1 · related_to · 0.9` |
| `task-p2-3-verify-decode-bucket-clamp` | Confirm Decode Block Buckets Clamp to Physical KV Size | `fact-plugin-0-30-0-features · depends_on · 0.9`; `ref-vllm-gaudi-plugin · related_to · 0.7` |

### P3 — `cust-phase-p3-custom-kernels`

| id | title | extra edges |
|---|---|---|
| `task-p3-1-sparse-topk-kernel` | Single CustomOp for Sparse Top-k / QSA Indexer | `concept-qsa-indexer · depends_on · 0.9`; `hyp-sparse-topk-not-capturable · related_to · 0.9`; `cust-risk-r3-sparse-topk-uncapturable · related_to · 0.9`; `playbook-tpc-customop-authoring · depends_on · 0.9`; `fact-customop-single-kernel-contract · depends_on · 0.9`. High graph-capture risk: data-dependent control flow |
| `task-p3-2-ple-dilated-conv-kernel` | Single CustomOp for PLE Dilated Short-Conv | `concept-ple-dilated-conv-ngram · depends_on · 0.9`; `playbook-tpc-customop-authoring · depends_on · 0.85`; `fact-plugin-0-30-0-features · related_to · 0.7`; `task-p4-4-eliminate-host-coercing-ops · followed_by · 0.7` |
| `task-p3-3-fp8-ngram-gather-kernel` | Single CustomOp for FP8 N-gram Gather-Then-Dequant | `concept-ple-dilated-conv-ngram · depends_on · 0.85`; `fact-gaudi2-fp8-dtype-support · depends_on · 0.8`; `playbook-tpc-customop-authoring · depends_on · 0.85`; `fact-customop-single-kernel-contract · depends_on · 0.85`. Stays FP8 on Gaudi 2 MME — no INT8 re-expression |

### P4a — `cust-phase-p4-pin-check`

| id | title | extra edges |
|---|---|---|
| `task-p4-1-verify-pin-c05d75a` | Verify the Build Pin is at/after `c05d75a` | `fact-pin-c05d75a-resolves-1734 · depends_on · 0.95`; `ref-issue-1734-synstatus-26 · related_to · 0.85`; `decision-pin-check-before-kernels · related_to · 0.9` |
| `task-p4-2-boot-without-enforce-eager` | Boot Without `--enforce-eager` and Record Failures | `concept-graph-capture-vs-eager · depends_on · 0.85`; `question-which-subgraphs-fail-capture · related_to · 0.9`; `task-p4-1-verify-pin-c05d75a · depends_on · 0.8`; `playbook-graph-capture-triage · related_to · 0.8` |

### P4b — `cust-phase-p4-capture`

| id | title | extra edges |
|---|---|---|
| `task-p4-3-apply-pr1843-mitigations` | Integrate PR #1843 Capture Mitigations | `source-vllm-gaudi-pr1843 · derived_from · 0.9`; `ref-pr1843-mitigations · depends_on · 0.9`; `concept-graph-capture-vs-eager · related_to · 0.8`. DS=0 concrete-plan recipe, host-side decode count fix, bmm score contraction fix, flat `index_copy_` store rewrite restoring first-request survival |
| `task-p4-4-eliminate-host-coercing-ops` | Remove Host-Coercing Ops From QSA/PLE Hot Paths | `concept-qsa-indexer · related_to · 0.85`; `concept-ple-dilated-conv-ngram · related_to · 0.85`; `concept-graph-capture-vs-eager · depends_on · 0.85`. Targets `.nonzero` in PLE `_pool_and_store`, `.item()`, `torch.minimum` in `_expand_plan`, `keep.any()` in the KV-store epilogue |
| `task-p4-5-meet-customop-capture-contract` | Prove Each P3 CustomOp Satisfies the Capture Contract | `fact-customop-single-kernel-contract · depends_on · 0.95`; `hyp-customop-gates-compile-capture · related_to · 0.9`; `task-p3-1-sparse-topk-kernel · depends_on · 0.8`; `task-p3-2-ple-dilated-conv-kernel · depends_on · 0.8`; `task-p3-3-fp8-ngram-gather-kernel · depends_on · 0.8` |

### P5 — `cust-phase-p5-moe-economics`

| id | title | extra edges |
|---|---|---|
| `task-p5-1-gathered-expert-moe-combine` | Enable Gathered-Expert MoE Combine for FP8 | `fact-plugin-0-30-0-features · depends_on · 0.9`; `cust-risk-r4-1733-lowbatch-moe · related_to · 0.85`; `concept-moe-expert-parallel-vs-tp · related_to · 0.8` |
| `task-p5-2-preregister-throughput-protocol` | Pre-register the Throughput Protocol Before Each Lever | `playbook-fp8-moe-throughput-attribution · depends_on · 0.95`; `pillar-measured-before-default · related_to · 0.85`; `question-moe-saturation-point · related_to · 0.8`. Mirrors PR seeds 301-303 |
| `task-p5-3-tune-bucketing-and-tp-ep` | Tune Decode Bucketing; Treat Higher TP/EP as Measured | `task-p0-5-benchmark-hccl-collectives · depends_on · 0.9`; `hyp-all2all-enables-expert-parallel · related_to · 0.9`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.85`; `decision-tp-ep-measured-not-default · related_to · 0.9` |

### P6 — `cust-phase-p6-feature-parity`

| id | title | extra edges |
|---|---|---|
| `task-p6-1-hpu-mtp-drafter` | Implement an HPU MTP Drafter (or Accept the Dropped Head) | `concept-mtp-speculative-decoding · depends_on · 0.9`; `question-mtp-drafter-on-hpu · related_to · 0.9`; `task-p1-5-honor-not-convert-drop-mtp · preceded_by · 0.8` |
| `task-p6-2-vision-tower` | Implement the Vision Stack for Conditional Generation | `task-p1-2-register-model-and-runner · depends_on · 0.7`; `source-vllm-gaudi-pr1829 · related_to · 0.7`. PR #1829 excluded the vision tower |
| `task-p6-3-enable-prefix-caching` | Re-enable Prefix Caching With Regression Coverage | `concept-prefix-caching-semantics · depends_on · 0.9`; `task-p2-1-side-caches-to-kv-blocks · depends_on · 0.95`; `task-p2-2-keep-prefix-caching-off · contradicts · 0.8`. Deferred until P2.1 lands |

---

## decisions/ (7)

Body sections: `Context`, `Alternatives considered`, `Decision`, `Consequence`.

| id | title | spec + edges |
|---|---|---|
| `decision-reuse-pr1829-as-base` | Base the Port on vllm-gaudi PR #1829 Rather Than a Fresh Implementation | Alternatives: fresh implementation from the model config; upstreaming to core vLLM first. `pillar-reuse-over-rederivation · supports · 0.95`; `source-vllm-gaudi-pr1829 · derived_from · 0.9`; `cust-phase-p1-reuse-pr1829 · related_to · 0.9`; `fact-pr1829-scope-and-limits · depends_on · 0.85` |
| `decision-pin-check-before-kernels` | Run the Cheap Pin Check Before Committing to Kernel Authoring | Flagged by the roadmap as judgment on leverage, not a sourced claim — cap confidence at 0.65. `cust-phase-p4-pin-check · related_to · 0.9`; `fact-pin-c05d75a-resolves-1734 · supports · 0.8`; `hyp-customop-gates-compile-capture · related_to · 0.7`; `task-p4-1-verify-pin-c05d75a · related_to · 0.85` |
| `decision-fp8-no-requantization` | Serve the FP8 Checkpoint Directly — No Re-quantization Fork | E4M3/E5M2 are supported on Gaudi 2, so no INT8 or BF16 re-expression fork. `fact-gaudi2-fp8-dtype-support · supports · 0.9`; `task-p3-3-fp8-ngram-gather-kernel · related_to · 0.8`; `cust-phase-p0-platform-gate · related_to · 0.8`; `task-p0-1-load-fp8-on-eager · related_to · 0.85` |
| `decision-prefix-cache-off-until-p2-1` | Keep Prefix Caching Disabled Until Side Caches Are Block-Managed | Correctness before a feature nobody can serve yet. `concept-prefix-caching-semantics · depends_on · 0.9`; `task-p2-2-keep-prefix-caching-off · related_to · 0.9`; `task-p2-1-side-caches-to-kv-blocks · depends_on · 0.85`; `cust-risk-r2-hbm-side-cache-pressure · related_to · 0.8` |
| `decision-tp-ep-measured-not-default` | Choose TP Degree and Expert Parallelism From Measured Bandwidth | EP is an all-to-all dispatch/combine pattern; feasibility depends on measured all2all throughput, not on the primitive existing. Do not copy the Gaudi 3 TP4 default. `pillar-measured-before-default · supports · 0.95`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.9`; `task-p0-5-benchmark-hccl-collectives · depends_on · 0.9`; `concept-moe-expert-parallel-vs-tp · depends_on · 0.85`; `task-p5-3-tune-bucketing-and-tp-ep · related_to · 0.85` |
| `decision-eager-first-compiled-later` | Serve Eager-First, Remove `--enforce-eager` Only After Capture Work | Eager is the correctness baseline and the byte-equality reference; compiled mode is the later speed lever. `concept-graph-capture-vs-eager · depends_on · 0.9`; `cust-phase-p0-platform-gate · related_to · 0.85`; `cust-phase-p4-capture · related_to · 0.9`; `ref-issue-1734-synstatus-26 · related_to · 0.75` |
| `decision-defer-feature-parity-p6` | Defer MTP, Vision, and Prefix Caching Behind Text-Only Serving | P6 is product-driven, not required for enablement. `cust-phase-p6-feature-parity · related_to · 0.9`; `task-p6-1-hpu-mtp-drafter · related_to · 0.8`; `task-p6-2-vision-tower · related_to · 0.8`; `task-p6-3-enable-prefix-caching · related_to · 0.8` |

---

## facts/ (10)

Body: the statement, the numbers, and where it came from. `source_url` populated where a public URL is known; otherwise `"Empty"` with the source node named in edges.

| id | title | spec + edges |
|---|---|---|
| `fact-gaudi2-hbm-and-bandwidth` | Gaudi 2 Has 96GB HBM2E at 2.45 TB/s per Card | Also: 24x100 Gbps RoCE on-chip; 4 cards in this target. `source-gaudi2-spec-sheets · derived_from · 0.9`; `fact-gaudi3-reference-specs · related_to · 0.8`; `decision-tp-ep-measured-not-default · supports · 0.8`; `cust-phase-p0-platform-gate · related_to · 0.85` |
| `fact-gaudi2-fp8-dtype-support` | Gaudi 2 Supports FP8 E4M3 and E5M2 | Capability confirmed; throughput is not. `source-gaudi2-spec-sheets · derived_from · 0.9`; `decision-fp8-no-requantization · supports · 0.9`; `hyp-gaudi2-fp8-mme-throughput-gap · related_to · 0.85`; `task-p0-1-load-fp8-on-eager · supports · 0.9` |
| `fact-gaudi3-reference-specs` | Gaudi 3 Reference: 128GB, 3.7 TB/s, 1.8 PFlops FP8 | The comparison point PR #1829 was built against; explains why its TP/util numbers do not transfer. `source-vllm-gaudi-pr1829 · derived_from · 0.85`; `related_to · fact-gaudi2-hbm-and-bandwidth · 0.8`; `supports · pillar-measured-before-default · 0.85` |
| `fact-target-stack-versions` | Target Stack: Suite 1.24.2, PyTorch 2.13, Plugin 0.30.0, 4x Gaudi 2 | Upstream vLLM pinned at/after `c05d75a`. `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.9`; `ref-vllm-gaudi-plugin · related_to · 0.9`; `ref-upstream-vllm-pin · related_to · 0.9`; `task-p1-3-retarget-pin-to-0-30-0 · supports · 0.9` |
| `fact-pin-c05d75a-resolves-1734` | Upstream Pin `c05d75a` Resolved synStatus-26 for GDN Hybrids | "Keep Qwen3Next layer boundaries sequence parallel" resolved issue #1734 with no plugin change. `ref-issue-1734-synstatus-26 · derived_from · 0.85`; `ref-upstream-vllm-pin · related_to · 0.9`; `task-p4-1-verify-pin-c05d75a · supports · 0.9`; `cust-phase-p4-pin-check · supports · 0.85` |
| `fact-hccl-includes-all2all` | HCCL Exposes allreduce, allgather, reduce-scatter and all2all | Confidence capped at 0.65: HCCL is Gaudi's NCCL emulation layer and the collective list is corroborated by secondary snippets; the authoritative primitives table 404'd under `latest`. Per-primitive dtype/topology caveats unverified. `concept-hccl-collective-layer · related_to · 0.85`; `cust-risk-r6-hccl-all2all-bandwidth · supports · 0.7`; `question-hccl-primitive-caveats · related_to · 0.9`; `source-hccl-docs-index · derived_from · 0.8` |
| `fact-customop-single-kernel-contract` | A UserCustomOp Is One TPC Kernel and Needs the `custom_op` Namespace | Registration via `registerUserCustomOp(schema, tpc_guid, OutputMetaFn, optional FillParamsFn)` with types in `hpu_custom_op_pt2.h`; multi-op Python decomposition re-creates eager dispatch cost; namespace registration gates full `torch.compile` support. `source-pytorch-customop-docs · derived_from · 0.85`; `ref-pytorch-customop-api · related_to · 0.9`; `ref-tpc-sdk · related_to · 0.9`; `playbook-tpc-customop-authoring · supports · 0.9`; `hyp-customop-gates-compile-capture · supports · 0.8` |
| `fact-plugin-0-30-0-features` | Plugin v0.30.0 Ships Gathered-Expert MoE Combine and Clamped Decode Buckets | Release lineage also brought TPC-native `causal_conv1d` and FP8/INC stability (v0.24.0 onward). `source-vllm-gaudi-release-notes · derived_from · 0.85`; `task-p5-1-gathered-expert-moe-combine · supports · 0.9`; `task-p2-3-verify-decode-bucket-clamp · supports · 0.9`; `ref-vllm-gaudi-plugin · related_to · 0.85` |
| `fact-pr1829-scope-and-limits` | PR #1829 Is a Gaudi 3, Eager-Only Qwen4Exp Port | ~2.4k lines in `vllm_gaudi/models/qwen4_exp.py`; no compiled-mode support, no vision tower, `mtp.*` head dropped, pinned to `dd3bc9c72faf`. `source-vllm-gaudi-pr1829 · derived_from · 0.9`; `decision-reuse-pr1829-as-base · supports · 0.85`; `fact-model-architecture-blocks · related_to · 0.85`; `cust-phase-p1-reuse-pr1829 · supports · 0.9` |
| `fact-model-architecture-blocks` | Qwen3.8-Flash-Next Composition: GDN, QSA, PLE, HyperConnection, MoE | GDN with 48 value heads / 16 QK heads / 128 head dim, QSA indexer + attention, PLE norm + n-gram embedding, gated-residual HyperConnection, FP8 sparse MoE, plus an `mtp.*` head the port drops. `source-vllm-gaudi-pr1829 · derived_from · 0.85`; `concept-gdn-gated-delta-net · related_to · 0.9`; `concept-qsa-indexer · related_to · 0.9`; `concept-ple-dilated-conv-ngram · related_to · 0.9`; `concept-hyperconnection-gated-residual · related_to · 0.85` |

---

## hypotheses/ (5)

Body: the claim, the test that settles it, what changes if it is false. All `verified_at: "Empty"`.

| id | title | spec + edges |
|---|---|---|
| `hyp-gaudi2-fp8-mme-throughput-gap` | Gaudi 2 FP8 MME Throughput Trails Gaudi 3 | Test: P0.2 micro-benchmark. Flagged by the roadmap as an inference from spec sheets, not a measurement. `fact-gaudi2-fp8-dtype-support · depends_on · 0.8`; `cust-risk-r1-fp8-mme-throughput · supports · 0.85`; `task-p0-2-fp8-mme-benchmark · related_to · 0.9`; `fact-gaudi3-reference-specs · derived_from · 0.7` |
| `hyp-sparse-topk-not-capturable` | Sparse Top-k Stays Uncapturable Even as a Single CustomOp | Data-dependent control flow may be a compiler-layer limit; author inference. Test: P4.2 capture attempt after P3.1 lands. `cust-risk-r3-sparse-topk-uncapturable · supports · 0.9`; `task-p3-1-sparse-topk-kernel · related_to · 0.85`; `task-p4-2-boot-without-enforce-eager · related_to · 0.85`; `ref-issue-1734-synstatus-26 · related_to · 0.6`; `contradicts · decision-eager-first-compiled-later · 0.5` (only weakly: it bounds how far compiled mode can go) |
| `hyp-all2all-enables-expert-parallel` | HCCL All2All Bandwidth Is Sufficient for Expert-Parallel MoE | The primitive exists; its throughput on the Gaudi 2 fabric is unmeasured. Test: P0.5 numbers vs the allreduce baseline. `fact-hccl-includes-all2all · depends_on · 0.7`; `cust-risk-r6-hccl-all2all-bandwidth · supports · 0.9`; `task-p0-5-benchmark-hccl-collectives · related_to · 0.9`; `concept-moe-expert-parallel-vs-tp · depends_on · 0.8`; `question-hccl-primitive-caveats · related_to · 0.8` |
| `hyp-customop-gates-compile-capture` | Single-Kernel + `custom_op` Namespace Is What Unblocks Capture | The roadmap flags this P3→P4 ordering as its author's reading of the contract, not an Intel statement. Test: capture after one compliant CustomOp. `fact-customop-single-kernel-contract · depends_on · 0.8`; `cust-phase-p4-capture · related_to · 0.85`; `task-p4-5-meet-customop-capture-contract · supports · 0.85`; `decision-pin-check-before-kernels · related_to · 0.6`; `note-provenance-register · related_to · 0.8` |
| `hyp-side-caches-oom-at-concurrency` | Module-Allocated Side Caches OOM at Target Concurrency on 96GB | QSA ring + compressed-key cache + PLE state + n-gram history grow with concurrency outside scheduler control. Test: concurrency ramp at target max-model-len. `fact-gaudi2-hbm-and-bandwidth · depends_on · 0.85`; `cust-risk-r2-hbm-side-cache-pressure · supports · 0.9`; `task-p2-1-side-caches-to-kv-blocks · related_to · 0.9`; `concept-kv-block-ownership · related_to · 0.85` |

---

## questions/ (5)

Body: the question, why it blocks, which measurement answers it.

| id | title | edges |
|---|---|---|
| `question-what-tp-degree-fits-gaudi2` | What TP Degree and Context Length Actually Fit on 4x Gaudi 2? | `task-p0-3-resize-tp-and-memory · related_to · 0.9`; `hyp-side-caches-oom-at-concurrency · depends_on · 0.75`; `fact-gaudi2-hbm-and-bandwidth · depends_on · 0.85`; `cust-phase-p0-platform-gate · related_to · 0.9` |
| `question-which-subgraphs-fail-capture` | Which Subgraphs Still Fail to Capture After the Pin Fix? | `task-p4-2-boot-without-enforce-eager · related_to · 0.9`; `cust-phase-p4-pin-check · related_to · 0.9`; `hyp-sparse-topk-not-capturable · related_to · 0.8`; `playbook-graph-capture-triage · related_to · 0.8` |
| `question-moe-saturation-point` | Where Does Cost-per-Token Saturate on Gaudi 2? | `task-p5-2-preregister-throughput-protocol · related_to · 0.85`; `cust-risk-r4-1733-lowbatch-moe · depends_on · 0.8`; `cust-phase-p5-moe-economics · related_to · 0.9` |
| `question-hccl-primitive-caveats` | What Per-Primitive Caveats Apply to HCCL all2all on Suite 1.24.2? | `fact-hccl-includes-all2all · depends_on · 0.8`; `bookmark-hccl-primitives-table · related_to · 0.9`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.9`; `note-provenance-register · related_to · 0.75` |
| `question-mtp-drafter-on-hpu` | Is an HPU MTP Drafter Worth Building Against the Dropped Head? | `task-p6-1-hpu-mtp-drafter · related_to · 0.9`; `concept-mtp-speculative-decoding · depends_on · 0.85`; `cust-phase-p6-feature-parity · related_to · 0.85` |

---

## concepts/ (11)

Body: what it is, why it matters specifically for this port, and the failure mode it explains.

| id | title | edges |
|---|---|---|
| `concept-gdn-gated-delta-net` | Gated DeltaNet (GDN) Linear-Attention State | `fact-model-architecture-blocks · related_to · 0.9`; `task-p1-1-port-qwen4-exp-model · related_to · 0.85`; `ref-issue-1734-synstatus-26 · related_to · 0.8`; `concept-kv-block-ownership · related_to · 0.7`; `depends_on · fact-pin-c05d75a-resolves-1734 · 0.7` |
| `concept-qsa-indexer` | QSA Indexer and Sparse Attention Selection | `fact-model-architecture-blocks · related_to · 0.9`; `task-p3-1-sparse-topk-kernel · related_to · 0.9`; `concept-tpc-customop-integration · related_to · 0.8`; `task-p4-4-eliminate-host-coercing-ops · related_to · 0.85`; `hyp-sparse-topk-not-capturable · related_to · 0.85` |
| `concept-ple-dilated-conv-ngram` | PLE Dilated Short-Conv and N-gram Embedding State | `fact-model-architecture-blocks · related_to · 0.9`; `task-p3-2-ple-dilated-conv-kernel · related_to · 0.9`; `task-p3-3-fp8-ngram-gather-kernel · related_to · 0.9`; `task-p4-4-eliminate-host-coercing-ops · related_to · 0.85`; `concept-kv-block-ownership · related_to · 0.8` |
| `concept-hyperconnection-gated-residual` | HyperConnection Gated Residual (`HpuGatedResidual`) | `fact-model-architecture-blocks · related_to · 0.85`; `task-p1-1-port-qwen4-exp-model · related_to · 0.8`; `concept-graph-capture-vs-eager · related_to · 0.6`; `ref-issue-1734-synstatus-26 · related_to · 0.7` |
| `concept-moe-expert-parallel-vs-tp` | Expert Parallelism vs Tensor Parallelism for Sparse MoE | `fact-model-architecture-blocks · related_to · 0.85`; `concept-hccl-collective-layer · depends_on · 0.85`; `decision-tp-ep-measured-not-default · related_to · 0.9`; `hyp-all2all-enables-expert-parallel · related_to · 0.9`; `task-p5-3-tune-bucketing-and-tp-ep · related_to · 0.8`; `cust-risk-r4-1733-lowbatch-moe · related_to · 0.75` |
| `concept-hccl-collective-layer` | HCCL as Gaudi's NCCL Emulation Layer | `fact-hccl-includes-all2all · related_to · 0.9`; `ref-hccl-benchmarking-docs · related_to · 0.85`; `concept-moe-expert-parallel-vs-tp · supports · 0.8`; `task-p0-5-benchmark-hccl-collectives · related_to · 0.85`; `bookmark-hccl-primitives-table · related_to · 0.7` |
| `concept-tpc-customop-integration` | TPC CustomOp Integration Path | `fact-customop-single-kernel-contract · depends_on · 0.9`; `playbook-tpc-customop-authoring · related_to · 0.9`; `ref-tpc-sdk · related_to · 0.9`; `ref-pytorch-customop-api · related_to · 0.9`; `cust-phase-p3-custom-kernels · related_to · 0.9` |
| `concept-graph-capture-vs-eager` | Eager Execution vs HPU Graph Capture | `task-p4-2-boot-without-enforce-eager · related_to · 0.9`; `ref-issue-1734-synstatus-26 · related_to · 0.9`; `task-p0-4-set-required-flags · related_to · 0.8`; `concept-qsa-indexer · related_to · 0.8`; `decision-eager-first-compiled-later · related_to · 0.9` |
| `concept-prefix-caching-semantics` | Prefix Caching Correctness Under Hybrid State | `task-p2-2-keep-prefix-caching-off · related_to · 0.9`; `task-p6-3-enable-prefix-caching · related_to · 0.9`; `concept-kv-block-ownership · depends_on · 0.85`; `decision-prefix-cache-off-until-p2-1 · related_to · 0.9`; `concept-ple-dilated-conv-ngram · related_to · 0.75` |
| `concept-kv-block-ownership` | Scheduler-Owned KV Blocks vs Module-Allocated Buffers | `task-p2-1-side-caches-to-kv-blocks · related_to · 0.95`; `hyp-side-caches-oom-at-concurrency · related_to · 0.9`; `concept-prefix-caching-semantics · supports · 0.8`; `concept-gdn-gated-delta-net · related_to · 0.7`; `cust-phase-p2-cache-plumbing · related_to · 0.9` |
| `concept-mtp-speculative-decoding` | MTP Multi-Token-Prediction Speculative Decoding | `task-p6-1-hpu-mtp-drafter · related_to · 0.9`; `task-p1-5-honor-not-convert-drop-mtp · related_to · 0.85`; `question-mtp-drafter-on-hpu · related_to · 0.9`; `ref-vllm-gaudi-plugin · related_to · 0.7` |

---

## playbooks/ (5)

Body: numbered steps, verification at each step, and the "stop and escalate" condition.

| id | title | edges |
|---|---|---|
| `playbook-tpc-customop-authoring` | Authoring a TPC CustomOp for One Primitive | `concept-tpc-customop-integration · depends_on · 0.9`; `fact-customop-single-kernel-contract · depends_on · 0.9`; `cust-phase-p3-custom-kernels · related_to · 0.9`; `ref-tpc-sdk · related_to · 0.85`; `ref-pytorch-customop-api · related_to · 0.85`; `task-p3-1-sparse-topk-kernel · related_to · 0.85` |
| `playbook-hccl-collective-benchmark` | Benchmarking HCCL Collectives Before Choosing Topology | `concept-hccl-collective-layer · depends_on · 0.85`; `task-p0-5-benchmark-hccl-collectives · related_to · 0.9`; `ref-hccl-benchmarking-docs · related_to · 0.9`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.85`; `cust-phase-p0-platform-gate · related_to · 0.9` |
| `playbook-graph-capture-triage` | Triaging HPU Graph Capture Failures | `concept-graph-capture-vs-eager · depends_on · 0.9`; `task-p4-2-boot-without-enforce-eager · related_to · 0.9`; `task-p4-4-eliminate-host-coercing-ops · related_to · 0.9`; `ref-pr1843-mitigations · related_to · 0.85`; `cust-phase-p4-capture · related_to · 0.9`; `ref-issue-1734-synstatus-26 · related_to · 0.8` |
| `playbook-fp8-moe-throughput-attribution` | Attributing MoE Throughput Changes to One Lever | `task-p5-2-preregister-throughput-protocol · depends_on · 0.95`; `cust-phase-p5-moe-economics · related_to · 0.9`; `pillar-measured-before-default · related_to · 0.85`; `question-moe-saturation-point · related_to · 0.85`; `task-p5-1-gathered-expert-moe-combine · related_to · 0.8` |
| `playbook-agent-grounding` | Grounding an Agent in This Vault Before Work | `pillar-provenance-discipline · depends_on · 0.8`; `cust-phase-p0-platform-gate · related_to · 0.8`; `source-roadmap-qwen4-exp-gaudi2-v1-1 · related_to · 0.7`; `cust-phase-p3-custom-kernels · related_to · 0.75`; `cust-phase-p2-cache-plumbing · related_to · 0.7` |

---

## references/ (8)

Body: what the thing is, current known state, and what to re-check. `visibility: public`, `source_url` where known.

| id | title | edges |
|---|---|---|
| `ref-vllm-gaudi-plugin` | vllm-gaudi Plugin | `fact-target-stack-versions · related_to · 0.9`; `source-vllm-gaudi-release-notes · related_to · 0.85`; `fact-plugin-0-30-0-features · related_to · 0.9`; `cust-phase-p1-reuse-pr1829 · related_to · 0.85` |
| `ref-upstream-vllm-pin` | Upstream vLLM Pin `c05d75a` | `fact-pin-c05d75a-resolves-1734 · related_to · 0.9`; `fact-target-stack-versions · related_to · 0.9`; `task-p1-3-retarget-pin-to-0-30-0 · related_to · 0.85`; `cust-phase-p4-pin-check · related_to · 0.8` |
| `ref-issue-1733-low-batch-moe` | vllm-gaudi Issue #1733 — MoE Slowness at Low Batch | `cust-risk-r4-1733-lowbatch-moe · related_to · 0.95`; `cust-phase-p5-moe-economics · related_to · 0.9`; `task-p5-1-gathered-expert-moe-combine · related_to · 0.8`; `concept-moe-expert-parallel-vs-tp · related_to · 0.7` |
| `ref-issue-1734-synstatus-26` | vllm-gaudi Issue #1734 — synStatus-26 / compileGraph | `fact-pin-c05d75a-resolves-1734 · related_to · 0.95`; `cust-phase-p4-capture · related_to · 0.9`; `concept-graph-capture-vs-eager · related_to · 0.9`; `concept-gdn-gated-delta-net · related_to · 0.8`; `hyp-sparse-topk-not-capturable · related_to · 0.6` |
| `ref-pr1843-mitigations` | PR #1843 Capture Mitigations | `task-p4-3-apply-pr1843-mitigations · related_to · 0.95`; `source-vllm-gaudi-pr1843 · related_to · 0.9`; `playbook-graph-capture-triage · related_to · 0.85`; `cust-phase-p4-capture · related_to · 0.85` |
| `ref-tpc-sdk` | Gaudi TPC SDK | `fact-customop-single-kernel-contract · related_to · 0.9`; `playbook-tpc-customop-authoring · related_to · 0.9`; `cust-phase-p3-custom-kernels · related_to · 0.9`; `cust-risk-r5-no-intel-primitive-roadmap · related_to · 0.85`; `bookmark-tpc-sdk-kernel-guide · related_to · 0.8` |
| `ref-pytorch-customop-api` | PyTorch CustomOp API Contract | `fact-customop-single-kernel-contract · related_to · 0.95`; `concept-tpc-customop-integration · related_to · 0.9`; `playbook-tpc-customop-authoring · related_to · 0.85`; `source-pytorch-customop-docs · related_to · 0.9` |
| `ref-hccl-benchmarking-docs` | HCCL Testing & Benchmarking Documentation | `playbook-hccl-collective-benchmark · related_to · 0.9`; `concept-hccl-collective-layer · related_to · 0.85`; `task-p0-5-benchmark-hccl-collectives · related_to · 0.85`; `bookmark-hccl-primitives-table · related_to · 0.8`; `source-hccl-docs-index · related_to · 0.85` |

---

## sources/ (7)

Body: what the source is, what it grounds in this vault, and how current it is.

| id | title | spec + edges |
|---|---|---|
| `source-roadmap-qwen4-exp-gaudi2-v1-1` | Roadmap JSON v1.1 (qwen4_exp on Gaudi 2) | The seeded origin: `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json`. `cust-phase-p0-platform-gate · related_to · 0.9`; `note-provenance-register · related_to · 0.9`; `event-2026-10-15-roadmap-baseline-v1-1 · related_to · 0.8`; `visibility: public` |
| `source-vllm-gaudi-pr1829` | vllm-gaudi PR #1829 — Qwen4Exp on Gaudi 3 | Grounds P1 and the architecture facts; needs its description + diff dropped into `raw/` for a real conversion. `source_url: https://github.com/HabanaAI/vllm-gaudi/pull/1829` (verify path on landing); `fact-pr1829-scope-and-limits · supports · 0.9`; `decision-reuse-pr1829-as-base · supports · 0.9`; `bookmark-pr1829-diff · followed_by · 0.7`; `cust-phase-p1-reuse-pr1829 · supports · 0.9` |
| `source-vllm-gaudi-pr1843` | vllm-gaudi PR #1843 — Capture Mitigations | `source_url: https://github.com/HabanaAI/vllm-gaudi/pull/1843` (verify path on landing); `task-p4-3-apply-pr1843-mitigations · supports · 0.9`; `cust-phase-p4-capture · supports · 0.8`; `ref-pr1843-mitigations · related_to · 0.9`; `bookmark-pr1843-diff · followed_by · 0.7` |
| `source-vllm-gaudi-release-notes` | vllm-gaudi Release Notes v0.24.0 → v0.30.0 | TPC-native `causal_conv1d`, FP8/INC stability, gathered-expert MoE combine. `fact-plugin-0-30-0-features · supports · 0.9`; `ref-vllm-gaudi-plugin · related_to · 0.85`; `cust-phase-p5-moe-economics · supports · 0.7` |
| `source-gaudi2-spec-sheets` | Gaudi 2 Hardware Specification Sources | 96GB HBM2E @ 2.45 TB/s, 24x100 Gbps RoCE, FP8 E4M3/E5M2. `fact-gaudi2-hbm-and-bandwidth · supports · 0.9`; `fact-gaudi2-fp8-dtype-support · supports · 0.9`; `pillar-measured-before-default · related_to · 0.6` |
| `source-hccl-docs-index` | HCCL Documentation Index (Suite 1.24.2) | Index page corroborates the collective list; the primitives table 404'd. `fact-hccl-includes-all2all · supports · 0.7`; `concept-hccl-collective-layer · supports · 0.8`; `question-hccl-primitive-caveats · related_to · 0.85`; `bookmark-hccl-primitives-table · related_to · 0.85` |
| `source-pytorch-customop-docs` | PyTorch CustomOp API Documentation | `fact-customop-single-kernel-contract · supports · 0.9`; `ref-pytorch-customop-api · related_to · 0.9`; `playbook-tpc-customop-authoring · supports · 0.7` |

---

## bookmarks/ (4)

Body: the link, why it matters, what converting it would produce. `confidence: 0.3` (unprocessed), `visibility: namespace`.

| id | title | edges |
|---|---|---|
| `bookmark-pr1829-diff` | Unprocessed: PR #1829 Description and Diff | `source-vllm-gaudi-pr1829 · derived_from · 0.8`; `task-p1-1-port-qwen4-exp-model · related_to · 0.8`; `note-seed-coverage-and-gaps · related_to · 0.8` |
| `bookmark-pr1843-diff` | Unprocessed: PR #1843 Description and Diff | `source-vllm-gaudi-pr1843 · derived_from · 0.8`; `task-p4-3-apply-pr1843-mitigations · related_to · 0.8`; `note-seed-coverage-and-gaps · related_to · 0.8` |
| `bookmark-hccl-primitives-table` | Unprocessed: HCCL Supported Primitives Table (404 under `latest`) | `source-hccl-docs-index · derived_from · 0.85`; `question-hccl-primitive-caveats · related_to · 0.9`; `fact-hccl-includes-all2all · related_to · 0.8`; `cust-risk-r6-hccl-all2all-bandwidth · related_to · 0.75` |
| `bookmark-tpc-sdk-kernel-guide` | Unprocessed: TPC SDK Kernel Authoring Guide | `ref-tpc-sdk · related_to · 0.9`; `playbook-tpc-customop-authoring · related_to · 0.85`; `cust-risk-r5-no-intel-primitive-roadmap · related_to · 0.7` |

---

## events/ (2)

| id | title | edges |
|---|---|---|
| `event-2026-10-15-roadmap-baseline-v1-1` | Roadmap v1.1 Adopted as Baseline | `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.9`; `followed_by · event-2026-10-15-vault-seed-build · 0.9`; `cust-phase-p0-platform-gate · related_to · 0.7` |
| `event-2026-10-15-vault-seed-build` | Vault Seeded from the Roadmap (111 Nodes) | `event-2026-10-15-roadmap-baseline-v1-1 · preceded_by · 0.9`; `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.85`; `note-seed-coverage-and-gaps · related_to · 0.9` |

---

## notes/ (2)

| id | title | edges |
|---|---|---|
| `note-provenance-register` | Provenance Register — What Is Sourced and What Is Inference | Carries the roadmap's `evidence_grounded` and `author_inference_flagged` lists verbatim, item by item, each mapped to the nodes that depend on it. `source-roadmap-qwen4-exp-gaudi2-v1-1 · derived_from · 0.95`; `pillar-provenance-discipline · related_to · 0.9`; `hyp-customop-gates-compile-capture · related_to · 0.85`; `fact-hccl-includes-all2all · related_to · 0.85`; `question-hccl-primitive-caveats · related_to · 0.8`; `decision-pin-check-before-kernels · related_to · 0.85` |
| `note-seed-coverage-and-gaps` | Seed Coverage and Known Gaps | What the seed converted from the roadmap, what it could not (PR diffs, plugin release notes, HCCL table, zero measurements), and the exact `raw/` inputs that would close each gap. `event-2026-10-15-vault-seed-build · derived_from · 0.9`; `bookmark-pr1829-diff · related_to · 0.85`; `bookmark-pr1843-diff · related_to · 0.85`; `bookmark-hccl-primitives-table · related_to · 0.85`; `bookmark-tpc-sdk-kernel-guide · related_to · 0.8`; `note-provenance-register · related_to · 0.8` |

---

## Not Seeded (deliberate)

- `patterns/` — a pattern is a *validated* recurring solution. Nothing here has survived a Gaudi 2 run yet. Candidates to promote later: "measure collectives before topology", "byte-equality check before fusion".
- `contacts/` — the roadmap names no people or teams. Populate when ownership exists; `authored_by` edges currently point at nothing by design.
- `patterns` and `contacts` stay empty with `.gitkeep` — an empty folder is a true statement, a fabricated node is not.
