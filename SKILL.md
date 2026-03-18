---
name: n8n-workflow-builder
description: Generate, refactor, and optimize importable n8n workflow JSON from plain-language logic chains, automation requirements, app integrations, branching rules, payload schemas, or existing workflow exports. Use when Codex needs to turn a user's business process into a complete n8n workflow, improve an existing n8n JSON export, redesign node relationships, add retries or error handling, reduce unnecessary Code nodes, or produce a cleaner, more maintainable n8n canvas with better triggers, routing, batching, approvals, notifications, and webhook behavior.
---

# N8n Workflow Builder

Turn a user's natural-language process description into production-minded n8n workflow JSON. Prefer a clean node graph, explicit data contracts, readable naming, and import-safe output over fast but fragile node dumping.

## Operating Modes

Choose the lightest mode that satisfies the request:

1. New build
   - Create a workflow from a logic chain, requirements list, SOP, or product idea.
2. Refactor
   - Improve an existing n8n JSON workflow without changing the user's core business outcome.
3. Repair
   - Fix broken connections, unclear routing, missing validation, or weak error handling in an existing workflow.
4. Upgrade
   - Replace overused `Code` nodes with clearer built-in nodes when practical.

## Intake Checklist

Distill the request into this planning canvas before writing JSON:

- business goal
- trigger type
- source systems
- destination systems
- input payload shape
- output or side effects
- routing rules
- validation rules
- retries, throttling, and batching needs
- async waits or approval steps
- failure notifications
- observability or summary reporting

If details are missing, make safe assumptions and state them. Ask follow-up questions only when the missing choice would materially change credentials, production side effects, compliance posture, or a critical business rule.

## Workflow Construction Rules

1. Prefer built-in or first-party n8n nodes.
2. Use `HTTP Request` when a suitable built-in node does not exist.
3. Avoid community nodes unless the user explicitly asks for them.
4. Normalize fields immediately after the trigger with `Set`, mapping, or a minimal transform node.
5. Use `IF`, `Switch`, `Merge`, `Split In Batches`, `Wait`, `Loop Over Items`, and `Respond to Webhook` deliberately before reaching for `Code`.
6. Use `Code` only when expression syntax or built-in nodes would become less readable than a short scripted transform.
7. Put external side effects after validation and routing, not before.
8. Add resilience only where it improves the business flow: retries, deduplication, rate-limit waits, approval pauses, failure alerts, and summary notifications.

## Node Design Standards

- Keep node names unique, short, and action-oriented.
- Prefer ASCII-only names for portability.
- Use stable string IDs.
- Keep one responsibility per node.
- Lay out the happy path from left to right.
- Keep rejection, fallback, and failure branches visually separate on the lower side of the canvas.
- Start with one primary trigger unless the workflow truly needs multiple entry points.
- End request-response webhook flows with `Respond to Webhook`.

## Output Contract

Produce the final answer in this order unless the user explicitly asks for JSON only:

1. short architecture summary
2. assumptions
3. one complete fenced `json` block containing the workflow
4. brief import notes covering credentials, environment variables, webhook paths, schedules, or post-import setup

JSON rules:

- Return a full workflow object, not pseudocode.
- Include top-level `name`, `nodes`, `connections`, and `settings`.
- For each node, include at least `id`, `name`, `type`, `typeVersion`, `position`, and `parameters`.
- Keep `connections` aligned with the exact source node names.
- Do not invent credential IDs.
- Use placeholders only where the user must supply environment-specific values.
- Do not include comments inside JSON.

## Optimization Heuristics

Apply these when they improve clarity or reliability:

- collapse trivial transform-only `Code` nodes into `Set` or expressions
- batch fan-out API calls before rate-limited services
- validate required fields before external writes
- add idempotent lookup or upsert keys where duplicates are likely
- add one operational summary or alert path for workflows with business impact
- preserve user intent while simplifying node count and connection complexity

## Existing Workflow Edits

When the user provides an existing workflow JSON:

- preserve working logic unless the user asks for a redesign
- keep credential references untouched unless the user asks to change them
- avoid renaming nodes that are still semantically correct unless readability clearly improves
- explain structural changes briefly before returning the updated JSON

## Validation

- If the workflow JSON is written to disk, run `scripts/validate_workflow.py <path-to-json>`.
- Treat validation warnings as prompts to review layout or flow quality, not always as blockers.
- Fix all structural validation errors before delivery.

## References

- Read `references/n8n-workflow-patterns.md` for node selection and connection structure.
- Read `references/request-template.md` when shaping a user's rough idea into a complete n8n build request.
- Read `references/review-checklist.md` before finalizing a complex workflow.
- Use `scripts/validate_workflow.py` for a local sanity check on generated JSON files.
