# Local Office Delivery Checklist

Use this before packaging a workflow for office users or another computer.

## Required Files

- `README.md` with purpose, install, run, verify, and troubleshooting notes.
- `flow_spec.md` and `run_contract.md`.
- Example config such as `config/example.env`, never a real `.env`.
- A smoke test or dry-run command.

## README Shape

Keep it operator-focused:

1. What this workflow automates.
2. What files, systems, or pages it touches.
3. What the user needs to install or configure.
4. How to run it.
5. How to verify the output.
6. What to do when it fails.
7. Where logs and outputs are written.

## Safety Scan

Run targeted checks before handing the package to another user:

```bash
find <package> -name '.env' -o -iname '*token*' -o -iname '*secret*' -o -iname '*cookie*' -o -iname '*credential*'
rg -n --hidden --glob '!.git' --glob '!*.md' '(AKIA|BEGIN [A-Z ]*PRIVATE KEY|password\\s*=|token\\s*=|secret\\s*=|cookie\\s*=)' <package>
```

Review hits manually. Do not include browser profiles, cookies, real credentials, customer data, or private exports unless the user explicitly confirms they belong in the package.

## Office User Fit

Prefer:

- One visible run command.
- Clear output location.
- Dry-run or smoke-test mode.
- Plain-language error messages.
- Desktop/app/panel entry when useful.

Avoid:

- Requiring users to edit source code.
- Requiring terminal-only setup when the target user expects a button/app.
- Hardcoded personal paths in colleague-facing packages.
