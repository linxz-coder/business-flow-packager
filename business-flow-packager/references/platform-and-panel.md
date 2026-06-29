# Platform And Launcher Packaging

Read this before adding a script to a panel, creating a macOS app wrapper, or preparing a Windows exe.

## Script Panel

When the user wants a button in the local script panel:

1. Use `$add-script-to-panel` and follow its `SKILL.md`.
2. Inspect `~/script-manager/commands.json`.
3. Choose `mode: "background"` for non-interactive commands whose logs should show in the web panel.
4. Choose `mode: "terminal"` for prompts, passwords, SSH, menus, or stdin.
5. Add conflict groups for browser exports, shared output files, or script-manager packaging.
6. Validate JSON and `http://127.0.0.1:8787/api/commands`.

Do not add panel entries before the underlying script exists and has passed a cheap validation.

## macOS App Form

For macOS, prefer a small `.app` wrapper around the verified command instead of embedding business logic inside the app bundle.

Use an app wrapper when:

- The user wants Dock/Finder launch.
- The script is already verified from Terminal.
- The command can run with a stable cwd and environment.

Keep the source script outside the app bundle when it is expected to be updated. Store app build notes in `release/mac/README.md` or `panel/README.md`.

On this user's machine, check existing helpers in `~/script-manager`, including:

- `create_macos_app.py`
- `install_on_mac.py`
- `~/Applications/脚本面板.app`

## Windows Exe Form

For Windows, only promise an exe when the workflow is portable:

- No AppleScript, Finder, Keychain, LaunchAgent, macOS-only app, or hardcoded `/Users/...` dependency.
- Browser automation uses Playwright/Selenium with install instructions.
- File paths are config-driven.
- Python dependencies are listed in `requirements.txt`.

Common build choices:

- PyInstaller for Python scripts.
- A `.bat` or PowerShell wrapper for internal workflows where full exe packaging is unnecessary.

Include a smoke test command and a clean Windows install path. If the workflow cannot be made portable, say so and keep the macOS app/panel package only.

## Launcher Verification

For any launcher, verify at least:

- The command starts from a clean shell.
- Missing config fails with a readable message.
- Logs are written where the operator expects.
- The launcher does not silently swallow non-zero exits.
