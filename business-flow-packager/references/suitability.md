# Scriptability Suitability Gate

Use this reference before writing code when the workflow touches external systems, credentials, browser sessions, paid services, production data, human judgment, or unclear outputs.

## Script It When

- The workflow is repeated or likely to be reused.
- Inputs can be listed as files, dates, URLs, IDs, env vars, or operator prompts.
- Outputs can be verified as files, database rows, API responses, dashboard state, sent messages, or logs.
- Required credentials or sessions already exist locally, or the user can supply them through a standard secure mechanism.
- Human decisions can be turned into parameters, config, review checkpoints, or explicit "manual approval required" stops.
- The failure modes can be made visible with logs and non-zero exit codes.
- The script can be tested with a dry-run, fixture, read-only mode, or a cheap real run.

## Do Not Script Yet When

- The user cannot state the desired output or success criteria.
- The workflow depends on subjective judgment that cannot be parameterized.
- It requires CAPTCHA, one-time codes, phone approval, or a human-in-the-loop login every run.
- It relies on unstable screen coordinates with no accessible DOM/API/file fallback.
- It would expose secrets, private customer files, cookies, browser profiles, or regulated data in a shareable package.
- It changes production systems and there is no dry-run, sandbox, backup, or rollback path.
- It depends on Mac-only apps but the requested target is Windows exe, or vice versa, and no portable fallback exists.
- The only evidence is a vague verbal process and no local files, logs, exports, or command history can be found.

## Response For Unsuitable Workflows

Be direct and concrete:

1. State that the workflow should not be scripted yet.
2. Name the blocking reason.
3. List the exact missing evidence or decision.
4. Offer the smallest next step that would make it scriptable.

Example:

```text
这个流程现在不适合做成一键脚本：最后一步需要人工判断截图内容是否合格，而且没有可校验的文件/API 输出。要继续，需要先定义合格规则，或把这一步改成“脚本生成候选结果，用户确认后再提交”。
```

## Risk Levels

- Low: local file transforms, report generation, read-only summaries, deterministic format conversion.
- Medium: authenticated downloads, browser exports, spreadsheet updates, scheduled jobs, panel buttons.
- High: production writes, payments, messaging users, bulk deletes, private data packaging, credential migration.

For medium/high risk workflows, require a run contract with dry-run behavior, logs, idempotency notes, and verification steps.
