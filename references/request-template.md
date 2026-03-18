# n8n Request Template

Use this template to help the user provide enough detail for a strong workflow.

## Minimal Prompt

```text
Use $n8n-workflow-builder to generate a complete n8n workflow JSON.

Business goal:
- ...

Trigger:
- ...

Input data:
- ...

Steps:
1. ...
2. ...
3. ...

If / else rules:
- ...

Systems involved:
- ...

Success result:
- ...

Failure handling:
- ...
```

## High-Quality Prompt

```text
Use $n8n-workflow-builder to generate an optimized, importable n8n workflow JSON.

Business goal:
- When a new lead submits a form, enrich the data, score the lead, route it to the correct sales owner, and notify Slack.

Trigger:
- Webhook from website form

Input payload:
- name
- phone
- email
- company
- budget
- city

Business rules:
1. Reject requests with missing phone or email.
2. Enrich company information from an external API.
3. If budget >= 50000, route to enterprise sales.
4. If budget < 50000, route to SMB sales.
5. Send a Slack message with lead summary.
6. Return a success response to the webhook caller.

Reliability requirements:
- Avoid duplicate processing by email.
- Retry the enrichment API once on transient failure.
- If enrichment fails twice, continue with a fallback branch and notify ops.

Output requirements:
- Return complete n8n JSON only.
- Use built-in nodes where possible.
- Keep the flow readable and easy to maintain.
```

## Missing Details That Usually Matter

- exact trigger type
- expected payload fields
- side effects that must happen synchronously
- which systems are read-only vs write targets
- retry tolerance
- who should receive failure notifications
- schedule cadence and timezone
- whether the workflow is for testing or production
