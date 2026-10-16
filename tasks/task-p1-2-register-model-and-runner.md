---
id: task-p1-2-register-model-and-runner
title: "Register the Model Classes and Runner Hooks"
type: task
namespace: qwen4-exp-gaudi2
visibility: namespace
summary: "Register Qwen4ExpForCausalLM and Qwen4ExpForConditionalGeneration via ModelRegistry.register_model and add the architecture to maybe_set_mamba_kv_cache_groups_ids in hpu_model_runner.py."
auto_inject: false
applicable_when: "P1, after task-p1-1 has the model file in place; the model is unreachable by the engine until registration lands"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If plugin 0.30.0 renamed the registry entry point or the mamba KV cache group helper, the registration must follow the new names rather than the PR's"
tags: ["roadmap-task", "p1", "model-registry", "model-runner", "kv-cache"]
edges: [
  {"target": "cust-phase-p1-reuse-pr1829", "type": "part_of", "weight": 0.9, "note": "Without registration the model exists but cannot be served"},
  {"target": "ref-vllm-gaudi-plugin", "type": "related_to", "weight": 0.8, "note": "Both edit sites are inside the vllm-gaudi plugin, not upstream vLLM"},
  {"target": "fact-model-architecture-blocks", "type": "depends_on", "weight": 0.8, "note": "The hybrid layers are why the architecture needs the mamba KV cache group treatment"},
  {"target": "concept-kv-block-ownership", "type": "related_to", "weight": 0.7, "note": "Cache group assignment here is what later determines whether side state can be block-managed in P2"}
]
related: ["[[cust-phase-p1-reuse-pr1829]]", "[[task-p1-1-port-qwen4-exp-model]]"]
source_url: "Empty"
---

# Register the Model Classes and Runner Hooks

Register both architecture names — `Qwen4ExpForCausalLM` and `Qwen4ExpForConditionalGeneration` — through `ModelRegistry.register_model`, and add the architecture to `maybe_set_mamba_kv_cache_groups_ids` in `hpu_model_runner.py`.

Why the second half matters as much as the first: this model is a hybrid. Its linear-attention and sparse-attention layers do not share cache semantics with ordinary attention, so the runner has to know the architecture belongs in the mamba-style KV cache grouping. Register the model without that hook and it may construct happily and then fail at cache allocation, which reads like a memory bug but is a classification bug.

The `ForConditionalGeneration` variant is registered for completeness even though the text-only path uses the causal-LM class and the vision stack is out of scope for this phase; dropping it now would force a second pass when P6 revisits multimodal support.

Keep these edits separate from the model file work in version control: they touch plugin internals and are the parts most likely to conflict with a future plugin bump.

Done when: the engine resolves both architecture names and boots the causal-LM variant with the hybrid cache groups assigned, without cache-shape errors.
