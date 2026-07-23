# Face — how Jor is believed

The face is why people feel connected to Jor rather than to "a speaker with a chatbot."
It must be expressive enough that Kal instinctively reads Jor's state.

The strategy behind it: for humans, **attention is stickiness**. Jor pays visible
attention through [perception](perception.md) — breaking flow with questions and
encouragement like an attentive teacher — and the face **anthropomorphizes** that
attention, compounding the stickiness. A camera that watches is surveillance; eyes that
watch are a relationship.

## Locked decisions

- **Abstract-expressive only.** Eyes/shapes (Cozmo/EMO lineage), never a humanlike
  rendered face. Cheaper, avoids the uncanny valley, and ages well.
- **A real range of emotions**, selected by the session context: the active skill and the
  current moment drive expression (Monk = soft, slow blinks; Advisor = alert, firm; Yoga
  Teacher = encouraging, attentive).
- **Upgradeable emotion packs.** The base set ships with the kernel; skills or extensions
  can add expressions for specific needs.
- **Quirky pack (V2).** A planned first-party pack of playful expressions — wink,
  eye-roll, smirk, mock-surprise, mischief — for humor and personality moments outside
  the base set. Also serves as the reference example for community-built packs.
- **Persona cues are subtle.** The face hints at who Jor is right now (color accent,
  idle animation); the canvas states it explicitly.

## Base emotion set (V1 proposal)

`neutral / idle` · `listening` · `thinking` · `happy / encouraging` · `concerned / empathic`
· `focused / firm` · `sleepy / off-duty` · `confused` (asks Kal to repeat)

Plus micro-behaviors that create "aliveness": blinking, idle drift, gaze toward the
speaker, reaction latency < 300 ms (expressions must react instantly even when the brain
takes 2–3 s to answer — the face acknowledges *hearing* before *answering*).

## Architecture

- **Face renderer = a standalone component** with a small command protocol, e.g.
  `{expression: "empathic", intensity: 0.7, accent: "#8a6", gaze: [x,y]}`.
- Same renderer runs in the browser **simulator** (V1) and on the hardware display (V2) —
  write once, WebGL/canvas-based.
- The protocol is part of the **kernel** ([community.md](community.md)): stable, versioned,
  so community faces/bodies interoperate.

## Reuse vs build

Little exists to glue here — this is one of the genuinely **missing** pieces we build.
Low-fi prior art to study: FluxGarage RoboEyes (Arduino), Vector/Cozmo eye animation
principles, EMO. See [oss-map.md](oss-map.md).

## Decided: eyes + mouth

The face has **both eyes and a mouth** — the mouth smiles and carries expressions
(smile, open-talking, flat/firm, small "o" of surprise/confusion), and animates while
Jor speaks. Prototype renderer lives in [`face/`](../face/) — a standalone page speaking
the expression protocol, with a bridge (`face/bridge.py`) that maps the live Hermes
event stream onto expressions.

## Open questions

- Emotion selection: rule-based from skill config in V1, or model-driven?
- How much personality drift is allowed per skill before Jor stops feeling like one being?
