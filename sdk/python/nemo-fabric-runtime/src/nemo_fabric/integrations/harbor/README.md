<!--
SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Harbor Integration

Use `nemo_fabric.integrations.harbor:FabricAgent` to run NVIDIA NeMo Fabric
adapters in Harbor tasks. Harbor options select the model, harness, skills, MCP
servers, tool policy, and telemetry; `FabricAgent` translates them into one
typed `FabricConfig` for the task run.

Harbor's `skills_dir` is a task-side collection containing `<skill_name>/SKILL.md` directories. The task runner expands its immediate entries into individual Fabric skill paths in name order, preserving explicit `config.skills.paths` and avoiding duplicate paths. An empty collection adds no skills. Missing collections and entries without a regular `SKILL.md` file fail before harness execution; skill contents are still validated by the selected adapter. Collection paths are resolved inside the task environment, relative to `fabric_config_base_dir` when not absolute, never through the host filesystem. Use matching Fabric versions on the host and in the task environment for this transport contract.

Refer to the [Harbor example](../../../../../../../examples/harbor/README.md)
for runnable SWE-Bench commands, configuration variations, reward checks, and
Relay artifacts.
