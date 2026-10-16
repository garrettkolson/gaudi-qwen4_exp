# CLAUDE.md — Qwen3.8-Flash-Next (`qwen4_exp`) Serving on Gaudi 2 via vllm-gaudi

This repository's purpose is to serve **Qwen3.8-Flash-Next (qwen4_exp)** on **4x Gaudi 2** through the **vllm-gaudi** plugin — from a correct eager forward pass to compiled-mode serving with documented MoE economics.

The project's working memory is not this file and not any agent's context window. It is the **Infinite Brain knowledge graph** in this repository: typed nodes, typed edges, trust metadata. The roadmap at the root is the human-owned source document; the graph is the machine-usable form of it.

---

## 1. Grounding is mandatory before any work

**Every working agent grounds itself in the vault before beginning any work.** No agent starts a task from a prompt, a ticket, or its own memory. Not for a code change, not for a benchmark, not for a "quick question" about the project.

Grounding sequence (read-only — grounding writes nothing):

1. `CLAUDE.md` (this file).
2. `_system/INDEX.md` — the map of all nodes, grouped by type with summaries.
3. The **phase node** for the work you are about to do: `custom/cust-phase-*.md`. Then every `tasks/task-*.md` linked into it.
4. Walk `depends_on` edges **upstream** from those tasks. **An unmet dependency is a stop condition, not advice.** P3 work before P1 lands, or P5 work before P4_capture, is wasted work by design of the plan.
5. The phase's `cust-risk-*.md` nodes, plus any `hyp-*` / `question-*` node its tasks name. Confidence below 0.7 means **unverified** — you have to measure it, not assume it.
6. Only then start.

If the graph is missing something you need, that is a finding: create the node with real edges, or report the gap. If the graph contradicts your assignment, **the graph wins until a human says otherwise** — record the conflict as a finding rather than silently diverging.

Use `/query-vault` (or `_system/_prompts/Query Vault Prompt.md` if you have no slash commands) for specific questions instead of grepping the whole vault. Targeted traversal costs a few hundred tokens; reading everything does not.

```bash
python _system/lint_vault.py      # verify the graph is intact before you trust it
```

---

## 2. Target stack

| Component | Version / Value |
|---|---|
| Gaudi software suite | 1.24.2 |
| PyTorch | 2.13 |
| vllm-gaudi plugin | 0.30.0 |
| Upstream vLLM | 0.30.0, pinned at/after `c05d75a` |
| Hardware | 4x Gaudi 2 |
| Per-card memory | 96 GB HBM2E @ 2.45 TB/s |
| FP8 support | E4M3 and E5M2 |
| Reference port | vllm-gaudi PR #1829 (Gaudi 3, eager-only) |

Source of truth: `qwen4_exp_gaudi2_roadmap.json` (root). The vault reads the immutable copy at `raw/processed/2026-10-15-qwen4-exp-gaudi2-roadmap-v1.1.json`.

---

## 3. The plan at a glance

Recommended execution order: **P0 → P1 → P4_pin_check → P3 → P4_capture → P5** (P2 branches off P1; P6 is deferred).

| Phase | Goal | Gate |
|---|---|---|
| [P0](custom/cust-phase-p0-platform-gate.md) | Confirm FP8 is a real runtime path on Gaudi 2 and size HBM/TP from measurements | **Gating** — nothing proceeds without it |
| [P1](custom/cust-phase-p1-reuse-pr1829.md) | Correct eager forward by retargeting PR #1829, not re-deriving the model | depends on P0 |
| [P2](custom/cust-phase-p2-cache-plumbing.md) | Side caches onto scheduler-owned KV blocks; stable at concurrency 8+ | depends on P1 |
| [P3](custom/cust-phase-p3-custom-kernels.md) | Three hard primitives as single fused TPC CustomOps, byte-equal to eager | depends on P1 |
| [P4a](custom/cust-phase-p4-pin-check.md) | Cheap pin check — does `c05d75a` alone unblock capture for GDN/HyperConnection? | depends on P1, **do before heavy P3** |
| [P4b](custom/cust-phase-p4-capture.md) | Serve with `--enforce-eager` removed, or documented hybrid | depends on P4a + P3 |
| [P5](custom/cust-phase-p5-moe-economics.md) | Cost-per-token curve on Gaudi 2 with the saturation point identified | depends on P4b + P2 |
| [P6](custom/cust-phase-p6-feature-parity.md) | MTP drafter, vision tower, prefix caching — product-driven, deferred | not required for text-only |

The ordering rationale is itself a decision node: the cheap pin check comes before heavy kernel authoring, because [fact-pin-c05d75a-resolves-1734](facts/fact-pin-c05d75a-resolves-1734.md) may remove part of P3's motivation for free.

---

## 4. Non-negotiables

These are pillars and decisions, not style preferences. Read the node before working around one.

