# Codex Context Pack · 代码上下文打包器

**Codex / codex破甲 / DeepSeek / DeepSeek破甲 / 破甲 开发者工具系列**

[![CI](https://github.com/HaoHaolovestolearn/codex-context-pack/actions/workflows/ci.yml/badge.svg)](https://github.com/HaoHaolovestolearn/codex-context-pack/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

### NB破甲入口

**[🌐 项目官网](https://nbpojia.lol) · [💬 Telegram 社群](https://t.me/HaoNB_6666) · [📚 破甲教程](https://nbpojia.lol/tutorials/armor) · [🔌 API 教程](https://nbpojia.lol/tutorials/api)**

使用问题、示例交流和版本反馈可到 TG 群；需要联系管理员：[HaoNB_666](https://t.me/HaoNB_666)。请勿在群内发送密钥或私有源码。

## 这个项目解决什么

适合在与 Codex 或 DeepSeek 讨论代码前准备可审阅的上下文。选择一个小目录，生成 Markdown 源码包、SHA-256 清单和 HTML 浏览报告。

本项目是 NB破甲社区的独立开源工具。`codex破甲`、`DeepSeek破甲` 和 `破甲` 用于标识社区系列；具体能力以本仓库代码和示例为准。项目与 OpenAI / DeepSeek 无官方隶属关系。

## 功能

- 按路径排序，输出文件大小和 SHA-256，方便复核来源。
- 支持单文件/总体字节上限和重复 `--exclude` 相对路径 glob。
- 跳过符号链接、常见密钥文件、依赖目录和疑似凭据内容。
- 自动使用更长的 Markdown 围栏，避免源码中的反引号破坏格式。

## 三分钟开始

需要 Python 3.10 或更高版本（CI 验证 Python 3.12）。Linux / macOS 可将 `python` 替换为 `python3`；Windows 可使用 `py -3`。只使用标准库，无需 pip 安装依赖。

```bash
git clone https://github.com/HaoHaolovestolearn/codex-context-pack.git
cd codex-context-pack
python main.py examples/demo --out outputs/demo
python main.py examples/demo --exclude "*.md" --max-total 10000 --out outputs/code-only
```

命令在 `outputs/` 生成结果。用浏览器直接打开对应的 `.html` 文件即可查看离线报告，报告顶部和底部保留官网与 Telegram 社群入口。输入数据保留在本机，工具不调用模型接口；点击外部社群/官网链接时才会打开相应网站。

完整演示可运行：

```bash
python smoke.py
python main.py --help
```

`smoke.py` 在临时目录中验证示例，结束后清理结果；要保留报告请运行上面的 CLI 命令。

## 输入、输出与边界

输入是本地目录；输出 `context.md`、`manifest.json`、`report.html`。默认每文件 100000 字节、合计 1000000 字节。只处理受支持的 UTF-8 文本扩展名；不读取 `.gitignore`。默认跳过 `.git`、`.codex`、虚拟环境、node_modules、outputs 等目录。被剪枝目录不逐文件列入跳过清单。敏感检测只是文件名/正则启发式，不能保证无泄露；分享前必须人工检查。不要选择仍在被其他进程修改的输入目录。

更多字段和错误处理见 [使用指南](docs/USAGE.md)。示例均为虚构演示数据。

## 验证与自动发布

```bash
python -m unittest discover -s tests -v
python smoke.py
python build_release.py
```

每次提交 / Pull Request 自动在 Linux、Windows、macOS 运行测试和完整示例，并验证源码压缩包可构建。推送 `v*` 标签时，测试成功后自动发布 Source ZIP 与 SHA-256 校验文件。首版为 **v1.0.0**；[下载发布版本](https://github.com/HaoHaolovestolearn/codex-context-pack/releases)。源码包需要 Python，不是独立可执行程序。

## 五个独立工具

| 项目 | 主要用途 |
| --- | --- |
| [Codex Context Pack](https://github.com/HaoHaolovestolearn/codex-context-pack) | 代码上下文打包器 |
| [Codex Prompt Check](https://github.com/HaoHaolovestolearn/codex-prompt-check) | 提示词模板检查器 |
| [Codex Usage Ledger](https://github.com/HaoHaolovestolearn/codex-usage-ledger) | Token 用量账本 |
| [Codex Response Diff](https://github.com/HaoHaolovestolearn/codex-response-diff) | 模型回答对比器 |
| [Codex Task Board](https://github.com/HaoHaolovestolearn/codex-task-board) | 编程任务看板 |

它们各自维护源码、示例、测试、CI 与 Release，可以单独使用。

## English

Codex Context Pack is a local-first Python developer utility for Codex and DeepSeek workflows. 把选定代码整理成带清单和哈希的 Markdown 上下文包. It uses the Python standard library, produces reviewable local outputs, and does not send input data to a model service. NB Pojia is a community label; this repository is independently maintained.

## 参与和联系

欢迎提交带复现输入和预期行为的 Issue / PR。参见 [贡献指南](CONTRIBUTING.md)、[更新记录](CHANGELOG.md) 和 [MIT 许可证](LICENSE)。

**[NB破甲官网](https://nbpojia.lol) · [加入 Telegram 社群](https://t.me/HaoNB_6666)**
