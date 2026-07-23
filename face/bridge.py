#!/usr/bin/env python3
"""Jor face bridge: Hermes gateway events -> face expression commands.

Connects to the Hermes dashboard WebSocket (ws://127.0.0.1:9119/api/ws),
maps agent events onto face expressions, and rebroadcasts them to the face
page over ws://localhost:8732. Also serves the face page on
http://localhost:8731.

Run:  python3 face/bridge.py        (needs: pip install websockets)
Then open http://localhost:8731 — status shows "live" when connected.
"""

import asyncio
import functools
import http.server
import json
import os
import re
import subprocess
import threading
import time
import urllib.request
import sys
from pathlib import Path

try:
    import websockets
except ImportError:
    raise SystemExit("pip install websockets")

FACE_HTTP_PORT = 8731
FACE_WS_PORT = 8732

# event type -> expression command
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

def discover() -> tuple[str | None, str | None]:
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
    try:
        with urllib.request.urlopen(base + "/", timeout=5) as r:
            html = r.read().decode("utf-8", "replace")
        m = re.search(r"__HERMES_SESSION_TOKEN__\s*=\s*['\"]([^'\"]+)['\"]", html)
        if m: return base, m.group(1)
    except: pass
    
    return None, None

async def broadcast(cmd: dict):
    dead = set()
    for ws in clients:
        try:
            await ws.send(json.dumps(cmd))
        except Exception:
            dead.add(ws)
    clients.difference_update(dead)

_last_plugin_event = 0.0
_voice_active_until = 0.0  # rolling: set on real TTS playback


async def _handle_plugin_event(etype: str):
    """Map a live desktop event to a face expression.

    Voice-aware: the mouth follows actual TTS playback (audio.play/audio.stop
    from the plugin's audio tap), not the text stream. While a voice session
    is active (TTS heard in the last 15 min), streaming text renders as
    *thinking* — Jor is composing what he's about to say — and speaking waits
    for the audio.
    """
    global _turn_end_task, _voice_active_until
    now = time.time()
    voice_mode = now < _voice_active_until

    def cancel_settle():
        global _turn_end_task
        if _turn_end_task:
            _turn_end_task.cancel()
            _turn_end_task = None

    if etype == "audio.play":
        _voice_active_until = now + 900
        cancel_settle()
        await broadcast({"expression": "speaking"})
    elif etype == "audio.stop":
        cancel_settle()
        _turn_end_task = asyncio.create_task(_settle_sequence())
    elif etype in ("turn.end", "message.complete"):
        cancel_settle()
        if voice_mode:
            # audio may still be coming — hold, settle only if it never arrives
            _turn_end_task = asyncio.create_task(_delayed_settle(6.0))
        else:
            _turn_end_task = asyncio.create_task(_settle_sequence())
    else:
        cmd = EVENT_MAP.get(etype)
        if cmd:
            if voice_mode and cmd["expression"] == "speaking":
                cmd = {"expression": "thinking"}
            cancel_settle()
            await broadcast(cmd)


async def _delayed_settle(delay: float):
    await asyncio.sleep(delay)
    await _settle_sequence()


async def face_client(ws):
    """Face pages AND the desktop plugin connect here. The plugin sends
    {"hermesEvent": type} frames (real-time, per-token) which take priority
    over the log-tail fallback; {"expression": ...} frames (trigger CLI,
    tests) broadcast as-is."""
    global _last_plugin_event, _turn_end_task
    clients.add(ws)
    try:
        async for message in ws:
            try:
                obj = json.loads(message)
            except json.JSONDecodeError:
                continue
            etype = obj.get("hermesEvent")
            if etype:
                _last_plugin_event = time.time()
                await _handle_plugin_event(etype)
            elif "expression" in obj:
                await broadcast(obj)
    finally:
        clients.discard(ws)

