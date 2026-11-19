#!/bin/bash
# 装配 FPK 运行时载荷（CPython 3.14.10 + venv + 汉化 wheel）
#
# 本地用法（NAS 或任意 x86_64 Linux，root）：
#     cd <包目录的上一级>
#     sudo bash freeclaudecode/scripts/build_payload.sh
#     fnpack build --directory ./freeclaudecode
#
# CI 用法（GitHub Actions，root）：
#     sudo bash fnos-fpk/freeclaudecode/scripts/build_payload.sh
#     --skip-python 跳过编译，直接用缓存好的 /var/apps/freeclaudecode/app/runtime/python
#
# 需要：root、gcc/make（首次编译时）、约 1.2GB 临时空间、能访问 python 镜像与 PyPI。
set -euo pipefail

APPNAME=freeclaudecode
APPDIR=/var/apps/${APPNAME}/app
PKG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY_VER=${PY_VER:-3.14.10}
PY_MIRROR=${PY_MIRROR:-https://mirrors.huaweicloud.com/python}
WHEEL_URL=${WHEEL_URL:-"https://github.com/303528084/free-claude-code/releases/download/zh-v6.19.40-1/free_claude_code-6.19.40%2Bzh.1-py3-none-any.whl"}
PIP_INDEX=${PIP_INDEX:-https://pypi.org/simple}
BUILD=${BUILD:-/tmp/fcc-build}

SKIP_PYTHON=false
for arg in "$@"; do
  case "$arg" in
    --skip-python) SKIP_PYTHON=true ;;
    *) ;;
  esac
done

[ "$(id -u)" = "0" ] || { echo "请用 root 执行（需要写 /var/apps）"; exit 1; }
[ -f "$PKG_DIR/manifest" ] || { echo "没找到包目录：$PKG_DIR"; exit 1; }

JOBS=$(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)

echo "==> 1/3 准备 CPython ${PY_VER} 到 ${APPDIR}/runtime/python"
if [ -x "$APPDIR/runtime/python/bin/python3" ]; then
  echo "    已存在，跳过编译（缓存命中）"
else
  if [ "$SKIP_PYTHON" = "true" ]; then echo "    要求跳过编译但找不到运行时，退出"; exit 1; fi
  mkdir -p "$BUILD"
  cd "$BUILD"
  [ -f "Python-${PY_VER}.tgz" ] || curl -sSLO "${PY_MIRROR}/${PY_VER}/Python-${PY_VER}.tgz"
  [ -d "Python-${PY_VER}" ] || tar -xzf "Python-${PY_VER}.tgz"
  cd "Python-${PY_VER}"
  [ -f Makefile ] || ./configure --prefix="$APPDIR/runtime/python" --with-ensurepip=install \
      --disable-test-modules > "$BUILD/configure.log" 2>&1
  make -j"$JOBS" > "$BUILD/make.log" 2>&1
  make install > "$BUILD/install.log" 2>&1
fi
"$APPDIR/runtime/python/bin/python3" --version

echo "==> 2/3 建 venv 并安装汉化 wheel"
rm -rf "$APPDIR/venv"
"$APPDIR/runtime/python/bin/python3" -m venv "$APPDIR/venv"
if ! "$APPDIR/venv/bin/pip" install -q --no-cache-dir -i "$PIP_INDEX" "$WHEEL_URL" 2>&1 | tail -n 3; then
  echo "    镜像索引失败，改用默认索引重试"
  "$APPDIR/venv/bin/pip" install -q --no-cache-dir "$WHEEL_URL"
fi
"$APPDIR/venv/bin/python" -c "import free_claude_code, sys; print('    import ok', sys.version.split()[0])"

echo "==> 3/3 把载荷拷回包目录并瘦身"
rm -rf "$PKG_DIR/app/runtime/python" "$PKG_DIR/app/venv"
mkdir -p "$PKG_DIR/app/runtime"
cp -a "$APPDIR/runtime/python" "$PKG_DIR/app/runtime/python"
cp -a "$APPDIR/venv" "$PKG_DIR/app/venv"

rm -rf "$PKG_DIR/app/runtime/python/include" \
       "$PKG_DIR/app/runtime/python/lib/pkgconfig" \
       "$PKG_DIR/app/runtime/python/share/man"
find "$PKG_DIR/app/runtime/python" "$PKG_DIR/app/venv" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true

echo "载荷体积："
du -sh "$PKG_DIR/app/runtime/python" "$PKG_DIR/app/venv"
echo "完成：fnpack build --directory $PKG_DIR"
