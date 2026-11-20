#!/usr/bin/env python3
"""验证 gateway_shim.py（假上游 + UDS 客户端）。

只能在支持 Unix Socket 的 asyncio 上跑：Linux / macOS / Windows 10+ 的 Python（Windows 版 asyncio
没有 start_unix_server，会直接 NotImplementedError，此时脚本会提示跳过）。

    python3 scripts/test_shim.py
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PKG, "app", "shim"))

import gateway_shim  # noqa: E402

PREFIX = "/app/freeclaudecode"
UP_PORT = 18586
SEEN: dict[str, str] = {}

HTML_BODY = (
    b'<html><head>'
    b'<link rel="stylesheet" href="/admin/assets/v1/admin.css" />'
    b'<script src="/admin/assets/v1/admin.js"></script>'
    b'</head><body><a href="/admin/model_config">cfg</a></body></html>'
)

# 真实 admin 前端里的两种写法：字符串里的绝对路径 + 正则字面量里转义过的路径。
# 后者要是被直接插前缀，正则会被提前闭合、整段 JS 变语法错误（真机上踩过）。
JS_BODY = (
    b'const base = "/admin/api/code";\n'
    b'let id = /^\\/admin\\/code\\/([0-9a-f-]+)$/.exec(path)?.[1] || null;\n'
)


async def fake_upstream(reader, writer) -> None:
    head = await reader.readuntil(b"\r\n\r\n")
    SEEN["head"] = head.decode("latin-1")
    path = head.split(b" ")[1]

    if path.endswith(b"/admin"):
        body = HTML_BODY
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n")
        writer.write(f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode())
        writer.write(body)
        await writer.drain()
        writer.close()
        return

    if b"stream=1" in path:
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\nConnection: close\r\n\r\n")
        writer.write(b"data: first\n\n")
        await writer.drain()
        await asyncio.sleep(0.3)
        writer.write(b"data: second\n\n")
        await writer.drain()
        writer.close()
        return

    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok")
    await writer.drain()
    writer.close()


async def unix_request(path: str, payload: bytes) -> bytes:
    reader, writer = await asyncio.open_unix_connection(path)
    writer.write(payload)
    await writer.drain()
    chunks = []
    while True:
        data = await reader.read(4096)
        if not data:
            break
        chunks.append(data)
    writer.close()
    return b"".join(chunks)


async def main() -> int:
    tmp = tempfile.mkdtemp()
    sock_path = os.path.join(tmp, "fcc.sock")

    up = await asyncio.start_server(fake_upstream, "127.0.0.1", UP_PORT)
    shim_task = asyncio.create_task(gateway_shim.serve(sock_path, "127.0.0.1", UP_PORT, PREFIX))
    for _ in range(60):
        if os.path.exists(sock_path):
            break
        await asyncio.sleep(0.05)

    def req(path: str, extra: str = "") -> bytes:
        return (
            f"GET {PREFIX}{path} HTTP/1.1\r\n"
            "Host: nas.example.com:8000\r\n"
            "Origin: http://nas.example.com:8000\r\n"
            "X-Trim-Userid: 1000\r\n"
            "X-Trim-Isadmin: true\r\n"
            "X-Trim-Username: admin\r\n"
            "Accept-Encoding: gzip, deflate\r\n"
            f"{extra}\r\n"
        ).encode("latin-1")

    page = await unix_request(sock_path, req("/admin"))
    sse = await unix_request(sock_path, req("/admin/api/live?stream=1"))

    ok = True

    def check(cond: bool, label: str) -> None:
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + label)
        ok = ok and cond

    head = SEEN.get("head", "")
    print("--- 上游收到的请求 ---")
    print(head)
    print("--- 返回给客户端的 HTML 片段 ---")
    print(page.decode("latin-1")[-260:])

    check("GET /admin HTTP/1.1" in head, "网关前缀已剥离")
    check("Host: 127.0.0.1:18586" in head, "Host 改写为回环")
    check("Origin: http://127.0.0.1:18586" in head, "Origin 改写为回环")
    check("nas.example.com" not in head, "原 Host/Origin 已移除")
    check("X-Trim-Isadmin: true" in head, "X-Trim-* 保留")
    check("Accept-Encoding" not in head, "Accept-Encoding 已移除（保证响应可改写）")
    check(b'href="/app/freeclaudecode/admin/assets/v1/admin.css"' in page, "HTML 里的资源路径已加前缀")
    check(b'src="/app/freeclaudecode/admin/assets/v1/admin.js"' in page, "JS 引用已加前缀")
    check(b'href="/app/freeclaudecode/admin/model_config"' in page, "裸 /admin 链接已加前缀")
    check(b'"/app/freeclaudecode/admin/assets/v1/admin.css"' not in page, "没有重复加前缀")
    check(b"data: first" in sse and b"data: second" in sse, "SSE 流式两帧都送达")

    js_head = b"Content-Type: text/javascript; charset=utf-8\r\nContent-Length: 1\r\n\r\n"
    js_rewritten = gateway_shim._rewrite_body(js_head, JS_BODY, PREFIX)
    js_out = js_rewritten[1] if js_rewritten else JS_BODY
    print("--- JS 改写结果 ---")
    print(js_out.decode("latin-1"))
    check(b'"/app/freeclaudecode/admin/api/code"' in js_out, "JS 字符串路径已加前缀")
    check(b"/^\\/app\\/freeclaudecode\\/admin\\/code\\/" in js_out, "正则字面量加了转义前缀")
    check(js_out.count(b"\\/\\/") == 0, "没有产生双反斜杠（否则正则直接语法错误）")

    bad = (
        f"POST {PREFIX}/admin/api/config/apply HTTP/1.1\r\n"
        "Host: nas.example.com\r\nTransfer-Encoding: chunked\r\n\r\n"
    ).encode("latin-1")
    check((await unix_request(sock_path, bad)).startswith(b"HTTP/1.1 400"), "chunked 请求被拒绝")

    shim_task.cancel()
    up.close()
    await up.wait_closed()
    print("\n结论：", "全部通过" if ok else "存在失败项")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except NotImplementedError:
        print("当前平台的 asyncio 不支持 Unix Socket，请在 Linux 上跑本测试")
        sys.exit(1)
