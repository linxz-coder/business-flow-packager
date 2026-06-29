# Business Flow Packager Skill

把重复业务流程打包成可验证的一键脚本、脚本面板按钮、macOS app、Windows exe 方案，并整理成可分享到 GitHub 的结构。

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

## 使用方式

在 Codex 里说：

```text
用 $business-flow-packager 检查这个业务流程，适合的话做成脚本，并准备脚本面板/app/GitHub 交付。
```

或者：

```text
把这个每月报表流程做成一键脚本，不适合脚本化就直接告诉我原因。
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
