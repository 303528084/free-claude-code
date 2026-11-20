#!/usr/bin/env python3
"""从官方图标生成飞牛应用图标（可选工具，CI 不用它跑）。

图标来源是上游自带的 ``src/free_claude_code/assets/app-icon.png``（1024×1024 透明底）。
飞牛桌面的应用磁贴需要一个实心方块才好看，所以这里把官方图形居中放在
官方 logo 里那块深色（#080b12）的圆角方块上，圆角比例取 22%。

输出（相对 FPK 包根目录）：
    ICON.PNG        64 x 64
    ICON_256.PNG    256 x 256
    app/ui/images/icon_64.png
    app/ui/images/icon_256.png

依赖 Pillow（只在本地重新生成图标时用）：
    python -m pip install pillow
    python scripts/make_icons.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PKG))
SRC = os.path.join(REPO, "src", "free_claude_code", "assets", "app-icon.png")

BG = (8, 11, 18, 255)   # #080b12，取自官方 logo 的深色块
RADIUS = 0.22           # 圆角半径 / 画布边长
INNER = 0.76            # 官方图形占画布的比例
TARGETS = (
    (256, "ICON_256.PNG"),
    (64, "ICON.PNG"),
    (256, os.path.join("app", "ui", "images", "icon_256.png")),
    (64, os.path.join("app", "ui", "images", "icon_64.png")),
)


def render(size: int) -> "Image.Image":
    from PIL import Image, ImageDraw

    src = Image.open(SRC).convert("RGBA")
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    radius = int(size * RADIUS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    canvas.paste(Image.new("RGBA", (size, size), BG), (0, 0), mask)

    inner = int(size * INNER)
    offset = (size - inner) // 2
    canvas.paste(src.resize((inner, inner), Image.LANCZOS), (offset, offset), src.resize((inner, inner), Image.LANCZOS))
    return canvas


def main() -> int:
    if not os.path.isfile(SRC):
        print(f"找不到官方图标：{SRC}", file=sys.stderr)
        return 1
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("需要 Pillow：python -m pip install pillow", file=sys.stderr)
        return 1

    cache = {}
    for size, rel in TARGETS:
        out = os.path.join(PKG, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if size not in cache:
            cache[size] = render(size)
        cache[size].save(out, "PNG")
        print(f"写出 {out}（{size}x{size}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
