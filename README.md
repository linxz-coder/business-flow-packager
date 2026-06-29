# Business Flow Packager

将已经跑通的办公业务操作沉淀为可复用自动化：一键脚本、脚本面板入口、macOS app、Windows exe 方案，或团队内部可交付包。

## 适用场景

- 报表生成、数据导出、Excel 清洗、文件整理、内容发布、固定格式播报等重复办公操作。
- 已由 AI 在一次 session 中成功执行，需要固化为后续可复用流程。
- 需要判断流程是否适合脚本化；不适合时输出明确原因。
- 需要把已验证脚本接入脚本面板、桌面应用入口或同事可使用的本地交付包。

## 使用方式

在业务流程跑通后，输入一句即可：

```text
用 $business-flow-packager 打包当前已完成的流程。
```

打包历史 session：

```text
用 $business-flow-packager 打包这个已跑通的 session：<thread/session 链接或标题>
```

可选补充目标：

```text
只生成脚本。
生成脚本，并准备脚本面板入口。
整理成办公室同事可使用的交付包。
仅面向 macOS，不需要 Windows exe。
```

## 用户确认

用户不需要重新编写需求文档。系统会从成功 session 中提取命令、文件变更、输出结果和验证证据。

当存在必须确认的决策时，会打开本地 HTML 确认页。常见确认项包括：

- 交付形式：脚本、脚本面板入口、macOS app、Windows exe、办公交付包。
- 是否保留人工确认点。
- 哪些脚本入口可以加入脚本面板。
- 是否排除或替换敏感示例数据。

确认后，结果写入：

```text
<flow_package>/confirm_ui/result.json
```

## 交付物

典型输出包括：

```text
flow_package/
├── README.md
├── flow_spec.md
├── run_contract.md
├── scripts/
├── config/
├── tests/
├── confirm_ui/
├── docs/
├── exports/
└── release/
```

- `flow_spec.md`：业务目标、输入输出、人工假设和数据边界。
- `run_contract.md`：执行命令、工作目录、依赖、日志、幂等性和验证方式。
- `scripts/`：可运行脚本。
- `tests/`：smoke test 或 dry-run 验证。
- `confirm_ui/`：确认页输入和确认结果。
- `release/`：app/exe/压缩包等内部交付产物。

## 安装

skill 本体目录：

```text
business-flow-packager/
```

安装到 Codex：

```bash
ln -s /path/to/business-flow-packager/business-flow-packager ~/.codex/skills/business-flow-packager
```

## 工具命令

创建业务流交付包：

```bash
python3 business-flow-packager/scripts/make_flow_package.py --root ./flows/monthly-report --title "Monthly Report" --platform mac --panel
```

打开本地确认页：

```bash
python3 business-flow-packager/scripts/confirm_ui.py ./flows/monthly-report
```

盘点已由 session 指向的目录：

```bash
python3 business-flow-packager/scripts/flow_probe.py --paths ~/some-workflow --output /tmp/flow_probe.json --markdown /tmp/flow_probe.md
```

## 安全边界

- 不打包或转交真实 `.env`、token、cookie、浏览器 profile、客户数据或私有导出。
- 不从静态文档目录反推业务流；以已成功执行的 session 为准。
- 不在脚本验证前加入脚本面板。
- 不承诺跨平台打包，除非流程不存在系统专属依赖。
