# Spike results — Hermes integration points (2026-07-23)

Verdict: **glue Hermes Desktop as-is.** All three integration points exist today; two
small upstream PRs would make them nicer. Verified against Hermes Agent v0.19.0 source
(`~/.hermes/hermes-agent`). File references below are into that repo.

## 1. Event stream for the face window — YES, zero changes

The desktop app receives live agent state over a WebSocket carrying JSON-RPC events, and
an external process can join it:

- Connect to `ws://127.0.0.1:9119/api/ws?token=<SESSION_TOKEN>` (send an
  `Origin: http://127.0.0.1:9119` header). Server: `hermes_cli/web_server.py:18148`,
  handler `tui_gateway/ws.py:283`.
- Token: parse `window.__HERMES_SESSION_TOKEN__` from `GET http://127.0.0.1:9119/`, or
  pin `HERMES_DASHBOARD_SESSION_TOKEN` when starting the backend.
- Event vocabulary maps cleanly onto face states: `status.update` /`reasoning.delta`
  (thinking), `message.start`/`message.delta`/`message.complete` (responding),
  `tool.start`/`tool.progress`/`tool.complete` (working), `turn.start`/`turn.end`,
  `session.*`, `approval.request`, `clarify.request`.
- Desktop plugins get the same stream via `host.onEvent` (`apps/desktop/src/sdk/index.ts:93`)
  — so the face could alternatively ship as a **Hermes Desktop plugin** instead of a
  separate window.
- Gap: no "user speech started" event (mic-side). Small PR: emit a `GatewayNotice` from
  `hermes_cli/voice.py` through `gateway/stream_events.py`. Until then the face window
  can watch the mic itself.

**Live-test correction (2026-07-23):** session events are routed to **the one transport
that owns the session** (`write_json`, `tui_gateway/server.py:1194` — `session["transport"]`
is singular); only session-less globals broadcast to all connected peers. So a second,
passive WS connection does NOT see events for turns driven from Hermes Desktop's own
socket. Consequences:
- **Workaround now:** `face/bridge.py` tails `~/.hermes/logs/agent.log`, whose lines
  (voice transcription, stream-request open, tool completed, turn ended) map cleanly to
  listening/thinking/focused/speaking.
- **Proper fixes:** (a) a **Hermes Desktop plugin** — plugins run inside the owning
  transport and get the full stream via `host.onEvent('*')` (`apps/desktop/src/sdk`);
  (b) upstream PR: a read-only `/api/face`-style broadcast endpoint mirroring
  `events_ws` (`hermes_cli/web_server.py:18207`). PR (b) is promoted to top of the
  upstream list.
- Also note: gateway lifecycle **hooks** (`~/.hermes/hooks/`) fire only in the messaging
  gateway (`gateway/run.py`), not for Desktop chat sessions — not a face signal source.
- Hermes Desktop spawns its backend on a **random port** with the session token in the
  child process env (`HERMES_DASHBOARD_SESSION_TOKEN`) — the bridge auto-discovers via
  `ss -tlnp` + `/proc/<pid>/environ`; `HERMES_PORT`/`HERMES_TOKEN` override.

## 2. Perception-signal injection — YES for next-turn; interrupt needs a tiny PR

Recommended combination:

- **Pull (yoga keypoints, on demand):** a local **MCP server** in the perception service
  exposing `get_pose_keypoints()` / `get_user_state()`; registered under `mcp_servers:`
  in config (hot-reloaded). The agent calls it like any tool.
- **Push (ambient signals, every turn):** a **`pre_llm_call` plugin hook**
  (`hermes_cli/plugins.py:1158`, consumed in `agent/turn_context.py:844`) that reads the
  perception service's latest state and returns `{"context": "[perception] Kal seems
  confused (0.8)"}` — appended to the user message of every turn. Supported, no core
  changes.
- **Interrupt / wake an idle session (the attentive-teacher flow-break):** not externally
  reachable today. The machinery exists (`AIAgent.steer()` `run_agent.py:2944`, busy
  router `gateway/run.py:6001`); smallest extension is a ~30-line authenticated route
  `POST /api/sessions/{id}/inject` in `gateway/platforms/api_server.py:1556` that calls
  `steer()`/`handle_message()`. This is our first upstream PR candidate — V1 can start
  with pull+push only (Jor reacts at the next turn, good enough at 2–3 s cadence).
- Dead ends confirmed: `hermes send` is outbound-only; webhooks spawn isolated sessions;
  `prefill_messages_file` is start-of-session only.

## 3. Canvas via the preview pane — YES, zero changes

- The agent-side tool **`open_preview`** (`tools/open_preview_tool.py`, active when
  `HERMES_DESKTOP=1`) pushes `{url, label}` to the desktop, which renders it in a real
  Chromium `<webview>` — JS, WebSocket, canvas, WebGL all work, **no host CSP**.
- **Live localhost pages work**: the perception service serves
  `http://localhost:<port>/overlay` (live yoga skeleton via its own WebSocket) and the
  skill calls `open_preview("localhost:<port>/overlay", "Pose Coach")`.
- **File mode**: `open_preview("/path/lesson.html")` renders live and **auto-reloads on
  file rewrite** (~200 ms debounce) — a skill can advance slides by overwriting the file.
- Caveat: `getUserMedia` **camera is denied inside the pane** (`electron/main.ts:5232`)
  — correct for us anyway: the perception service owns the webcam and streams
  keypoints to the page.
- Theming: bake it into the served HTML/CSS for V1. Optional ~10-line upstream PR adds
  a `themeCss` field injected via `webview.insertCSS` (`preview-pane.tsx:588`).

## Skill loading from this repo — WORKING

`~/.hermes/config.yaml` → `skills.external_dirs: [/home/thimmaiah/work/kal/skills]`.
Skills here are discovered and indexed (verified with `skills/coaching/financial-advisor`).
Two gotchas hit and solved:
- `hermes config set` stored the JSON list as a *string* — external_dirs must be a real
  YAML list (edit the file or use a YAML-aware tool).
- Hermes treats external skill dirs as read-only for its autonomous curator — good:
  our repo stays the source of truth (`agent/skill_utils.py:591`).

## Consequences for the V1 architecture

1. The **face** can be a standalone WS client *or* a Hermes Desktop plugin — decide
   after prototyping the renderer.
2. The **perception service** is one process with three faces: webcam pipelines, an MCP
   server (pull), a state endpoint the `pre_llm_call` hook reads (push), plus the
   localhost overlay pages the canvas renders.
3. **Upstream PR list (small, high-leverage):** session-inject route (steer),
   user-speech event, `themeCss` on `open_preview`.
