"""检查当前树是否可以直接打汉化版发布包。

用法（在仓库根执行）：
    python zh/check_release_ready.py            # 只检查源码树
    python zh/check_release_ready.py dist       # 额外检查 dist/ 里的构建产物
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 汉化过的文件里必须出现的中文片段，用来确认发布包不是英文原版
EXPECTED_ZH = {
    "src/free_claude_code/api/admin_static/index.html": ["模型配置", "供应商"],
    "src/free_claude_code/config/admin/manifest.py": ["供应商", "模型路由", "推理强度"],
    "src/free_claude_code/config/admin/provider_manifest.py": ["API 密钥", "接口地址"],
}


def run(args: list[str]) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout


def check_tree() -> None:
    """重跑一遍翻译套用，工作区必须仍然干净（否则说明有英文文案还没汉化）。"""
    script = ROOT / "zh" / "apply_translations.py"
    subprocess.run([sys.executable, str(script)], check=True, cwd=ROOT)
    dirty = run(["status", "--porcelain", "--untracked-files=no"]).strip()
    if dirty:
        raise SystemExit(
            "翻译套用后有未提交的改动，说明还有英文文案没有汉化，请补译后再发布：\n" + dirty
        )

    for rel, needles in EXPECTED_ZH.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                raise SystemExit(f"{rel} 缺少预期的中文文案：{needle}")


def check_dist(dist: Path, version: str) -> None:
    wheel = dist / f"free_claude_code-{version}-py3-none-any.whl"
    if not wheel.is_file():
        raise SystemExit(f"缺少 wheel：{wheel.name}")

    with zipfile.ZipFile(wheel) as archive:
        names = [n for n in archive.namelist() if not n.endswith("/")]
        html = "free_claude_code/api/admin_static/index.html"
        manifest = "free_claude_code/config/admin/manifest.py"
        for member in (html, manifest):
            if member not in names:
                raise SystemExit(f"wheel 缺少文件：{member}")
        targets = {
            html: ["模型配置", "供应商"],
            manifest: ["模型路由", "推理强度"],
        }
        for member, needles in targets.items():
            text = archive.read(member).decode("utf-8")
            for needle in needles:
                if needle not in text:
                    raise SystemExit(f"wheel 内 {member} 未汉化：缺少 {needle}")
    print(f"[ok] wheel {wheel.name} 内已含中文界面文案")


def main() -> int:
    version = sys.argv[1] if len(sys.argv) > 1 else None
    dist = sys.argv[2] if len(sys.argv) > 2 else None
    check_tree()
    print("[ok] 翻译套用后工作区干净")
    if dist:
        if not version:
            raise SystemExit("检查 dist 时必须同时给出版本号")
        check_dist(Path(dist), version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
