# Simulator — Jor without a body

**The simulator is V1's body and the project's front door.** It must be so easy to run
that a contributor with zero hardware is talking to Jor within minutes of cloning.

## What it is

A browser app (plus the local perception service) that stands in for the robot:

- **Jor's face** rendered in a window — the *same* face renderer that will ship on
  hardware ([face.md](face.md)), speaking the same command protocol.
- **Webcam = Jor's eyes**, **mic/speakers = Jor's ears and voice** — feeding the same
  perception pipelines ([perception.md](perception.md)).
- Runs alongside the [canvas](canvas.md) — two windows: Jor's face + the teaching canvas.
- Implements the **body interface contract** ([body.md](body.md)), so hardware later is
  "just another driver."

## Why it's critical

1. **V1 ships on it** — the whole companion loop (face, voice, vision, skills, memory)
   is proven in software before a single part is bought.
2. **Community on-ramp** — like Linux needing only a PC, Jor needs only a browser.
   Contributors build skills, faces, and perception improvements against the simulator.
3. **CI** — scripted sessions (recorded video/audio in, expected behavior out) become the
   project's integration tests.

## V1 approach: Hermes Desktop + two Jor components

**Hermes Desktop** (Nous Research's native front end, June 2026) already provides a large
slice of the simulator: full back-and-forth **voice conversations**, a **preview pane**
that renders web pages/files (→ the V1 [canvas](canvas.md)), a file browser (→ a free
first cut of the [memory view](memory.md) — Hermes memory is readable markdown), a
settings UI, and **natural-language cron scheduling** (→ the Financial Advisor's monthly
ritual). It shares one agent core, sessions, skills, and memory with the CLI and gateway.

That reduces our simulator build to the two things that make Jor *Jor*:

1. **The face window** — our expressive renderer ([face.md](face.md)) as a companion
   window, subscribed to agent/session events (via the Hermes gateway) so it reacts
   instantly while the brain thinks.
2. **The perception service** — webcam → emotion signals + pose keypoints
   ([perception.md](perception.md)), injected into Hermes context, driving the
   attentive-teacher flow-breaks.

**Spike done — verdict: glue Hermes Desktop as-is.** (a) External processes can join the
live event WebSocket; (b) perception signals inject via a local MCP server (pull) + a
`pre_llm_call` plugin hook (push), with a small upstream PR for true mid-turn interrupts;
(c) the `open_preview` tool pushes live localhost pages into the pane with no CSP
restrictions. Full recipes and file references: [spike-hermes.md](spike-hermes.md).

## V1 milestones

1. **Face window**: renderer + expression protocol, idle aliveness (blinks, drift).
2. **Voice loop**: mic → STT → Hermes → TTS → speaker, with face reacting instantly
   (listening/thinking) while the brain takes its 2–3 s.
3. **Perception loop**: webcam → local emotion signals + pose keypoints → Hermes context.
4. **Skill sessions**: the three launch skills runnable end-to-end, canvas included.
5. **One-command start**: `docker compose up` or a single script; keys in `.env`.

## Open questions

- Electron/Tauri app vs plain browser tabs? (Plain browser first — least friction.)
- Simulated inputs for CI: a "virtual webcam" fixture format for pose/emotion tests.
