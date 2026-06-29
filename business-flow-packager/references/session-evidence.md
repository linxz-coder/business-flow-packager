# Session Evidence Extraction

Use this reference when packaging a workflow that an AI session has already run successfully.

## Source Of Truth

The successful session is the source of truth. Extract:

- User intent and final accepted outcome.
- Commands actually run, including cwd and environment assumptions.
- Files read, created, edited, moved, uploaded, or verified.
- Browser or app actions that affected the outcome.
- Manual decisions or confirmations made by the user.
- Output artifacts and their final paths.
- Verification evidence: tests, logs, API responses, workbook checks, screenshots, live URLs, or remote HEADs.
- Errors encountered and the recovery path that finally worked.

Do not treat a directory listing, SOP document, README, or loose notes as the workflow. Those are supporting evidence only.

## If The Session Is Current

Use the visible conversation and tool calls. Summarize a session evidence block before scripting:

```text
Session Evidence
- Source: current thread
- Successful command path:
- Files changed:
- Outputs verified:
- Manual decisions:
- Known gaps:
```

## If The Session Is Previous

Locate or request the session/thread reference. Acceptable anchors:

- Thread link or title.
- Session id.
- Date plus task name.
- A copied transcript or command log.
- The final output directory plus enough context to identify the prior run.

If the previous session cannot be located, do not fabricate the workflow from nearby files. Offer to run the workflow once with the user and then package that run.

## Packaging From Evidence

Turn the evidence into:

- `flow_spec.md`: what the workflow is for and what the operator cares about.
- `run_contract.md`: the exact reusable command, inputs, outputs, locks, logs, dry-run behavior, and verification.
- Script code: the smallest wrapper or automation that reproduces the successful path.
- Tests or smoke checks that prove the wrapper still follows the session's verified path.

## Gap Handling

Common gaps:

- A manual choice was made but not recorded.
- A browser session was already logged in but the login path is unknown.
- The final file was manually renamed.
- A message was sent manually outside the script.
- The successful run depended on a local temporary file that no longer exists.

For each gap, either parameterize it, add a manual checkpoint, inspect the missing evidence, or mark the workflow unsuitable until a clean run captures it.
