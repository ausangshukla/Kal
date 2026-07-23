#!/usr/bin/env python3
"""Jor face bridge: Hermes gateway events -> face expression commands.

Connects to the Hermes dashboard WebSocket (ws://127.0.0.1:9119/api/ws),
maps agent events onto face expressions, and rebroadcasts them to the face
page over ws://localhost:8732. Also serves the face page on
http://localhost:8731.

Run:  python3 face/bridge.py        (needs: pip install websockets)
Then open http://localhost:8731 — status shows "live" when connected.

The face page works without this bridge too (demo mode with buttons).
"""

import asyncio
import functools
import http.server
import json
import os
import re
import subprocess
import threading
import urllib.request
from pathlib import Path

try:
    import websockets
except ImportError:
    raise SystemExit("pip install websockets")

FACE_HTTP_PORT = 8731
FACE_WS_PORT = 8732

# event type -> expression command; None payload = ignore event
EVENT_MAP = {
    "gateway.ready":    {"expression": "happy", "intensity": 0.6},
    "turn.start":       {"expression": "listening"},
    "turn.started":     {"expression": "listening"},
    "status.update":    {"expression": "thinking"},
    "reasoning.delta":  {"expression": "thinking"},
    "thinking.delta":   {"expression": "thinking"},
    "reasoning.available": {"expression": "thinking"},
    "message.start":    {"expression": "speaking"},
    "message.delta":    {"expression": "speaking"},
    "message.complete": {"expression": "idle"},
    "turn.end":         {"expression": "happy", "intensity": 0.5},
    "turn.error":       {"expression": "concerned"},
    "error":            {"expression": "concerned"},
    "tool.start":       {"expression": "focused"},
    "tool.started":     {"expression": "focused"},
    "tool.progress":    {"expression": "focused"},
    "tool.complete":    {"expression": "thinking", "intensity": 0.6},
    "clarify.request":  {"expression": "confused"},
    "approval.request": {"expression": "surprised", "intensity": 0.6},
    "session.interrupt": {"expression": "listening"},
}

clients: set = set()


def _token_from_environ(pid: str) -> str | None:
    try:
        env = open(f"/proc/{pid}/environ", "rb").read().decode(errors="replace")
    except OSError:
        return None
    for kv in env.split("\0"):
        if kv.startswith("HERMES_DASHBOARD_SESSION_TOKEN="):
            return kv.split("=", 1)[1]
    return None


def discover() -> tuple[str, str]:
    """Find the Hermes backend: (http base, session token).

    Order: HERMES_PORT/HERMES_TOKEN env override -> scan running hermes
    processes for their listen port + env token (Hermes Desktop spawns a
    headless backend on a random port) -> classic `hermes dashboard` on
    9119 (token scraped from the served SPA).
    """
    port, tok = os.environ.get("HERMES_PORT"), os.environ.get("HERMES_TOKEN")
    if port and tok:
        return f"http://127.0.0.1:{port}", tok

    try:
        out = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if "hermes" not in line.lower() or "127.0.0.1:" not in line:
                continue
            pm = re.search(r"127\.0\.0\.1:(\d+)", line)
            im = re.search(r"pid=(\d+)", line)
            if not (pm and im):
                continue
            tok = _token_from_environ(im.group(1))
            if tok:
                return f"http://127.0.0.1:{pm.group(1)}", tok
    except OSError:
        pass

    base = "http://127.0.0.1:9119"
    with urllib.request.urlopen(base + "/", timeout=5) as r:
        html = r.read().decode("utf-8", "replace")
    m = re.search(r"__HERMES_SESSION_TOKEN__\s*=\s*['\"]([^'\"]+)['\"]", html)
    if not m:
        raise RuntimeError("no Hermes backend found — launch `hermes desktop` or `hermes dashboard`")
    return base, m.group(1)


async def broadcast(cmd: dict):
    dead = set()
    for ws in clients:
        try:
            await ws.send(json.dumps(cmd))
        except Exception:
            dead.add(ws)
    clients.difference_update(dead)


async def face_client(ws):
    clients.add(ws)
    try:
        await ws.wait_closed()
    finally:
        clients.discard(ws)


async def hermes_loop():
    """Connect to the Hermes event stream; retry forever."""
    while True:
        try:
            base, token = discover()
            url = base.replace("http://", "ws://") + f"/api/ws?token={token}"
            async with websockets.connect(
                url, origin=base, ping_interval=20
            ) as ws:
                print(f"bridge: connected to Hermes event stream at {base}")
                await broadcast(EVENT_MAP["gateway.ready"])
                async for raw in ws:
                    for line in str(raw).splitlines():
                        try:
                            frame = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if frame.get("method") != "event":
                            continue
                        etype = (frame.get("params") or {}).get("type", "")
                        cmd = EVENT_MAP.get(etype)
                        if cmd:
                            await broadcast(cmd)
        except Exception as e:
            print(f"bridge: hermes connection lost ({e}); retrying in 3s")
            await asyncio.sleep(3)


def serve_static():
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(Path(__file__).parent)
    )
    http.server.ThreadingHTTPServer(("127.0.0.1", FACE_HTTP_PORT), handler).serve_forever()


async def main():
    threading.Thread(target=serve_static, daemon=True).start()
    print(f"face page:  http://localhost:{FACE_HTTP_PORT}")
    async with websockets.serve(face_client, "127.0.0.1", FACE_WS_PORT):
        await hermes_loop()


if __name__ == "__main__":
    asyncio.run(main())
