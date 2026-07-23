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
import re
import threading
import urllib.request
from pathlib import Path

try:
    import websockets
except ImportError:
    raise SystemExit("pip install websockets")

HERMES_HTTP = "http://127.0.0.1:9119"
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


def fetch_token() -> str:
    """Scrape the dashboard session token from the served SPA."""
    with urllib.request.urlopen(HERMES_HTTP + "/", timeout=5) as r:
        html = r.read().decode("utf-8", "replace")
    m = re.search(r"__HERMES_SESSION_TOKEN__\s*=\s*['\"]([^'\"]+)['\"]", html)
    if not m:
        raise RuntimeError("session token not found — is `hermes serve`/desktop running?")
    return m.group(1)


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
            token = fetch_token()
            url = f"ws://127.0.0.1:9119/api/ws?token={token}"
            async with websockets.connect(
                url, origin=HERMES_HTTP, ping_interval=20
            ) as ws:
                print("bridge: connected to Hermes event stream")
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