- **Measured numbers beat inherited ones.** TP degree, `--max-model-len`, memory utilization, and any move to expert-parallelism come from what you measured on this 4-card box — never copied from the Gaudi 3 reference (128GB/3.7TB/s, TP4, 0.80 util). [pillar-measured-before-default](pillars/pillar-measured-before-default.md), [decision-tp-ep-measured-not-default](decisions/decision-tp-ep-measured-not-default.md)
- **Reuse over re-derivation.** PR #1829's ~2.4k-line `qwen4_exp.py` is the base. The work is retargeting, not authoring. [pillar-reuse-over-rederivation](pillars/pillar-reuse-over-rederivation.md)
- **Correctness gates speed.** A kernel is done when it is byte-equal to the eager reference on Gaudi 2. Faster-and-wrong is a bug, not an optimisation. [pillar-correctness-gates-speed](pillars/pillar-correctness-gates-speed.md)
- **Evidence and inference stay separate.** The roadmap labels which claims it sourced and which it inferred. An inference presented as a constraint is how the team plans around a wall that does not exist. [note-provenance-register](notes/note-provenance-register.md)
- **FP8 is served directly.** E4M3/E5M2 are supported on Gaudi 2: no INT8 or BF16 re-quantization fork, no INT8 re-expression of the n-gram gather. [decision-fp8-no-requantization](decisions/decision-fp8-no-requantization.md)
- **Prefix caching stays OFF until P2.1 lands.** [decision-prefix-cache-off-until-p2-1](decisions/decision-prefix-cache-off-until-p2-1.md)
- **Eager first, compiled later.** Eager is the correctness baseline; capture is the later lever. [decision-eager-first-compiled-later](decisions/decision-eager-first-compiled-later.md)
- **EP is not a default lever.** Expert parallelism is an all-to-all dispatch/combine pattern: it is feasible only if measured HCCL all2all bandwidth says so. [cust-risk-r6-hccl-all2all-bandwidth](custom/cust-risk-r6-hccl-all2all-bandwidth.md)

Runtime flags required in P0: `--kv-cache-dtype auto`, `VLLM_SKIP_WARMUP=true`, `--enforce-eager`, `--language-model-only`.

---

## 5. Risks that actually bite

| Risk | Exposure | What to do |
|---|---|---|
| [R2 — 96GB HBM pressure](custom/cust-risk-r2-hbm-side-cache-pressure.md) | high / high | P2.1 block-managed side caches; lower `--max-model-len`/util |
| [R3 — sparse top-k uncapturable](custom/cust-risk-r3-sparse-topk-uncapturable.md) | medium-high / medium | Hybrid compiled+eager for the QSA region only |
| [R4 — #1733 low-batch MoE slowness](custom/cust-risk-r4-1733-lowbatch-moe.md) | medium / high | Gathered-expert combine; compete on high concurrency only |
| [R6 — HCCL all2all bandwidth](custom/cust-risk-r6-hccl-all2all-bandwidth.md) | medium / medium-high | P0.5 benchmark; fall back to pure TP if all2all is weak |
| [R5 — no Intel roadmap for primitives](custom/cust-risk-r5-no-intel-primitive-roadmap.md) | confirmed / medium | Own it via TPC SDK + CustomOp contract |
| [R1 — Gaudi 2 FP8 throughput](custom/cust-risk-r1-fp8-mme-throughput.md) | medium / medium | P0.2 micro-benchmark; performance question, not feasibility |

Known blocker in the compiled-mode path: `synStatus-26` / synapse `compileGraph` (issue #1734 family).

---

## 6. Where things live

| Path | What it is |
|---|---|
| `qwen4_exp_gaudi2_roadmap.json` | Human-owned working roadmap. Never edit it from an agent session. |
| `raw/processed/` | Immutable source copies. Never edit, never delete. |
| `_system/INDEX.md` | Agent entry point: every node with summary and edge count. |
| `_system/AGENTS.md` | Full operating rules, including the grounding protocol. |
| `_system/SEED-MANIFEST.md` | Id registry — the roadmap→node mapping and required edges. |
| `_system/FRONTMATTER-SCHEMA.md` | The node schema, including the reduced `log` schema. |
| `_system/lint_vault.py` | Graph validator + index generator. Run it before committing vault changes. |
| `logs/` | One immutable log node per skill execution; never indexed. |

Skills available as slash commands (`.claude/skills/`): `/convert-note`, `/query-vault`, `/organize-vault`, `/vault-health`, `/init-vault`. Agents without slash commands read the skill file and follow it — the text is the contract either way.

---

## 7. Working rules

1. **Never edit `raw/`, `raw/processed/`, or the root roadmap JSON.** New source material goes into `raw/` as a new dated file, then `/convert-note`.
2. **Every node you create has at least one real edge** to an existing node, and gets a row in `_system/INDEX.md`.
3. **Do not invent numbers.** If the roadmap does not state it and you have not measured it, it is a `question` or a low-confidence `hypothesis`, never a `fact`.
4. **`verified_at` means measured.** A document is not verification. Nothing seeded in this vault is verified.
5. **A measurement is an event.** When a benchmark finishes, write the number into a `fact-*` node, adjust the `hyp-*` nodes it settles, and let the risks that hung off those hypotheses update through their edges. Then log it.
6. **Run the linter** (`python _system/lint_vault.py`) after any vault edit; an unresolved edge target silently breaks traversal for whoever comes next.

---

## 8. What is known to be unknown

The vault carries five open questions that block specific decisions — context length and TP degree fit ([question-what-tp-degree-fits-gaudi2](questions/question-what-tp-degree-fits-gaudi2.md)), which subgraphs still fail capture ([question-which-subgraphs-fail-capture](questions/question-which-subgraphs-fail-capture.md)), where cost-per-token saturates ([question-moe-saturation-point](questions/question-moe-saturation-point.md)), HCCL per-primitive caveats ([question-hccl-primitive-caveats](questions/question-hccl-primitive-caveats.md)), and whether an HPU MTP drafter pays for itself ([question-mtp-drafter-on-hpu](questions/question-mtp-drafter-on-hpu.md)).

Nothing in this project has been measured on Gaudi 2 hardware yet. P0 exists to change that.
