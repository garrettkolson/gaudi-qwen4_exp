---
id: ref-vllm-gaudi-plugin
title: "vllm-gaudi Plugin"
type: reference
namespace: qwen4-exp-gaudi2
visibility: public
summary: "The HabanaAI vLLM plugin supplying the HPU backend; target version 0.30.0, the base the Qwen4Exp port, MoE combine and decode-bucket behaviour hang off."
auto_inject: false
applicable_when: "When selecting a plugin version or locating plugin source paths (models, model runner, ops) for the port"
confidence: 0.85
verified_at: "Empty"
verified_by: "Empty"
staleness_signal: "If the installed plugin is not 0.30.0, or vllm_gaudi/models/qwen4_exp.py, hpu_model_runner.py and extension/ops.py no longer exist at the pinned tag, this reference no longer describes the plugin"
tags: ["vllm-gaudi", "plugin", "hpu-backend", "release-notes", "version-pin"]
edges: [
  {"target": "fact-target-stack-versions", "type": "related_to", "weight": 0.9, "note": "The stack names plugin 0.30.0 as the target release this reference points at"},
  {"target": "source-vllm-gaudi-release-notes", "type": "related_to", "weight": 0.85, "note": "v0.24.0 to v0.30.0 release notes are the cited grounding for the feature list below"},
  {"target": "fact-plugin-0-30-0-features", "type": "related_to", "weight": 0.9, "note": "Gathered-expert MoE combine and clamped decode buckets are the two 0.30.0 features P2 and P5 depend on"},
  {"target": "cust-phase-p1-reuse-pr1829", "type": "related_to", "weight": 0.85, "note": "P1 is a retarget inside this plugin's tree, not a change to upstream vLLM"}
]
related: ["[[fact-target-stack-versions]]", "[[fact-plugin-0-30-0-features]]", "[[task-p1-3-retarget-pin-to-0-30-0]]"]
source_url: "Empty"
---

# vllm-gaudi Plugin

The vllm-gaudi plugin is the HabanaAI vLLM backend for Gaudi accelerators. It supplies the HPU model runner (`hpu_model_runner.py`), HPU-specific model implementations under `vllm_gaudi/models/`, and the low-level op layer in `extension/ops.py`. The roadmap targets plugin 0.30.0 and treats this tree as where the Qwen4Exp port lives: PR #1829's `qwen4_exp.py` is a plugin file, the runner hook `maybe_set_mamba_kv_cache_groups_ids` is plugin code, and the FP8 MoE block-grid fix `_effective_moe_block_size` is a plugin-side patch to carry forward. Release notes v0.24.0 through v0.30.0 are cited by the roadmap as grounding TPC-native `causal_conv1d`, FP8/INC stability, the opt-in gathered-expert MoE combine, and decode buckets clamped to physical KV size.

Before relying on this: confirm 0.30.0 is a published release that installs against Suite 1.24.2 and PyTorch 2.13, confirm the named paths and symbols still exist at that tag, and check the feature claims against the actual release notes rather than this summary.
