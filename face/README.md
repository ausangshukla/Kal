# Jor's face — prototype renderer

Abstract-expressive **eyes + mouth** on a canvas. Speaks expression protocol v0:

```js
setExpression({ expression: "happy", intensity: 0.8, accent: "#7ec8ff" })
```

12 base poses: `idle listening thinking speaking happy empathic firm focused confused
concerned sleepy surprised` — smooth interpolation between them, plus aliveness
(blinking, gaze drift, breathing, talking mouth modulation).

## Run

**Demo mode** (no Hermes needed): open `index.html` in a browser — click the pose
buttons.

**Live mode** (reacts to the real agent):

```bash
pip install websockets
hermes serve &          # or launch Hermes Desktop (serves the same gateway)
python3 face/bridge.py  # then open http://localhost:8731
```

The bridge scrapes the dashboard session token, subscribes to the Hermes event
WebSocket (`/api/ws`), maps events → expressions (`EVENT_MAP` in `bridge.py`), and
rebroadcasts to the page on `ws://localhost:8732`. Status pill shows `live` when
connected; the page falls back to demo mode when the bridge is absent.

See [docs/spike-hermes.md](../docs/spike-hermes.md) for the event vocabulary.