async def hermes_loop():
    while True:
        try:
            base, token = discover()
            if not base:
                await asyncio.sleep(5)
                continue
            url = base.replace("http://", "ws://") + f"/api/ws?token={token}"
            async with websockets.connect(url, origin=base, ping_interval=20) as ws:
                print(f"bridge: connected to Hermes event stream at {base}")
                await broadcast(EVENT_MAP["gateway.ready"])
                async for raw in ws:
                    frame = json.loads(raw)
                    if frame.get("method") == "event":
                        etype = (frame.get("params") or {}).get("type", "")
                        cmd = EVENT_MAP.get(etype)
                        if cmd:
                            print(f"bridge: event {etype} -> {cmd['expression']}")
                            await broadcast(cmd)
        except Exception as e:
            print(f"bridge: hermes connection lost ({e}); retrying in 3s")
            await asyncio.sleep(3)

# agent.log line pattern -> expression. Patterns verified against a live
# desktop-session turn (see docs/spike-hermes.md addendum): the WS event
# stream is per-session-transport, so for Desktop-driven turns the log is
# currently the only external signal source.
LOG_PATTERNS = [
    (re.compile(r"Transcribed .* via local whisper"), {"expression": "listening"}),
    (re.compile(r"OpenAI client created \(chat_completion_stream"), {"expression": "thinking"}),
    (re.compile(r"agent\.tool_executor: tool \S+ completed"), {"expression": "focused"}),
    (re.compile(r"agent\.tool_executor: Tool .* returned error"), {"expression": "confused", "intensity": 0.7}),
]
TURN_END = re.compile(r"conversation_loop: Turn ended")

_turn_end_task = None


async def _turn_end_sequence():
    """Log-tail path: response already streamed by the time the log line
    lands — talk briefly, smile, settle."""
    await broadcast({"expression": "speaking"})
    await asyncio.sleep(2.5)
    await _settle_sequence()


async def _settle_sequence():
    """Plugin path: speaking already happened live — smile, then rest."""
    await broadcast({"expression": "happy", "intensity": 0.6})
    await asyncio.sleep(1.5)
    await broadcast({"expression": "idle"})


async def log_watcher():
    """Tail agent.log and derive expressions for Desktop-driven turns."""
    global _turn_end_task
    log_path = Path.home() / ".hermes" / "logs" / "agent.log"
    if not log_path.exists():
        print(f"bridge: agent.log not found at {log_path}")
        return

    print(f"bridge: tailing {log_path}")
    f = open(log_path, "r")
    f.seek(0, 2)  # end
    while True:
        line = f.readline()
        if not line:
            # handle rotation/truncation
            try:
                if log_path.stat().st_size < f.tell():
                    f.close()
                    f = open(log_path, "r")
            except OSError:
                pass
            await asyncio.sleep(0.3)
            continue

        # the desktop plugin's real-time events supersede the log tail
        if time.time() - _last_plugin_event < 8:
            continue

        if TURN_END.search(line):
            if _turn_end_task:
                _turn_end_task.cancel()
            _turn_end_task = asyncio.create_task(_turn_end_sequence())
            continue
        for pat, cmd in LOG_PATTERNS:
            if pat.search(line):
                if _turn_end_task:
                    _turn_end_task.cancel()
                    _turn_end_task = None
                await broadcast(cmd)
                break

def serve_static():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(Path(__file__).parent))
    http.server.ThreadingHTTPServer(("0.0.0.0", FACE_HTTP_PORT), handler).serve_forever()

async def main():
    threading.Thread(target=serve_static, daemon=True).start()
    asyncio.create_task(log_watcher())
    print(f"face page:  http://localhost:{FACE_HTTP_PORT}")
    async with websockets.serve(face_client, "0.0.0.0", FACE_WS_PORT):
        await hermes_loop()

async def test_trigger(expression, intensity=1.0):
    try:
        async with websockets.connect(f"ws://localhost:{FACE_WS_PORT}") as ws:
            await ws.send(json.dumps({"expression": expression, "intensity": intensity}))
            print(f"Triggered: {expression}")
    except Exception as e:
        print(f"Failed to trigger: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "trigger":
        expr = sys.argv[2] if len(sys.argv) > 2 else "happy"
        try:
            intensity = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        except:
            intensity = 1.0
        asyncio.run(test_trigger(expr, intensity))
    else:
        asyncio.run(main())
