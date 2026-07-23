# Jor — a companion that makes you Superman

**Jor** is an embodied AI companion whose single job is to make its human — **Kal** — 10x:
mentally stronger, physically healthier, financially sharper, and faster at learning
anything. Jor is a teacher, coach, and companion with a face you can believe, eyes that
read you, a voice that talks with you, and a canvas he teaches on.

> Working names. "Jor" and "Kal" derive from Superman lore (Jor-El / Kal-El) with the
> "-El" removed. Internal codenames for now — see [community.md](docs/community.md#naming)
> for the trademark question before any public launch.

## The idea in one picture

```
                ┌──────────────────────── THE BRAIN ────────────────────────┐
                │  Cloud LLM (Opus/Fable)  ←→  Local models (optional GPU)  │
                │            V1 backend: Hermes Agent (Nous Research)       │
                └──────────────▲────────────────────────▲──────────────────┘
                               │                        │
   ┌── JOR (the body) ─────────┴──┐      ┌── THE CANVAS ┴───────────────┐
   │ • Digital face: abstract,    │      │ Browser app on the PC/laptop │
   │   expressive emotions        │      │ where Jor teaches: slides,   │
   │ • Mic + speaker (talk/listen)│      │ diagrams, finances, poses.   │
   │ • Camera eyes: reads Kal's   │      │ V1: Hermes screens.          │
   │   face, checks yoga poses    │      └──────────────────────────────┘
   │ • Lamp-sized, commodity parts│
   │ • V1 = SIMULATOR in browser  │      ┌── NEO (skill system) ────────┐
   └──────────────────────────────┘      │ Markdown skill folders that  │
                                         │ turn Jor into a monk, a      │
                                         │ financial advisor, a yoga    │
                                         │ teacher… one persona at a    │
                                         │ time. Community-built.       │
                                         └──────────────────────────────┘
```

## Principles

1. **Glue first, build second.** Reuse the best of open source (Hermes, Whisper, Piper,
   MediaPipe, Ollama…); build only what's missing. The build-vs-reuse ledger lives in
   [oss-map.md](docs/oss-map.md).
2. **Runs everywhere, like Linux.** Low-end hardware → everything in the cloud. High-end →
   fully local. The split is configurable globally and per skill.
3. **One persona at a time.** A skill defines who Jor is right now (monk, advisor, yoga
   teacher), signaled through the canvas and subtle facial cues. Global overrides win.
4. **Kal owns the memory.** Jor's memory of Kal is visible and editable by Kal. Privacy
   (what leaves the device) is user-configurable, per skill if desired.
5. **Kernel + extensions.** A small trusted core (runtime, skill API, memory, face
   protocol) guarded by few maintainers; everything else is an extension anyone can build.
6. **Safety first** for anything that touches mental health, money, or the body.

## V1 — software only, 3 launch skills

No robot yet. A **browser simulator** (Jor's face + webcam + mic) proves the companion
loop, built on **Hermes Agent** as the backend, with three skills:

| Skill | What Jor becomes | Hard part |
|---|---|---|
| **Monk** | Psychologist / meditation guide for mental health | Safety, tone, memory of emotional context |
| **Financial Advisor** | Forces a monthly finance review & improvement ritual | Persistence, scheduling, ritual design |
| **Yoga Teacher** | Watches Kal do 10 common poses and corrects form | Real-time pose estimation (local vision) |

Conversation latency target: 2–3 s is acceptable. Emotion/vision runs local where
hardware allows; reasoning/teaching in the cloud.

## Components

| Doc | Component |
|---|---|
| [vision.md](docs/vision.md) | Why Jor exists, what 10x means, who Kal is |
| [body.md](docs/body.md) | The physical robot: lamp-sized, commodity parts (V2) |
| [face.md](docs/face.md) | Abstract expressive face, emotion rendering |
| [perception.md](docs/perception.md) | Camera eyes: emotion reading, yoga pose vision |
| [brain.md](docs/brain.md) | Orchestration, Hermes backend, local/cloud policy |
| [skills.md](docs/skills.md) | Neo: the skill format, personas, the 3 launch skills |
| [memory.md](docs/memory.md) | What Jor remembers, transparency, research agenda |
| [canvas.md](docs/canvas.md) | The teaching surface on the PC/laptop |
| [simulator.md](docs/simulator.md) | Browser-based Jor — V1's body and the contributor on-ramp |
| [oss-map.md](docs/oss-map.md) | Reuse-vs-build ledger across every subsystem |
| [community.md](docs/community.md) | Linux-style governance, licensing, naming |
| [roadmap.md](docs/roadmap.md) | V1 → V2 → V10 (Talus) |

## Status

Pre-code. Docs-first design phase, July 2026. Next step: stand up Hermes Agent, then the
simulator skeleton (see [roadmap.md](docs/roadmap.md)).
