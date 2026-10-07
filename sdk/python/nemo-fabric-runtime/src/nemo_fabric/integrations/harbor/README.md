<!--
SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Harbor Integration

Use `nemo_fabric.integrations.harbor:FabricAgent` to run NVIDIA NeMo Fabric
adapters in Harbor tasks. Harbor options select the model, harness, skills, MCP
servers, tool policy, and telemetry; `FabricAgent` translates them into one
typed `FabricConfig` for the task run.

Refer to the [Harbor example](../../../../../../../examples/harbor/README.md)
for runnable SWE-Bench commands, configuration variations, reward checks, and
Relay artifacts.

The integration projects normalized `RunResult.usage` into Harbor's `AgentContext` without requiring NeMo Relay or ATIF. Harbor input counts include cache: inclusive NeMo Fabric input is copied unchanged, while exclusive input is combined with cache only when both counts are known. If input semantics are unknown, Harbor input remains unknown unless the adapter explicitly reports zero cache tokens. Legacy results remain valid, but their input count needs explicit cache semantics or an ATIF fallback to populate Harbor's inclusive count; the original values remain in result metadata. Unknown counts and costs remain `None`; estimates are not promoted to reported cost. ATIF metrics fill only missing fields and are never added to normalized usage. The same collection path applies to unsuccessful results that contain usage.
