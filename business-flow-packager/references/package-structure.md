# Shareable Business Flow Package Structure

Use a two-level structure for GitHub sharing:

```text
repo-root/
├── README.md
├── .gitignore
├── docs/
│   └── operator-guide.md
├── examples/
│   └── README.md
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
        ├── exports/
        ├── logs/
        ├── notes/
        ├── panel/
        ├── release/
        └── backup/
```

For a single-flow repo, the flow folder may be the repo root, but keep `flow_spec.md` and `run_contract.md` separate.

## Lifecycle Pattern

Borrow the lifecycle shape from project-based repos:

- `sources/`: original or normalized source materials. Do not include private customer files in a public repo.
- `notes/`: analysis, operator notes, and decision records.
- `scripts/`: runnable automation code.
- `config/`: example config only; real `.env` and credentials stay local and ignored.
- `exports/`: generated outputs. Usually ignored unless they are safe examples.
- `logs/`: runtime logs. Ignore by default.
- `backup/`: rollback snapshots. Ignore by default.
- `release/`: generated app/exe/package artifacts. Ignore by default unless publishing a release asset intentionally.

## Flow Spec

`flow_spec.md` is human-readable:

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

- Command and cwd
- Runtime dependencies
- Required env vars or config files
- Idempotency behavior
- Locks and conflict groups
- Dry-run mode
- Logs
- Verification checks
- Rollback or cleanup steps

## Optimization From The Reference Structure

Project/example repos often separate in-progress work from shareable examples. Apply that here:

- Keep real customer/business runs under `flows/<name>/` or a private worktree.
- Move sanitized demo flows to `examples/` only after secrets and private data are removed.
- Keep a locked execution contract (`run_contract.md`) beside the script so future agents do not drift from the verified command.
