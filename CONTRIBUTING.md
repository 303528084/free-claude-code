# 参与贡献

感谢你帮助改进 Free Claude Code。请把改动控制在必要范围内，为你改动的行为补充测试，并保持 Claude Code 与 Codex 的公开工作流不被破坏。

## 提交 Pull Request 之前

- 纯文档类 PR 仅限仓库所有者提交。
- 功能性代码改动请一并包含相应的 README 及其他文档更新，这类附带的文档更新无需单独开 Issue。
- 不要提交 Docker 集成相关的 PR。
- 反馈 Bug 时，请给出全部模型映射、故障发生时的当前模型、完整报错信息以及可复现步骤。
- 为行为改动及相关边界情况补充有针对性的测试。

## Pull Request 标题

改动涉及 `assets/`、`scripts/`、`src/`、`pyproject.toml` 或 `uv.lock` 时，标题必须以 `patch: `、`minor: ` 或 `major: ` 开头，后面跟描述，冒号后严格保留一个空格。

未改动上述路径的 PR 不得使用发布前缀。请勿修改版本号。发布流程会在合并后计算版本、创建 Git tag，并发布到 PyPI 与 GitHub Releases。

## 开发环境

先安装 [uv](https://docs.astral.sh/uv/)，然后直接在代码检出目录中运行。uv 会自动安装项目所需的 Python 版本。

```bash
git clone https://github.com/Alishahryar1/free-claude-code.git
cd free-claude-code
uv run fcc-server
```

Python 命令一律用 `uv run` 执行，不要用全局 Python 解释器运行本项目。

## 质量检查

提交 PR 前请跑完整的本地 CI 流程：

```bash
./scripts/ci.sh
```

```powershell
.\scripts\ci.ps1
```

在 macOS/Linux 上可用 `--only`、`--skip`、`--dry-run` 做局部迭代，PowerShell 中对应为 `-Only`、`-Skip`、`-DryRun`。

单项修复与测试命令：

```bash
uv run ruff format
uv run ruff check --fix
uv run ty check
uv run pytest -v --tb=short
```

GitHub CI 以只检查（check-only）模式运行 Ruff，并禁止使用 `# type: ignore`、`# ty: ignore` 以及旧式注解绕过手段。请修复底层的类型与导入边界问题，而不是压制告警。

## 项目规范

- 目标版本为 Python 3.14，依赖原生惰性注解（lazy annotations），不要添加 `from __future__ import annotations`。
- Python 3.14 支持省略括号的多异常类型写法，例如 `except TypeError, ValueError:`。
- 共享的 Anthropic 协议行为请放在 `src/free_claude_code/core/anthropic/` 下，不要从其他供应商模块中导入工具函数。
- 供应商专属配置请放在拥有它的供应商模块中。
- 迁移完成后请删除失效的兼容代码，除非明确要求保留已发布的接口。
