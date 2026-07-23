# Neo — the skill system

*"I know kung fu."* Skills are downloaded into Jor; Kal learns them from Jor. A skill
turns Jor into a psychologist, a yoga teacher, a financial advisor — set up from the
computer or by voice command.

## Locked decisions

- **Format: an LLM skill folder** — markdown instructions + tools + config — **borrowed
  and enhanced from [Hermes Agent](https://github.com/nousresearch/hermes-agent)**, whose
  skills are already plain markdown files. We extend the format rather than invent one.
- **One skill active at a time.** The active skill defines Jor's persona; the canvas
  states it explicitly and the face cues it subtly.
- **Persona resolution:** global user override → else skill config. (Kal can pin "always
  gentle" or "always drill-sergeant" across every skill.)
- **Every skill declares a `modality`** — *how* it teaches, distinct from *who* the
  persona is. The modality defines the interaction loop the skill runs:
  - `socratic` — Jor leads with questions, never gives the answer while a question can
    get Kal there; answers earn follow-up questions. **First experiment.**
  - `instruct` — direct teaching: explain → example → check understanding.
  - `coach` — ritual/accountability loops (the Financial Advisor's monthly review).
  - `observe-correct` — watch Kal perform, interject corrections (Yoga Teacher).
  - `companion` — open listening, minimal steering (the Monk's check-ins).
  Modality is declared in `config.yaml`, shapes the SKILL.md session flows, and tunes
  the perception flow-break cadence ([perception.md](perception.md)) — socratic breaks
  flow *often* (questions are the medium), companion rarely. Kal's global override can
  force a modality across skills (e.g. "teach me everything socratically").
- **Commercial and FOSS skills both allowed.**
- **Marketplace: undecided — safety first.** Anything touching mental health, money, or
  the body needs a trust story before an open registry exists. Until then: skills are
  folders you install deliberately, and a small curated set ships with Jor.

## Proposed skill folder layout (extends Hermes)

```
skills/monk/
  SKILL.md          # persona, teaching style, boundaries, session flows
  config.yaml       # placement policy (local/cloud), face pack, canvas theme,
                    # activation phrases, memory namespace, schedule hooks
  tools/            # skill-specific tools (e.g., breathing-timer)
  canvas/           # teaching assets: slides, diagrams, reference media
  face/             # optional extra expressions (emotion pack)
  safety.md         # red lines, escalation rules, disclaimers
```

The `config.yaml` + `safety.md` + `canvas/` + `face/` extensions on top of vanilla
Hermes skills are **our build** — designed as upstreamable where possible.

## The three launch skills

### 1. Monk (psychologist / meditation)
- Daily check-ins, guided meditation, CBT-style reflection, mood memory over months.
- **Safety is the feature**: not a therapist, says so plainly; crisis detection →
  hands off to real human resources immediately; strongest privacy default (candidate
  for fully-local mode).

### 2. Financial Advisor
- **The monthly ritual**: Jor *initiates* ("Kal, it's the 1st — finance review time"),
  walks through the month on the canvas, extracts one improvement commitment, and
  follows up on last month's commitment.
- V1 data entry: manual / CSV import. No bank-account linking in V1.
- Education-not-advice framing; jurisdiction disclaimers in `safety.md`.

### 3. Yoga Teacher
- 10 common poses, visual correction via [perception.md](perception.md).
- Canvas shows reference pose + live skeleton overlay; Jor speaks corrections.
- Session memory: which poses improve, which corrections repeat.

## Open questions

- Skill signing/verification story for the eventual registry (research: how do Debian,
  F-Droid, and VS Code marketplace each handle trust?).
- Can a skill *degrade gracefully* when its preferred placement (e.g., fully-local) is
  unavailable — refuse to run, or run with a warning?
- Skill-authoring guide + template repo (critical for the community — see
  [community.md](community.md)).
