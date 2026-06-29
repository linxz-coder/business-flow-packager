# GitHub Release Checklist

Use this before pushing or syncing a packaged workflow or this skill to GitHub.

## Required Files

- `README.md` with purpose, install, run, verify, and safety notes.
- `.gitignore` that excludes secrets, logs, exports, browser profiles, caches, and build outputs.
- Example config such as `config/example.env`, never a real `.env`.
- License only when the user wants the package to be open source.

## README Shape

Keep it operator-focused:

1. What this package automates.
2. What systems/files it touches.
3. Install steps.
4. Configuration.
5. Run commands.
6. Verification.
7. Panel/app/exe packaging notes.
8. Data and secrets policy.

## Pre-Push Safety Scan

Run targeted checks before publishing:

```bash
find <repo> -name '.env' -o -iname '*token*' -o -iname '*secret*' -o -iname '*cookie*' -o -iname '*credential*'
rg -n --hidden --glob '!.git' --glob '!*.md' '(AKIA|BEGIN [A-Z ]*PRIVATE KEY|password\\s*=|token\\s*=|secret\\s*=|cookie\\s*=)' <repo>
```

Review any hit manually. Do not publish private business exports unless the user explicitly confirms they are safe to share.

## Syncing To GitHub

For this user's `linxz-coder` GitHub repos, prefer:

```bash
'/Users/linxiaozhong/ai_success_script_archive/原子能力-通用能力/上传文件到github/github_folder_sync.sh' --source '<local_folder>' --repo '<repo_name>'
```

Do not use delete/mirror mode unless the user explicitly asks to remove remote files absent from the local source.

Treat success as:

```text
[OK] Pushed to ...
```

If the repo does not exist or cannot be cloned over SSH, report that as the remaining blocker and keep the local package ready.
