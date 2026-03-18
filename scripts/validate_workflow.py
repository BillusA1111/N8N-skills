#!/usr/bin/env python3
"""
Basic validator for importable n8n workflow JSON.

Checks:
- root object shape
- required top-level fields
- node name uniqueness
- source and target connection references
- basic node field presence

This is a lightweight sanity check, not a full n8n schema validator.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def load_workflow(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        if len(data) != 1 or not isinstance(data[0], dict):
            raise ValueError("expected one workflow object or a single-item workflow array")
        data = data[0]
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a JSON object")
    return data


def is_trigger_node(node_type: str) -> bool:
    lowered = node_type.lower()
    return (
        "trigger" in lowered
        or lowered.endswith(".webhook")
        or lowered.endswith(".chattrigger")
    )


def validate_workflow(workflow: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    required_fields = ("name", "nodes", "connections", "settings")
    for field in required_fields:
        if field not in workflow:
            errors.append(f"missing top-level field: {field}")

    nodes = workflow.get("nodes")
    connections = workflow.get("connections")
    settings = workflow.get("settings")

    if not isinstance(workflow.get("name"), str) or not str(workflow.get("name")).strip():
        errors.append("top-level 'name' must be a non-empty string")

    if not isinstance(nodes, list):
        errors.append("top-level 'nodes' must be a list")
        return errors, warnings
    if not isinstance(connections, dict):
        errors.append("top-level 'connections' must be an object")
        return errors, warnings
    if not isinstance(settings, dict):
        errors.append("top-level 'settings' must be an object")
        return errors, warnings
    if not nodes:
        errors.append("workflow must contain at least one node")
        return errors, warnings

    node_names: list[str] = []
    node_ids: list[str] = []
    node_types: dict[str, str] = {}
    incoming = Counter()
    outgoing = Counter()
    trigger_count = 0

    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"node[{index}] must be an object")
            continue

        for field in ("id", "name", "type", "typeVersion", "position", "parameters"):
            if field not in node:
                errors.append(f"node[{index}] is missing field: {field}")

        name = node.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"node[{index}] must have a non-empty string name")
            continue
        node_names.append(name)
        node_types[name] = str(node.get("type", ""))
        node_id = node.get("id")
        if isinstance(node_id, str) and node_id.strip():
            node_ids.append(node_id)

        position = node.get("position")
        if not (
            isinstance(position, list)
            and len(position) == 2
            and all(isinstance(value, (int, float)) for value in position)
        ):
            warnings.append(f"node '{name}' should have a numeric [x, y] position")

        if is_trigger_node(node_types[name]):
            trigger_count += 1

    duplicates = [name for name, count in Counter(node_names).items() if count > 1]
    for name in duplicates:
        errors.append(f"duplicate node name: {name}")

    duplicate_ids = [node_id for node_id, count in Counter(node_ids).items() if count > 1]
    for node_id in duplicate_ids:
        errors.append(f"duplicate node id: {node_id}")

    known_names = set(node_names)

    for source_name, bundles in connections.items():
        if source_name not in known_names:
            errors.append(f"connections reference unknown source node: {source_name}")
            continue
        if not isinstance(bundles, dict):
            errors.append(f"connections['{source_name}'] must be an object")
            continue

        for bundle_type, branches in bundles.items():
            if not isinstance(branches, list):
                errors.append(
                    f"connections['{source_name}']['{bundle_type}'] must be a list"
                )
                continue

            for branch_index, branch in enumerate(branches):
                if not isinstance(branch, list):
                    errors.append(
                        f"connections['{source_name}']['{bundle_type}'][{branch_index}] must be a list"
                    )
                    continue

                for edge_index, edge in enumerate(branch):
                    if not isinstance(edge, dict):
                        errors.append(
                            "connection edge at "
                            f"'{source_name}'/{bundle_type}/{branch_index}/{edge_index} must be an object"
                        )
                        continue

                    target_name = edge.get("node")
                    if not isinstance(target_name, str) or target_name not in known_names:
                        errors.append(
                            f"connection from '{source_name}' points to unknown target node: {target_name}"
                        )
                        continue

                    outgoing[source_name] += 1
                    incoming[target_name] += 1

                    edge_type = edge.get("type")
                    if edge_type is None:
                        warnings.append(
                            f"connection from '{source_name}' to '{target_name}' should include a type"
                        )
                    elif edge_type != bundle_type:
                        warnings.append(
                            f"connection from '{source_name}' to '{target_name}' uses type '{edge_type}' under '{bundle_type}'"
                        )

                    edge_output_index = edge.get("index")
                    if not isinstance(edge_output_index, int):
                        warnings.append(
                            f"connection from '{source_name}' to '{target_name}' should include an integer index"
                        )

    if trigger_count == 0:
        warnings.append("workflow does not appear to contain a trigger node")
    elif trigger_count > 1:
        warnings.append("workflow contains multiple trigger-like nodes; verify multi-entry design is intentional")

    for name in node_names:
        node_type = node_types.get(name, "")
        if incoming[name] == 0 and outgoing[name] == 0:
            warnings.append(f"node '{name}' is isolated")
        elif incoming[name] == 0 and not is_trigger_node(node_type):
            warnings.append(
                f"node '{name}' has no incoming connection and does not look like a trigger"
            )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a basic n8n workflow JSON file")
    parser.add_argument("workflow_json", help="Path to the workflow JSON file")
    args = parser.parse_args()

    path = Path(args.workflow_json)
    if not path.is_file():
        print(f"[ERROR] File not found: {path}")
        return 1

    try:
        workflow = load_workflow(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 1

    errors, warnings = validate_workflow(workflow)

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")

    if errors:
        return 1

    print("[OK] Workflow passed basic sanity checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
