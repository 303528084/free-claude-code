# app/runtime 与 app/venv：运行时载荷放这里

打包前必须把下面两样东西放进 `app/`，否则 `cmd/main` 会直接报错退出：

```
app/
├── runtime/
│   └── python/                 # CPython 3.14.10，可移植构建
│       ├── bin/python3
│       └── lib/ …
├── venv/                       # 预装好依赖的虚拟环境
│   ├── bin/fcc-server
│   └── lib/python3.14/site-packages/…
└── shim/gateway_shim.py
```

## 为什么自带 Python

- 本项目 `pyproject.toml` 里是 `requires-python = "==3.14.10"`（精确锁版本）。
- 飞牛应用中心提供的运行时只有 `python312`（见文档「运行时环境」一节），版本对不上。
- 所以骨架按 `platform=x86` 自带一份 3.14.10：

```bash
# 在 Linux x86_64 构建机上（例如一台 x86 的 fnOS 容器或 CI）
curl -LO https://github.com/astral-sh/python-build-standalone/releases/download/<版本>/cpython-3.14.10-x86_64-unknown-linux-gnu-install_only.tar.gz
mkdir -p app/runtime && tar -xzf cpython-3.14.10-*.tar.gz -C app/runtime
mv app/runtime/python app/runtime/python 2>/dev/null || true   # 解压出的顶层目录名按实际调整
```

## 依赖怎么装进 venv

用我们 Release 里的汉化 wheel，在构建机上装好整个依赖树，再整体拷进包：

```bash
./app/runtime/python/bin/python3 -m venv app/venv
./app/venv/bin/pip install --no-cache-dir \
  "https://github.com/303528084/free-claude-code/releases/download/zh-v6.19.40-1/free_claude_code-6.19.40%2Bzh.1-py3-none-any.whl"
```

装完检查两件事：

```bash
./app/venv/bin/fcc-server --help          # 入口可用
du -sh app/runtime app/venv               # 体积（预计 runtime ~60MB + venv ~250MB）
```

> venv 里的 `fcc-server` shebang 会写成构建机上的绝对路径。为避免安装后路径不同导致无法执行，
> 建议改用 `app/venv/bin/python3 -m free_claude_code.cli.entrypoints` 之外更稳的方式：
> 保留 `cmd/main` 现在调用 `app/venv/bin/fcc-server` 的写法，并在构建后用
> `sed -i "1s|.*|#!/usr/bin/env bash\nexec \"\$(dirname \"\$0\")/python3\" -m ...|"` 修正，
> 或者干脆在 `cmd/main` 里改成 `"$PYTHON" -m <入口模块>`（待确认入口模块名后定稿）。

## 体积与架构

- `platform=x86`：包内含 x86_64 二进制，ARM 设备装不上（会由系统按 manifest 拦截）。
- 若以后要支持 ARM，需要另出一份 arm64 运行时并改 `platform=all` + 两份载荷，不建议在骨架阶段做。
