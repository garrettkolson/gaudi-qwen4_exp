# Local Custom Types

This file documents any `custom` node types created for domain-specific needs that fall outside the 16 canonical types defined in `NODE-TYPES.md`.

---

## Registration Format

To add a custom type, create an entry below with:

- **Type name:** lowercase, singular (e.g., `product`, `metric`)
- **Folder:** `custom/` (all custom types go here)
- **Rationale:** why the 16 canonical types don't fit
- **Usage scope:** which namespace(s) use this type

---

## Registered Local Types

### roadmap-phase

- **Type name:** `roadmap-phase`
- **Folder:** `custom/`
- **Node `type`:** `custom` (always) — the subtype is carried by the tag `roadmap-phase` and the id prefix `cust-phase-`
- **Rationale:** A roadmap phase is neither a `decision` (it is a bounded body of work, not a choice) nor a `task` (it decomposes into many tasks) nor a `playbook` (it is goal-and-exit-criteria shaped, not a repeatable procedure). It needs its own container holding a goal, a gating flag, dependencies, task decomposition, and exit criteria.
- **Usage scope:** `qwen4-exp-gaudi2`
- **Required body sections:** `Goal`, `Depends on`, `Tasks` (wikilinks to `task-*` nodes), `Exit criteria`. Gating phases state `Gating: yes`.
- **Required tags:** `roadmap-phase`, plus the phase id (e.g. `p0`) and `gating` where applicable.
- **Typical edges:** `depends_on` (predecessor phases), `preceded_by` / `followed_by` (recommended order), `supports`/`related_to` toward the `pillar-*` nodes the phase operationalises.

### roadmap-risk

- **Type name:** `roadmap-risk`
- **Folder:** `custom/`
- **Node `type`:** `custom` (always) — the subtype is carried by the tag `roadmap-risk` and the id prefix `cust-risk-`
- **Rationale:** A delivery risk is a probability/impact pair with a mitigation. `hypothesis` claims something testable is true; a risk claims something harmful may happen and names what reduces it. The distinction matters for retrieval: queries about "what could hurt us" want risks, queries about "what should we test" want hypotheses.
- **Usage scope:** `qwen4-exp-gaudi2`
- **Required body sections:** `Exposure` (probability × impact, as stated in the roadmap), `Mitigation`, `Trigger to watch`.
- **Required tags:** `roadmap-risk`, plus the risk id (e.g. `r1`) and its probability (`confirmed`, `high`, `medium-high`, `medium`, `low`).
- **Typical edges:** `related_to` the `cust-phase-*` nodes the risk threatens, `derived_from` the `source-*` node it came from, `depends_on` a `hyp-*` node when the risk's likelihood is itself untested, `supports`/`contradicts` the `question-*` that would resolve it.

---

*Registered 10/15/2026 during the seed build. Both types exist only in the `qwen4-exp-gaudi2` namespace.*
