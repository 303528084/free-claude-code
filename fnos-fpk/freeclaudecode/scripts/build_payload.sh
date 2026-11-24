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
WHEEL_URL=${WHEEL_URL:-"https://github.com/303528084/free-claude-code/releases/download/zh-v6.19.53-1/free_claude_code-6.19.53%2Bzh.1-py3-none-any.whl"}
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

echo "==> 2.5 用仓库源码覆盖后台静态资源（避免 wheel 落后于当前提交）"
REPO_ROOT="$(cd "$PKG_DIR/../.." && pwd)"
SITE_DIR="$("$APPDIR/venv/bin/python" -c "import free_claude_code, os; print(os.path.dirname(free_claude_code.__file__))")"
for sub in api/admin_static assets; do
  if [ -d "$REPO_ROOT/src/free_claude_code/$sub" ]; then
    cp -a "$REPO_ROOT/src/free_claude_code/$sub/." "$SITE_DIR/$sub/"
    echo "    已同步 $sub"
  fi
done

echo "==> 3/3 把载荷拷回包目录并瘦身"
rm -rf "$PKG_DIR/app/runtime/python" "$PKG_DIR/app/venv"
mkdir -p "$PKG_DIR/app/runtime"
cp -a "$APPDIR/runtime/python" "$PKG_DIR/app/runtime/python"
cp -a "$APPDIR/venv" "$PKG_DIR/app/venv"

rm -rf "$PKG_DIR/app/runtime/python/include" \
       "$PKG_DIR/app/runtime/python/lib/pkgconfig" \
       "$PKG_DIR/app/runtime/python/share/man"
find "$PKG_DIR/app/runtime/python" "$PKG_DIR/app/venv" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true

# 静态库、标准库测试用例、打包/构建工具：运行期完全用不到，白白撑大包
rm -f  "$PKG_DIR/app/runtime/python/lib/libpython"*.a
rm -rf "$PKG_DIR/app/runtime/python/lib/python3.14/test" \
       "$PKG_DIR/app/runtime/python/lib/python3.14/idlelib" \
       "$PKG_DIR/app/runtime/python/lib/python3.14/turtledemo" \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/pip" \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/pip"* \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/setuptools" \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/setuptools"* \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/pkg_resources" \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/wheel" \
       "$PKG_DIR/app/venv/lib/python3.14/site-packages/_distutils_hack"
find "$PKG_DIR/app/venv/lib/python3.14/site-packages" -type d -name 'licenses' -prune -exec rm -rf {} + 2>/dev/null || true
find "$PKG_DIR/app/venv/lib/python3.14/site-packages" -maxdepth 1 -name '*.dist-info' -type d -exec sh -c 'rm -rf "$1/RECORD" 2>/dev/null || true' _ {} \;
# 删了 setuptools/_distutils_hack 之后它留下的 .pth 还在，每次启动都会打印 ModuleNotFoundError 噪音
rm -f "$PKG_DIR/app/venv/lib/python3.14/site-packages/distutils-precedence.pth" 2>/dev/null || true

# 非 ASCII 文件名（例如 setuptools 造的 venv/bin/𝜋thon）在 fnOS 解包器上会导致整包解压失败，必须清掉
echo "==> 清理非 ASCII 条目"
badfile="$BUILD/non-ascii.txt"
mkdir -p "$BUILD"
find "$PKG_DIR/app" -print 2>/dev/null | LC_ALL=C grep '[^ -~]' > "$badfile" || true
if [ -s "$badfile" ]; then
  echo "    发现 $(wc -l < "$badfile") 个，逐个删除："
  sort -r "$badfile" | while IFS= read -r f; do echo "      $f"; rm -rf -- "$f"; done
fi
if find "$PKG_DIR/app" -print 2>/dev/null | LC_ALL=C grep -q '[^ -~]'; then
  echo "    仍有非 ASCII 条目，判定为失败" >&2
  find "$PKG_DIR/app" -print 2>/dev/null | LC_ALL=C grep '[^ -~]' | head -n 50 >&2
  exit 1
fi
echo "    已无非 ASCII 条目"

echo "==> 把绝对符号链接改成相对"
find "$PKG_DIR/app" -type l -print 2>/dev/null > "$BUILD/abs-links.txt" || true
python3 - "$PKG_DIR/app" <<'PY'
import os, sys
root = sys.argv[1]
INSTALL_PREFIX = "/var/apps/freeclaudecode/app"   # 安装后的 app 目录（载荷约定）
fixed = 0
for dirpath, _, files in os.walk(root):
    for name in files:
        p = os.path.join(dirpath, name)
        if not os.path.islink(p):
            continue
        tgt = os.readlink(p)
        if not os.path.isabs(tgt):
            continue
        print("    绝对链接：%s -> %s" % (os.path.relpath(p, root), tgt))
        if not tgt.startswith(INSTALL_PREFIX + "/"):
            print("    无法映射到包内路径，判定为失败", file=sys.stderr)
            sys.exit(1)
        real = os.path.join(root, tgt[len(INSTALL_PREFIX) + 1:])
        rel = os.path.relpath(real, os.path.dirname(p))
        os.remove(p)
        os.symlink(rel, p)
        fixed += 1
        print("      改为 %s" % rel)
print("    共修正 %d 个绝对符号链接" % fixed)
PY
if find "$PKG_DIR/app" -type l -exec sh -c 'case "$(readlink "$1")" in /*) echo "$1 -> $(readlink "$1")";; esac' _ {} \; | grep -q .; then
  echo "    仍存在绝对符号链接，判定为失败" >&2
  exit 1
fi
echo "    已无绝对符号链接"

echo "载荷体积："

du -sh "$PKG_DIR/app/runtime/python" "$PKG_DIR/app/venv"
echo "完成：fnpack build --directory $PKG_DIR"



