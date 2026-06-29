# Business Flow Packager Skill

把 AI 已经跑通的一次业务操作，沉淀成可验证的一键脚本、脚本面板按钮、macOS app、Windows exe 方案，并整理成可分享到 GitHub 的结构。

> **运作方式**：Business Flow Packager 是一套在 AI IDE / Codex 里运行的工作流（一个 skill）。它不是让 AI 只靠扫描某个文档目录去猜业务流程，而是把“AI 刚刚或之前已经帮你跑通的一次具体 session”整理成可复用工作流。AI 会从那次 session 里提取实际执行过的命令、修改过的文件、人工确认点、输出结果和验证证据；适合脚本化就打包，不适合就明确告诉你原因。
>
> **你要做的**：在某个业务流程被 AI 跑通后，对同一个 AI 说“把刚才这个流程打包成 skill/工作流”；或者把那次 session 的 thread、记录、命令、产物目录或关键输出给 AI，并说明你希望最后变成脚本、脚本面板按钮、macOS app、Windows exe，还是 GitHub 分享包。

## 适合什么场景

- 把 AI 已经跑通的报表、导出、整理、发布流程做成脚本。
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

### 1. 在流程跑通后，让 AI 立刻打包

最有效的用法是在 AI 刚刚完成一次业务操作后，直接接着说：

```text
用 $business-flow-packager 把刚才这个已经跑通的流程打包成可复用工作流。
先从本 session 里提取实际步骤、命令、文件、输出和验证证据；
适合脚本化就做成一键脚本，脚本验证后再告诉我哪些入口适合放进脚本面板。
```

或者更短：

```text
把刚才你帮我跑通的流程打包成工作流，能做脚本就做脚本，不能就说明原因。
```

### 2. 打包一个过去的 session

如果要打包的是之前某次对话或执行记录，把 session 线索给 AI：

```text
用 $business-flow-packager 打包这个 session 里已经跑通的流程：<thread/session 链接或标题>。
请先读取那次 session 的关键命令、文件变更、输出结果和验证方式，再整理成 GitHub 可分享的工作流。
```

也可以给更具体的上下文：

```text
上次 AI 已经帮我完成了“浏览器导出 + Excel 清洗 + 群里播报”。
请用 $business-flow-packager 根据那次执行记录打包，不要只扫描文档目录来猜流程。
```

如果 AI 没有自动进入这个流程，直接点名：

```text
先读 business-flow-packager/SKILL.md，然后按这个 skill 的流程执行。
```

### 3. AI 会按这个顺序处理

1. 先读取当前或指定 session 的实际执行记录。
2. 提取真实步骤：命令、脚本、文件输入输出、人工确认、验证证据。
3. 再检查 session 里涉及的文件和目录，用于补齐依赖，而不是从目录猜流程。
4. 判断流程是否适合脚本化。
5. 适合就写 `flow_spec.md` 和 `run_contract.md`，再做脚本。
6. 跑语法检查、dry-run 或低风险验证。
7. 把候选入口列出来，让你确认哪些放进脚本面板。
8. 按需要整理 macOS app、Windows exe 或 GitHub 分享包。

### 4. 你可以这样指定交付结果

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
    │   ├── session-evidence.md
    │   ├── suitability.md
    │   ├── package-structure.md
    │   ├── platform-and-panel.md
    │   └── github-release.md
    └── scripts/
        ├── flow_probe.py
        └── make_flow_package.py
```

## 内置工具

只读盘点 session 证据里已经指向的候选目录：

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
