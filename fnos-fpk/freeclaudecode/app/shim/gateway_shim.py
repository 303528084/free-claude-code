#!/usr/bin/env python3
"""网关适配：把飞牛统一网关的 Unix Socket 请求转成本机 TCP 请求。

为什么需要它：fcc-server 内部是 uvicorn，只支持 host/port 监听（没有 UDS），
而飞牛统一网关只会把请求写进 ${TRIM_APPDEST}/<gatewaySocket>。这个脚本负责：

  1. 监听 gatewaySocket 声明的 socket 路径；
  2. 剥掉 gatewayPrefix（例如 /app/freeclaudecode），还原成 fcc 认识的路径；
  3. 把 Host / Origin 改写成 http://127.0.0.1:<port>，让 fcc 的 loopback 校验通过；
  4. 保留 X-Trim-* 用户头，原样转给上游；
  5. 把 HTML/JS/CSS 响应里的 "/admin" 绝对路径改写成 "<prefix>/admin"，
     这样 Admin 前端挂在网关前缀下也能正常加载资源（不改项目代码）；
  6. 双向流式转发响应（SSE 可用）。

已知限制（骨架阶段接受）：
  - 每个连接只处理一个请求（向上游注入 Connection: close），不复用连接；
  - 只支持带 Content-Length 的请求体；chunked 请求体会被拒绝（400）；
  - 为了让路径改写在未压缩响应上生效，转发时会去掉 Accept-Encoding；
  - 没有 Content-Length 的响应（chunked）只流式透传，不做路径改写。

用法：
    python3 gateway_shim.py --socket /path/fcc.sock --upstream 127.0.0.1:8586 \
        --prefix /app/freeclaudecode
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys

REWRITABLE_TYPES = ("text/html", "javascript", "text/css", "application/json")

# 只改写真正的路径边界：/admin 后面必须紧跟 / " ' ` \ ? # 空白 < 或行尾，
# 这样 /admin.css、/admin.js 这类文件名不会被误改（第一版就踩过这个坑）。
_ADMIN_RE = re.compile(rb"/admin(?=[/\"'`\\?#\s<]|$)")

# JS 里还有正则字面量（例如 /^\/admin\/code\/([0-9a-f-]+)$/），
# 前缀里带斜杠，插进正则会把字面量提前闭合，整段 JS 直接语法错误。
# 所以 JS / JSON / HTML 只改「引号后面」的 /admin，正则里的（前面是 \ 或 ^）一律不碰。
_ADMIN_QUOTED_RE = re.compile(rb"([\"'`])/admin(?=[/\"'`\\?#\s<]|$)")

# 正则字面量里的写法是 \/admin\/（斜杠被转义），这种也要加前缀，
# 但插入的斜杠必须同样转义，否则字面量会被提前闭合。
_ADMIN_ESC_RE = re.compile(rb"(?<=\\)/admin(?=[\\/])")


def _rewrite_request(head: bytes, up_host: str, up_port: int, prefix: str) -> tuple[bytes, int] | None:
    """返回 (改写后的请求头, Content-Length)；无法处理时返回 None。"""
    lines = head.split(b"\r\n")
    if not lines or len(lines[0].split(b" ")) < 2:
        return None
    parts = lines[0].decode("latin-1").split(" ")
    method, target = parts[0], parts[1]
    version = parts[2] if len(parts) > 2 else "HTTP/1.1"

    path, _, query = target.partition("?")
    if prefix and path.startswith(prefix):
        path = path[len(prefix):]
    if not path.startswith("/"):
        path = "/" + path
    new_target = path + (("?" + query) if query else "")

    out = [f"{method} {new_target} {version}".encode("latin-1")]
    content_length = 0
    for raw in lines[1:]:
        if not raw or b":" not in raw:
            continue
        name = raw.split(b":", 1)[0].strip().lower()
        if name in (b"host", b"origin", b"connection", b"accept-encoding", b"proxy-connection"):
            continue
        if name == b"transfer-encoding":
            return None  # chunked 请求体不支持
        if name == b"content-length":
            try:
                content_length = int(raw.split(b":", 1)[1].strip() or b"0")
            except ValueError:
                content_length = 0
        out.append(raw)

    out.append(f"Host: {up_host}:{up_port}".encode("latin-1"))
    out.append(f"Origin: http://{up_host}:{up_port}".encode("latin-1"))
    out.append(b"Connection: close")
    return b"\r\n".join(out) + b"\r\n\r\n", content_length


def _rewrite_body(head: bytes, body: bytes, prefix: str) -> tuple[bytes, bytes] | None:
    """按需改写响应体里的 /admin 前缀；返回 (新响应头, 新响应体)。"""
    if not prefix or not body or b"/admin" not in body:
        return None

    ctype_ok = False
    quoted_only = False
    for line in head.split(b"\r\n")[1:]:
        if line.lower().startswith(b"content-type:"):
            val = line.split(b":", 1)[1].decode("latin-1").lower()
            ctype_ok = any(t in val for t in REWRITABLE_TYPES)
            # JS 与 JSON 里的路径一定在引号里；HTML 属性亦然。CSS 可能有无引号的 url(...)
            quoted_only = "javascript" in val or "application/json" in val or "text/html" in val
    if not ctype_ok:
        return None

    if quoted_only:
        # 匹配到的 "/admin" 前面已经有一个 "\"（转义斜杠），所以替换串不能再带前导反斜杠
        esc_prefix = prefix.replace("/", "\\/")[1:].encode("latin-1") + b"\\/admin"
        new_body = _ADMIN_ESC_RE.sub(esc_prefix, body)
        new_body = _ADMIN_QUOTED_RE.sub(lambda m: m.group(1) + (prefix + "/admin").encode("latin-1"), new_body)
    else:
        new_body = _ADMIN_RE.sub((prefix + "/admin").encode("latin-1"), body)
    lines = []
    for line in head.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            lines.append(f"Content-Length: {len(new_body)}".encode("latin-1"))
        else:
            lines.append(line)
    return b"\r\n".join(lines), new_body


async def handle(reader, writer, up_host, up_port, prefix) -> None:
    up_writer = None
    try:
        try:
            head = await reader.readuntil(b"\r\n\r\n")
        except (asyncio.IncompleteReadError, ConnectionError, asyncio.LimitOverrunError):
            writer.close()
            return

        rewritten = _rewrite_request(head, up_host, up_port, prefix)
        if rewritten is None:
            writer.write(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            await writer.drain()
            writer.close()
            return

        new_head, content_length = rewritten
        body = await reader.readexactly(content_length) if content_length > 0 else b""

        up_reader, up_writer = await asyncio.open_connection(up_host, up_port)
        up_writer.write(new_head)
        if body:
            up_writer.write(body)
        await up_writer.drain()

        try:
            resp_head = await up_reader.readuntil(b"\r\n\r\n")
        except (asyncio.IncompleteReadError, ConnectionError):
            writer.close()
            up_writer.close()
            return

        # 只有带 Content-Length 的响应才缓冲整体（这样才能改写内容）；其余边读边转
        resp_len = None
        for line in resp_head.split(b"\r\n")[1:]:
            if line.lower().startswith(b"content-length:"):
                try:
                    resp_len = int(line.split(b":", 1)[1].strip())
                except ValueError:
                    resp_len = None

        if resp_len is not None:
            payload = await up_reader.readexactly(resp_len)
            changed = _rewrite_body(resp_head, payload, prefix)
            if changed:
                resp_head, payload = changed
            writer.write(resp_head)
            writer.write(payload)
            await writer.drain()
        else:
            writer.write(resp_head)
            await writer.drain()
            try:
                while True:
                    chunk = await up_reader.read(65536)
                    if not chunk:
                        break
                    writer.write(chunk)
                    await writer.drain()
            except (ConnectionError, asyncio.CancelledError):
                pass
    finally:
        for w in (writer, up_writer):
            if w is not None:
                try:
                    w.close()
                except Exception:
                    pass


async def serve(socket_path: str, up_host: str, up_port: int, prefix: str) -> None:
    import os

    try:
        os.unlink(socket_path)
    except FileNotFoundError:
        pass
    server = await asyncio.start_unix_server(
        lambda r, w: handle(r, w, up_host, up_port, prefix), path=socket_path
    )
    os.chmod(socket_path, 0o660)
    print(f"[shim] listening {socket_path} -> {up_host}:{up_port} (prefix={prefix})", flush=True)
    async with server:
        await server.serve_forever()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--socket", required=True)
    ap.add_argument("--upstream", required=True, help="host:port，例如 127.0.0.1:8586")
    ap.add_argument("--prefix", default="", help="网关前缀，例如 /app/freeclaudecode")
    args = ap.parse_args(argv)

    host, _, port = args.upstream.rpartition(":")
    if not host or not port.isdigit():
        print(f"上游地址不合法：{args.upstream}", file=sys.stderr)
        return 2
    try:
        asyncio.run(serve(args.socket, host, int(port), args.prefix))
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
