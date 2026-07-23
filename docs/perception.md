# Perception — Jor's eyes and ears

Jor's differentiator over every chat assistant: he **watches and reads Kal** while
teaching. Perception is local-first wherever hardware allows.

## Locked decisions

- **Vision (face/emotion reading) and short reactions run locally** when a capable
  machine exists; on low-end setups everything falls back to cloud. Specific modes may
  force fully-local. The policy is set per skill with global overrides winning
  (see [brain.md](brain.md)).
- **Privacy is user-configurable, per skill.** Default stance to design toward: raw
  camera/mic never leaves the device; only derived signals ("Kal seems tired",
  "left arm too low") go to the cloud brain.
- **Yoga vision is scoped tight**: recognize and correct **10 common poses** only.

## Graceful degradation — camera is optional, always

Jor must be fully usable with **no camera at all** (broken, unplugged, or muted): voice,
face, canvas, skills, and memory all work; only the *seeing* features shed. Rules:

- Perception features are **additive**, never load-bearing: emotion reading off → no
  flow-breaks from visual signals (verbal cues still work — Jor can still *ask*);
  pose correction off → the Yoga skill switches to describe-and-self-report ("hold the
  pose — how does your lower back feel?") instead of refusing to run.
- The perception service reports capability (`camera: none | face | full-body`) and
  skills adapt via their config rather than erroring.
- Same principle covers privacy modes: "camera off" the setting and "camera broken" the
  hardware are the same code path.

## Pipelines

### Hearing
webcam/mic → VAD → wake word (if voice-activated) → STT → brain.
Candidates: Silero VAD, openWakeWord, faster-whisper (local) or cloud STT (low-end tier).

### Emotion reading (research needed — Q19)
face detection → landmarks/action units → derived state (confused, engaged, tired,
stressed) → brain as *signals*, not video.
Candidates: MediaPipe Face Landmarker, OpenFace, py-feat.

**Design stance: the attentive teacher.** The purpose of emotion reading is to let Jor
**break the flow** at the right moment — with a *question* or with *encouragement* —
exactly as a great human teacher does. Not silent adaptation, but visible attention:

1. During teaching, Kal looks confused → Jor stops and *asks* ("You look unsure — should
   I take that again, slower?").
2. Kal pushes through something hard → Jor *encourages* ("That was the tricky part — you
   got it.").
3. During the Monk session, sustained stress signs → Jor breaks in and offers a
   breathing exercise.
4. During finance review, Kal disengages → Jor names it, shortens the session, books a
   follow-up.

Being *seen* is the product: for humans, attention is stickiness — a teacher who notices
you is one you come back to — and the [face](face.md) anthropomorphizes Jor to compound
that stickiness. Emotion recognition from faces is noisy and culturally variable, which
is exactly why the flow-break is a question or encouragement, never a silent inference
acted on as fact.

**Open research:** intervention thresholds and cadence — how confident and how sustained
a signal must be before breaking flow, and the maximum interruption rate before
attentive flips to annoying (likely per-skill: Monk gentle/rare, Yoga frequent/brief).

### Yoga pose correction
camera → 2D/3D keypoints → pose classification (which of the 10) → form scoring against
reference → correction phrased by the brain, shown on canvas.
Candidates: MediaPipe Pose / BlazePose, MoveNet, RTMPose. Classification + scoring layer
on top is **ours to build** (small, tractable — keypoint geometry rules per pose).

The 10 poses (proposal, to confirm): Mountain, Downward Dog, Warrior I, Warrior II,
Tree, Chair, Cobra, Child's Pose, Plank, Triangle.

## Open questions

- Which emotion-signal vocabulary does the brain consume? (Define a small enum, resist
  pseudo-precision like "73% angry".)
- Camera placement/FOV needed to see both a face at desk distance and a full body on a
  yoga mat — one camera or a repositioning step ("move me so I can see your mat")?
- Latency budget for pose feedback: corrections useful within ~1–2 s of a held pose.
- Consent UX: how Jor shows he is watching (face cue + LED on hardware).
