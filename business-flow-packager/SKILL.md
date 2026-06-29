---
name: business-flow-packager
description: Package a business workflow that an AI session has already successfully executed into one-click scripts, script-panel buttons, macOS apps, Windows exe launchers, and GitHub-ready delivery folders. Use when the user asks to turn "刚才/上次/这个 session 跑通的流程", a completed AI-assisted business process, spreadsheet/report/export routine, browser operation, CLI sequence, or "业务流/一键打包/脚本面板/做成脚本/做成 app/exe/分享到 GitHub" request into a reusable automation, or when deciding that a previously executed workflow is not suitable for scripting and explaining why.
---

# Business Flow Packager

Turn a concrete workflow that has already been run successfully by AI into a durable local automation. Treat the successful session as the source of truth: commands actually run, files touched, manual decisions, outputs, logs, and verification evidence. Do not infer a workflow only by scanning a document path; use filesystem inspection only to verify and package what the session already proved.

## Workflow

1. Locate the successful session before designing anything:
   - If the user says "刚才这个流程", use the current conversation and tool history as the authoritative run record.
   - If the user references a previous thread/session, inspect that thread/session record or ask for the session link/title only if it cannot be located.
   - Extract actual steps, commands, cwd values, scripts, files changed, files read, URLs, browser actions, manual choices, outputs, and verification checks.
   - Mark anything that was guessed, manually decided, or not captured in the session as a gap; do not silently convert gaps into script logic.
2. Inspect only the files that the session evidence points to:
   - Read the scripts, configs, logs, exports, spreadsheets, app folders, and launchers touched by the successful run.
   - Use `scripts/flow_probe.py --paths <path...> --output <json> --markdown <md>` only as a supporting inventory for known paths, not as the primary way to discover the workflow.
   - If the user only provides a directory and no successful session, explain that the skill needs a run-through/session record or offer to run the workflow once first.
3. Decide scriptability before writing code:
   - Read `references/suitability.md` when the workflow has human judgment, credentials, browser state, external systems, destructive writes, or unclear outputs.
   - Continue only when inputs, outputs, credentials/session state, success checks, and failure behavior can be made explicit.
   - If unsuitable, tell the user the blocking reason and the smallest change that would make it scriptable.
4. Lock the workflow contract:
   - Capture `flow_spec.md`: purpose, operator inputs, source systems, output files, manual assumptions, and owner notes.
   - Capture `run_contract.md`: command, cwd, environment variables, idempotency rules, locks, logs, dry-run behavior, and verification checks.
   - Include a "Session Evidence" section listing the source session/thread and the exact evidence used.
   - Use `scripts/make_flow_package.py` to scaffold a shareable flow package when creating a new reusable workflow folder.
5. Build the smallest reliable script:
   - Prefer the existing project language and helpers.
   - Add dry-run or fixture mode for data-changing or external-system workflows.
   - Avoid hardcoded personal paths except for machine-local panel entries; for shareable packages use config files, env vars, or documented path discovery.
   - Do not request credentials before checking local auto-login/session scripts and existing env/config paths.
6. Validate the automation:
   - Run syntax checks and cheap dry-run/fixture tests.
   - Verify outputs by inspecting actual files, API responses, logs, workbook sheets, or UI state as appropriate.
   - Do not run long, destructive, or production-changing jobs solely to test packaging unless the user asked for execution.
7. Confirm launcher placement with the user:
   - After the script exists and is verified, summarize candidate commands and ask which ones should be added to the script panel.
   - If the user confirms panel integration, use `$add-script-to-panel`; do not modify that skill.
   - For the user's macOS panel, inspect `~/script-manager/commands.json` and validate `http://127.0.0.1:8787/api/commands`.
8. Package for the target platform:
   - For macOS, prefer an app wrapper around the verified command when the user asks for app form.
   - For Windows, create a `.exe` launcher/build recipe only when the workflow can run without Mac-only dependencies.
   - Read `references/platform-and-panel.md` before adding launchers or app/exe packaging.
9. Prepare GitHub sharing:
   - Include a root `README.md`, a minimal `.gitignore`, example config, and explicit install/run/verify steps.
   - Keep private exports, secrets, cookies, tokens, browser profiles, `.env`, and customer data out of the repo.
   - Read `references/github-release.md` before pushing or syncing.

## Resource Map

- `scripts/flow_probe.py`: read-only inventory of workflow folders, candidate scripts, configs, recent outputs, risk flags, and local script-panel state.
- `scripts/make_flow_package.py`: scaffold a reusable business-flow package with `flow_spec.md`, `run_contract.md`, `scripts/`, `config/`, `docs/`, `tests/`, `exports/`, `logs/`, and `release/`.
- `references/session-evidence.md`: how to extract a reusable workflow from a completed AI session.
- `references/suitability.md`: decision gate for "script it" vs "do not script it".
- `references/package-structure.md`: recommended shareable package layout, adapted from project/example lifecycle patterns.
- `references/platform-and-panel.md`: script panel, macOS app, and Windows exe packaging rules.
- `references/github-release.md`: GitHub-ready README, safety checks, and sync steps.

## Hard Rules

- Do not modify the `add-script-to-panel` skill; invoke it only when panel integration is confirmed.
- Do not infer the workflow from static documents alone; require a successful session/run record or run the workflow once first.
- Do not hide uncertainty by generating a script that depends on unverified manual behavior.
- Do not push or package secrets, private exports, tokens, cookies, browser profiles, or customer data.
- Do not overwrite user files without a backup or explicit confirmation.
- Do not call a workflow "done" until the created script/package and its verification evidence exist.
