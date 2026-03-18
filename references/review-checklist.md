# Review Checklist

Use this checklist before final delivery of a complex n8n workflow.

## Structural Checks

- The workflow has a clear primary trigger.
- Every non-trigger node has an intended inbound path.
- Node names are unique and readable.
- The `connections` object matches exact node names.
- Webhook request-response flows end with `Respond to Webhook`.

## Logic Checks

- Required fields are validated before downstream writes.
- Branching rules match the user's logic chain.
- Error paths are separated from happy-path processing.
- Expensive or rate-limited calls are batched or throttled.
- Approvals and waits are explicit, not implied.

## Maintainability Checks

- Simple transforms do not rely on unnecessary `Code` nodes.
- External side effects happen after validation.
- The canvas layout is readable from left to right.
- Assumptions are stated clearly.
- Credentials are not fabricated.
