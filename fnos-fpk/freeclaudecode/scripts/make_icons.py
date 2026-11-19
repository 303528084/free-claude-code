#!/usr/bin/env python3
"""生成占位图标（纯标准库，不依赖 Pillow）。

输出（相对 FPK 包根目录）：
    ICON.PNG        64 x 64
    ICON_256.PNG    256 x 256
    app/ui/images/icon_64.png
    app/ui/images/icon_256.png

风格：圆角方形渐变底 + 白色 ">_" 控制台符号，符合飞牛图标规范里的圆角/留白要求。
换成正式设计稿时，直接覆盖这四个文件即可。
"""

from __future__ import annotations

import math
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)

BG_FROM = (0x5B, 0x6C, 0xFF)
BG_TO = (0x8E, 0x7B, 0xFF)
FG = (0xFF, 0xFF, 0xFF)


def _dist_to_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _rounded_rect(px, py, x0, y0, x1, y1, r):
    cx = min(max(px, x0 + r), x1 - r)
    cy = min(max(py, y0 + r), y1 - r)
    if x0 <= px <= x1 and y0 <= py <= y1:
        return math.hypot(px - cx, py - cy) <= r
    return False


def render(size: int, supersample: int = 3) -> bytes:
    s = size * supersample
    acc = [[(0, 0, 0)] * size for _ in range(size)]

    r = s * 0.22
    glyph_thick = s * 0.055
    # 画布内边距
    pad = s * 0.08

    # ">" 两段
    gt = (pad + s * 0.22, s * 0.30)
    gb = (pad + s * 0.22, s * 0.64)
    gm = (pad + s * 0.52, s * 0.47)
    # "_" 一段
    us = (s * 0.52, s * 0.68)
    ue = (s * 0.82, s * 0.68)

    for y in range(s):
        for x in range(s):
            if not _rounded_rect(x, y, pad, pad, s - pad, s - pad, r):
                continue
            t = (x / s + y / s) / 2.0
            col = tuple(
                int(BG_FROM[i] + (BG_TO[i] - BG_FROM[i]) * t) for i in range(3)
            )
            if (
                _dist_to_segment(x, y, *gt, *gm) <= glyph_thick
                or _dist_to_segment(x, y, *gb, *gm) <= glyph_thick
                or _dist_to_segment(x, y, *us, *ue) <= glyph_thick
            ):
                col = FG
            # 盒式降采样累加
            ox, oy = x // supersample, y // supersample
            pr, pg, pb = acc[oy][ox]
            acc[oy][ox] = (pr + col[0], pg + col[1], pb + col[2])

    n = supersample * supersample
    rows = []
    for oy in range(size):
        row = bytearray()
        for ox in range(size):
            pr, pg, pb = acc[oy][ox]
            row += bytes((pr // n, pg // n, pb // n))
        rows.append(bytes(row))
    return b"".join(b"\x00" + row for row in rows)


def write_png(path: str, size: int) -> None:
    raw = render(size)
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(png)
    print(f"{path}  {size}x{size}  {len(png)} bytes")


def main() -> None:
    write_png(os.path.join(PKG, "ICON.PNG"), 64)
    write_png(os.path.join(PKG, "ICON_256.PNG"), 256)
    write_png(os.path.join(PKG, "app", "ui", "images", "icon_64.png"), 64)
    write_png(os.path.join(PKG, "app", "ui", "images", "icon_256.png"), 256)


if __name__ == "__main__":
    main()
