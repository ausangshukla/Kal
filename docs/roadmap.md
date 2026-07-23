# Roadmap — V1 → V2 → V10

## V1 — "Jor lives" (software only, ~3 months)

**Definition of done: the founder uses Jor daily, by choice.**

- Simulator: face window + voice loop + webcam perception ([simulator.md](simulator.md))
- Hermes Agent backend wired to Anthropic cloud models ([brain.md](brain.md))
- Skill system: format extensions + persona switching ([skills.md](skills.md))
- Three launch skills: Monk, Financial Advisor (monthly ritual), Yoga Teacher (10 poses)
- Memory: Hermes native + namespaces + the editable memory view ([memory.md](memory.md))
- Canvas V1 on Hermes screens ([canvas.md](canvas.md))
- Docs + repo public-ready (naming decision pending — [community.md](community.md))

**Suggested build order** (each step usable by itself):
1. Hermes up, talking to cloud model — text only
2. Voice loop (STT/TTS) + face window with instant reactions
3. First skill end-to-end: **Financial Advisor** (no vision needed — pure persona +
   canvas + ritual + memory; hardest product questions, easiest tech)
4. Perception service: emotion signals → context; **Monk** skill
5. Pose pipeline; **Yoga Teacher** skill
6. Memory view, settings, one-command start, contributor docs

## V2 — "Jor takes shape"

- **Hardware reference design**: lamp-sized, commodity BOM, honest mute ([body.md](body.md))
- **Tracking & metrics**: quantified 10x — streaks, progress, dashboards ([vision.md](vision.md))
- **Dual-interaction canvas**: shared drawing/annotation surface ([canvas.md](canvas.md))
- Physical degrees of freedom (pan/tilt gaze) as a V2.x extension
- **Quirky face pack**: wink, eye-roll, smirk, mischief — the first-party example of an
  emotion-pack extension ([face.md](face.md))
- Skill-authoring ecosystem push: template repo, tutorial, first outside contributors
- Memory research findings folded in (decay, consolidation, cross-skill consent)

## V3+ — "Jor multiplies" (unordered candidates)

- Skill registry with a real trust/curation mechanism
- More Kals: multi-user, family setups
- Any-screen canvas, mobile companion
- Richer emotion packs, community faces
- Local-first everything on affordable hardware

## V10 — "Talus"

Jor's brain on his own chip: edge inference baked into the body. Pure dream today; the
only present-day obligation is keeping model placement behind the policy engine so the
dream stays cheap to attempt ([brain.md](brain.md)).
