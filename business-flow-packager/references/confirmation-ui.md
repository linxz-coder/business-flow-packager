# Confirmation UI

Use the browser confirmation page when the workflow can be inferred from session evidence but a few packaging decisions need user confirmation. Keep user input minimal: the AI recommends defaults; the user only confirms or tweaks.

## Principle

Use the same confirmation-page pattern throughout the package:

- Chat remains the fallback.
- The AI writes `confirm_ui/recommendations.json`.
- A local browser page displays recommended choices.
- The user clicks confirm.
- The page writes `confirm_ui/result.json`.
- The AI reads `result.json` and continues without asking the user to restate the workflow.

Use one bundled confirmation gate, not many chat questions.

## When To Use

Use it for decisions such as:

- Delivery form: script only, script panel candidate, macOS app, Windows exe, GitHub package.
- Whether to add a manual checkpoint for risky production actions.
- Which candidate commands should become launcher entries.
- Platform scope when the session used Mac-only tools.
- Whether private example exports should be excluded or replaced with sanitized fixtures.

Do not use it to ask the user to describe the workflow again. The workflow should already come from session evidence.

## Data Contract

Write this before launching:

```json
{
  "title": "确认业务流打包方案",
  "summary": "AI 已从成功 session 提取默认方案。",
  "hint": "确认后 AI 会继续生成脚本、验证并整理交付包。",
  "evidence": {
    "source": "current-session",
    "outputs": ["exports/report.xlsx"],
    "verified": ["dry-run ok"]
  },
  "risks": ["脚本面板入口会在你确认后才添加。"],
  "decisions": [
    {
      "id": "delivery",
      "label": "交付形式",
      "description": "默认选择最适合当前 session 的形式。",
      "type": "multi_choice",
      "default": ["script", "github"],
      "options": [
        {"value": "script", "label": "一键脚本", "description": "生成可重复运行的脚本。"},
        {"value": "panel", "label": "脚本面板候选", "description": "生成候选按钮，用户确认后再加入面板。"}
      ]
    }
  ]
}
```

Supported decision types:

- `choice`: radio group, one value.
- `multi_choice`: checkboxes, array value.
- `boolean`: checkbox.
- `text`: textarea.

Launch:

```bash
python3 business-flow-packager/scripts/confirm_ui.py <flow_package_path>
```

For headless or test runs:

```bash
python3 business-flow-packager/scripts/confirm_ui.py <flow_package_path> --no-browser
```

Result is written to:

```text
<flow_package_path>/confirm_ui/result.json
```

## Fallback

If the page cannot open or times out, ask a short bundled chat confirmation with the same defaults. Do not turn it into a long requirements interview.
