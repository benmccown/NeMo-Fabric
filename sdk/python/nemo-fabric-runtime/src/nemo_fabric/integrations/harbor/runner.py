# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Run the Fabric SDK inside a Harbor task environment."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from nemo_fabric import Fabric
from nemo_fabric import RunResult
from nemo_fabric.integrations.harbor.models import FabricRunPayload
from nemo_fabric.integrations.harbor.telemetry import publish_telemetry_evidence


async def run(payload: FabricRunPayload) -> RunResult:
    config = payload.config.model_copy(deep=True)
    if payload.skills_dir is not None:
        root = Path(payload.skills_dir)
        if not root.is_absolute():
            root = Path(payload.config_base_dir) / root
        if not root.is_dir():
            raise ValueError(
                f"Harbor skills collection must be an existing task-side directory: {root}"
            )
        skills = sorted(root.iterdir())
        for skill in skills:
            if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                raise ValueError(
                    "Harbor skills collection entries must be directories "
                    f"containing SKILL.md: {skill}"
                )
        for skill in skills:
            config.add_skill_path(skill)
    result = await Fabric().run(
        config,
        base_dir=payload.config_base_dir,
        request=payload.request,
    )
    publish_telemetry_evidence(
        result,
        Path(payload.logs_dir),
        harbor_session_id=payload.request.context.get("harbor_session_id"),
        harbor_context_id=payload.request.context.get("harbor_context_id"),
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    payload = FabricRunPayload.model_validate_json(
        args.spec.read_text(encoding="utf-8")
    )
    result = asyncio.run(run(payload))
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result.to_mapping(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
