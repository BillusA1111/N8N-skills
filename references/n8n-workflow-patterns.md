# n8n Workflow Patterns

Use this reference when turning user requirements into importable workflow JSON.

## Minimum Workflow Shape

According to the official n8n workflow creation docs, the workflow object should include:

- `name`
- `nodes`
- `connections`
- `settings`

Treat these as the minimum required top-level fields.

## Output Shape Rules

- Return one workflow object unless the user explicitly asks for multiple workflows.
- Keep `nodes` as an ordered array that follows the main execution path from left to right.
- Keep `connections` keyed by the exact source node name.
- Prefer one logical responsibility per node.
- Do not invent unsupported app names or community node types.

## Connection Structure

Use the standard `connections` layout:

```json
{
  "Source Node": {
    "main": [
      [
        {
          "node": "Target Node",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```

Use additional branch arrays when a node has multiple outputs, such as `IF` or `Switch`.

## Minimal Example

```json
{
  "name": "Minimal Example",
  "nodes": [
    {
      "id": "manual-trigger",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        260,
        300
      ],
      "parameters": {}
    },
    {
      "id": "normalize-input",
      "name": "Normalize Input",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        520,
        300
      ],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "user-id",
              "name": "userId",
              "value": "={{$json.userId}}",
              "type": "string"
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [
          {
            "node": "Normalize Input",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {}
}
```

## Node Choice Guide

- Use `Manual Trigger` for draft or test flows.
- Use `Schedule Trigger` for polling, reporting, cleanup, and recurring syncs.
- Use `Webhook` for inbound app events or API-style automations.
- Use app-specific trigger nodes when they reduce custom webhook or polling work.
- Use `Set` or mapping nodes to normalize fields right after the trigger.
- Use `HTTP Request` when the target service has no suitable built-in node or needs a custom API operation.
- Use `IF` for binary routing and `Switch` for multi-branch routing.
- Use `Merge` when two upstream branches need to rejoin.
- Use `Split In Batches` before rate-limited or expensive downstream steps.
- Use `Wait` for throttling, async callbacks, or approval pauses.
- Use `Respond to Webhook` when the caller expects a synchronous response.

## Reliability Checklist

- Validate required inputs before writing to third-party systems.
- Prefer idempotent identifiers for upserts, deduplication, and retries.
- Add explicit failure notifications when the workflow has business impact.
- Add batching or waits when external APIs are likely to rate-limit.
- Keep side effects near the end of the happy path.

## Assumptions to State

When the user does not provide enough detail, state assumptions about:

- the trigger type
- the target apps or APIs
- field names and payload structure
- auth placeholders
- retry behavior
- schedule cadence
- webhook response expectations

## Avoid

- orphaned nodes with no valid connections
- duplicate node names
- fake credential IDs
- unnecessary `Code` nodes for simple mapping or branching
- mixing success and failure branches into one unreadable canvas
