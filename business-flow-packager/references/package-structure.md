# Office Business Flow Package Structure

Use this structure for office-friendly local handoff packages:

```text
package-root/
├── README.md
├── .gitignore
├── docs/
│   └── operator-guide.md
└── flows/
    └── flow-name/
        ├── README.md
        ├── flow_spec.md
        ├── run_contract.md
        ├── sources/
        ├── scripts/
        ├── config/
        │   └── example.env
        ├── tests/
        ├── confirm_ui/
        ├── exports/
        ├── logs/
        ├── notes/
        ├── panel/
        ├── release/
        └── backup/
```

For a single-flow package, the flow folder may be the package root, but keep `flow_spec.md` and `run_contract.md` separate.

## Lifecycle Pattern

Borrow the lifecycle shape from project-based workspaces:

- `sources/`: original or normalized source materials. Do not include private customer files in a colleague handoff package unless explicitly approved.
- `notes/`: analysis, operator notes, and decision records.
- `scripts/`: runnable automation code.
- `config/`: example config only; real `.env` and credentials stay local and ignored.
- `confirm_ui/`: optional `recommendations.json` and `result.json` for bundled user confirmation.
- `exports/`: generated outputs. Usually ignored unless they are safe examples.
- `logs/`: runtime logs. Ignore by default.
- `backup/`: rollback snapshots. Ignore by default.
- `release/`: generated app/exe/package artifacts. Ignore by default unless publishing a release asset intentionally.

## Flow Spec

`flow_spec.md` is human-readable:

- Session evidence: source thread/session, successful run summary, files touched, outputs verified, and known gaps
- Purpose
- Operator
- Trigger condition
- Inputs
- Source systems
- Outputs
- Manual assumptions
- Data sensitivity
- Known non-goals

## Run Contract

`run_contract.md` is the execution contract:

- Session evidence anchor
- Confirmation result path, if a browser confirmation was used
- Command and cwd
- Runtime dependencies
- Required env vars or config files
- Idempotency behavior
- Locks and conflict groups
- Dry-run mode
- Logs
- Verification checks
- Rollback or cleanup steps

## Office Handoff

Separate private working state from colleague-facing files:

- Keep real customer/business runs under `flows/<name>/` or a private worktree.
- Move sanitized samples to `docs/` or `sources/sample/` only after secrets and private data are removed.
- Keep a locked execution contract (`run_contract.md`) beside the script so future agents do not drift from the verified command.
