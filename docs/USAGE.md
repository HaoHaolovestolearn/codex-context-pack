# 代码上下文打包器使用指南

适合在与 Codex 或 DeepSeek 讨论代码前准备可审阅的上下文。选择一个小目录，生成 Markdown 源码包、SHA-256 清单和 HTML 浏览报告。

## 示例命令

```bash
python main.py examples/demo --out outputs/demo
python main.py examples/demo --exclude "*.md" --max-total 10000 --out outputs/code-only
```

## 数据约定

输入是本地目录；输出 `context.md`、`manifest.json`、`report.html`。默认每文件 100000 字节、合计 1000000 字节。只处理受支持的 UTF-8 文本扩展名；不读取 `.gitignore`。默认跳过 `.git`、`.codex`、虚拟环境、node_modules、outputs 等目录。被剪枝目录不逐文件列入跳过清单。敏感检测只是文件名/正则启发式，不能保证无泄露；分享前必须人工检查。不要选择仍在被其他进程修改的输入目录。

## 常见问题

- 路径不存在：从仓库根目录运行命令，给含空格的路径加引号。
- JSON 解析失败：使用 UTF-8，删除尾随逗号，查看报错行和字段。
- 输出被拒绝：确认目录可写，不要使用系统目录。
- 中文输出：入口自动配置 UTF-8；编辑器也应使用 UTF-8。
- HTML 报告：是本地快照，不需要服务器；不要把真实私密数据提交到公共仓库。

## 验证流程

运行单元测试与 `python smoke.py`。示例测试必须验证完整 CLI 链路，发布包使用固定源文件清单，并附 SHA-256。

[返回 README](../README.md) · [官网](https://nbpojia.lol) · [TG 社群](https://t.me/HaoNB_6666)
