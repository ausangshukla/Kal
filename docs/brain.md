# Brain — how Jor thinks

## Locked decisions

- **V1 backend: [Hermes Agent](https://github.com/nousresearch/hermes-agent)** (Nous
  Research). It already provides the agent loop, markdown skills, persistent memory,
  70+ tools, subagent orchestration, and works with Anthropic/cloud and local
  (Ollama/vLLM) models. We glue; we don't rewrite.
- **Target architecture: orchestrator.** A fast local layer handles perception,
  acknowledgment, and interruptions; a big cloud model (Opus/Fable via API) handles
  reasoning, teaching, and planning. In V1 this may collapse to "Hermes + cloud model"
  with perception feeding it signals.
- **Latency: 2–3 s conversational turns are acceptable.** The [face](face.md) covers the
  gap by reacting instantly (listening/thinking expressions).
- **Runs everywhere, like Linux — hardware tiers:**

  | Tier | Perception | Reasoning | Canvas |
  |---|---|---|---|
  | Low-end (any laptop) | Cloud | Cloud | On the PC/laptop |
  | Mid (decent CPU/GPU) | Local | Cloud | On the PC/laptop |
  | High (workstation GPU) | Local | Local or split | On the PC/laptop |

- **Local/cloud placement is policy, not code**: each skill declares preferred placement
  (e.g., the Monk may demand fully-local for intimacy); **global user overrides win**
  over skill config.
- **Talus** (Jor's own inference silicon) is a **V10 dream** — no design work now, but
  the placement-policy abstraction above is what makes it possible later.

## Prototyping setup (current)

Model choice is **config, not code** — the first live exercise of the placement-policy
principle:

- **Now (prototyping): Gemini Flash** — cheap and fast. Hermes `~/.hermes/config.yaml`:
  `model.provider` pointing at Google's OpenAI-compatible endpoint with
  `models/gemini-3-flash-preview`; key in the Hermes config/`.env`.
- **Later (quality): Anthropic** — switch with
  `hermes config set model anthropic/<model>` (or the interactive `hermes model`) plus
  `ANTHROPIC_API_KEY` in `~/.hermes/.env`. No Jor code changes.
- Skills must therefore never assume a specific model — prompts are written
  model-agnostic, and anything model-sensitive belongs in skill `config.yaml`.

## The interaction loop — who drives?

Three layers, from hard-coded to freeform:

1. **Reflex layer (code-driven, deterministic).** The face reacts to the gateway event
   stream (listening/thinking/speaking/working) and the perception service injects
   signals every turn. No model in this loop; it's why Jor feels alive at <300 ms while
   the brain takes 2–3 s.
2. **Session structure (skill-scripted).** A skill's SKILL.md defines flows (the finance
   ritual's six steps) and its **modality** ([skills.md](skills.md)) defines the loop
   shape — socratic: ask → listen → probe → only then teach → display on canvas. The
   model follows the script, but enforcement is prompt-level, not code-level.
3. **Cognition (model-driven, freeform).** Within a step, the model decides what to say,
   when to call `open_preview`, when to break flow on a perception signal.

So V1 is a **freeform core inside a scripted shell inside a reflex loop**. If
prompt-level enforcement proves too loose (model skips ritual steps, forgets the canvas),
the session/persona manager grows into a code-level state machine that feeds the model
one step at a time — that's the escalation path, not the starting point.

## What we build (the glue)

1. **The perception bus**: local vision/audio pipelines ([perception.md](perception.md))
   publishing derived signals into Hermes context.
2. **The placement policy engine**: skill config + global overrides → which model/endpoint
   serves which function (STT, TTS, reasoning, vision).
3. **The face/canvas bridge**: brain events → face expressions and canvas content.
4. **Session/persona manager**: one skill active at a time; loading a skill switches
   Jor's persona, canvas theme, and memory namespace.

## Open questions

- How deep can we reach into Hermes without forking? Prefer extension points; upstream
  patches where missing (good for the community relationship too).
- Interruption handling: can Kal talk over Jor and be heard? (Needs local VAD even in
  the low-end tier.)
- Which cloud model per function: big model for teaching/planning, small cheap model for
  chit-chat and acknowledgments?
