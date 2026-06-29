# Business Flow Packager Skill

把重复业务流程打包成可验证的一键脚本、脚本面板按钮、macOS app、Windows exe 方案，并整理成可分享到 GitHub 的结构。

> **运作方式**：Business Flow Packager 是一套在 AI IDE / Codex 里运行的工作流（一个 skill）。你在对话框里告诉 AI“这个流程想以后能一键跑”，AI 会先检查你电脑上的真实文件、脚本、日志、导出结果和现有面板入口；适合脚本化就直接做成可验证的脚本，不适合就明确告诉你原因。
>
> **你要做的**：把业务流程相关的文件、目录、网页、报表、旧脚本或操作说明给 AI，说明你希望最后变成脚本、脚本面板按钮、macOS app、Windows exe，还是 GitHub 分享包。

## 适合什么场景

- 把本机反复执行的报表、导出、整理、发布流程做成脚本。
- 判断一个业务流程是否适合自动化，不适合时给出明确原因。
- 脚本做好后，确认哪些入口要放到本机脚本面板。
- 需要同时考虑 macOS app、Windows exe、GitHub README 和可复用交付目录。

## 安装到 Codex

本仓库的 skill 本体在：

```text
business-flow-packager/
```

本机安装推荐软链接：

```bash
ln -s /path/to/business-flow-packager/business-flow-packager ~/.codex/skills/business-flow-packager
```

## 怎么让 AI 使用这个 Skill

### 1. 给 AI 一个具体业务流

最有效的说法是同时给出“流程在哪里”和“你想要的交付形式”：

在 Codex 里说：

```text
用 $business-flow-packager 检查 /Users/me/work/monthly-report 里的月度报表流程。
如果适合脚本化，就做成一键脚本；脚本验证通过后，告诉我哪些入口适合放进脚本面板。
```

或者：

```text
用 $business-flow-packager 把这个浏览器导出 + Excel 清洗 + 群里播报的流程打包。
先判断是否适合自动化，不适合就直接说明原因；适合的话做成 GitHub 可分享的结构。
```

也可以直接用自然语言触发：

```text
把这个每月报表流程做成一键脚本，不适合脚本化就告诉我原因。
```

如果 AI 没有自动进入这个流程，直接点名：

```text
先读 business-flow-packager/SKILL.md，然后按这个 skill 的流程执行。
```

### 2. AI 会按这个顺序处理

1. 先读真实文件、旧脚本、日志、导出结果和现有入口。
2. 判断流程是否适合脚本化。
3. 适合就写 `flow_spec.md` 和 `run_contract.md`，再做脚本。
4. 跑语法检查、dry-run 或低风险验证。
5. 把候选入口列出来，让你确认哪些放进脚本面板。
6. 按需要整理 macOS app、Windows exe 或 GitHub 分享包。

### 3. 你可以这样指定交付结果

```text
只做脚本，暂时不要放进脚本面板。
```

```text
脚本验证通过后，帮我准备放进脚本面板的候选按钮配置。
```

```text
这个要给别人用，做成 GitHub repo 结构，README 写清楚安装、配置、运行和验证。
```

```text
这个只在 Mac 上用，做成脚本 + macOS app 入口；不要承诺 Windows exe。
```

## 目录结构

```text
business-flow-packager/
├── README.md
└── business-flow-packager/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    │   ├── suitability.md
    │   ├── package-structure.md
    │   ├── platform-and-panel.md
    │   └── github-release.md
    └── scripts/
        ├── flow_probe.py
        └── make_flow_package.py
```

## 内置工具

只读扫描候选业务流目录：

```bash
python3 business-flow-packager/scripts/flow_probe.py --paths ~/some-workflow --output /tmp/flow_probe.json --markdown /tmp/flow_probe.md
```

创建一个业务流打包目录：

```bash
python3 business-flow-packager/scripts/make_flow_package.py --root ./flows/monthly-report --title "Monthly Report" --platform mac --panel
```

## 设计取舍

- Skill 本体不放冗长说明，详细判断标准放在 `references/`，按需读取。
- 借鉴项目型仓库的结构：`sources/`、`scripts/`、`exports/`、`notes/`、`backup/` 分开。
- 增加 `flow_spec.md` 和 `run_contract.md`，把业务目标和可执行契约拆开，避免后续维护时跑偏。
- 默认不把脚本直接塞进面板；脚本验证后先列出候选入口，再让用户确认。

## 安全边界

不要把真实 `.env`、token、cookie、浏览器 profile、客户数据、私有导出文件提交到 GitHub。发布前按 `business-flow-packager/references/github-release.md` 做检查。
