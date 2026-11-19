# 汉化工作区（仅存在于 zh-cn 分支）

本目录存放 `zh-cn` 分支的汉化基础设施。汉化内容不会进入上游仓库。

## 文件

| 文件 | 用途 |
| --- | --- |
| `strings.json` | 英文 → 中文对照表，分三类：`string_literals`（JS 中的引号字符串）、`template_literals`（含 `${}` 的模板字符串片段）、`html_literals`（`index.html` 中的文本与属性） |
| `apply_translations.py` | 读取对照表，把尚未翻译的英文文案替换成中文；可重复执行（幂等），执行后会列出仍疑似英文的界面文案供补译 |
| `sync_upstream.ps1` | 拉取上游 → 合并进 `zh-cn` → 自动重跑 `apply_translations.py` → 有变更则提交 |

## 日常同步

```powershell
# 只同步 zh-cn：合并上游 main 并补译
pwsh -File zh/sync_upstream.ps1

# 同时把 upstream-sync 分支硬同步到上游（纯镜像分支）
pwsh -File zh/sync_upstream.ps1 -Mirror

# 同步后把 zh-cn 推到 origin
pwsh -File zh/sync_upstream.ps1 -Push
```

上游新增的界面文案若不在 `strings.json` 中，脚本会在末尾以 `[待补译]` 列出；把这些条目补进 `strings.json` 后重跑即可。

## 覆盖范围

- 文档：`README.md`、`CONTRIBUTING.md`、`MAINTAINERS.md`
- Admin 管理界面：`src/free_claude_code/api/admin_static/` 下的 `index.html`、`admin.js`、`code_sessions.js`、`session_ui.js`、`api_key_editor.js`

未覆盖：由后端 `config/admin/manifest.py`、`provider_manifest.py` 下发的表单字段名与字段说明，以及命令行输出，仍为英文。

## 分支约定

- `upstream-sync`：上游镜像分支，始终等于 `upstream/main`，可用于对照英文原文。
- `zh-cn`：汉化分支，跟随上游更新，但内容不回推上游。
- `upstream` 的 push 地址已设为 `DISABLED`，误用 `git push upstream` 也不会写入上游仓库。
