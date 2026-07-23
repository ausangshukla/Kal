# OSS Map — glue the best, build only what's missing

The prime directive: **reuse the best open source available; build only the missing
pieces.** This ledger is the running answer to "are we reinventing something?" — every
subsystem lists what we glue and what we own. Candidates need spikes before commitment.

## Reuse (glue)

| Subsystem | Candidates | Notes |
|---|---|---|
| Agent runtime, skills, memory, tools | **[Hermes Agent](https://github.com/nousresearch/hermes-agent)** | The V1 backbone. Markdown skills, persistent memory, 70+ tools, subagents; Anthropic/OpenRouter/local backends |
| Cloud reasoning | Anthropic API (Opus/Fable) | Teaching, planning, personas |
| Local LLM serving | Ollama, vLLM | High-end tier / fully-local modes |
| STT | faster-whisper (local), cloud STT (low-end tier) | |
| VAD / wake word | Silero VAD, openWakeWord | Wake word needed for voice-activation mode |
| TTS | Piper (fast, local), Kokoro; cloud TTS fallback | Persona voices per skill |
| Face/emotion signals | MediaPipe Face Landmarker, OpenFace, py-feat | Research spike — see [perception.md](perception.md) |
| Pose estimation | MediaPipe Pose/BlazePose, MoveNet, RTMPose | Keypoints for yoga skill |
| Simulator shell & voice UI | **Hermes Desktop** (`apps/desktop`) | Voice I/O, preview pane, file browser, settings, NL cron — shares core/sessions/skills/memory with CLI & gateway |
| Canvas V1 | Hermes Desktop preview pane | Spike programmatic pane control |
| Canvas V2 shared surface | tldraw, Excalidraw | Dual interaction later |
| Memory enhancements | Letta (MemGPT), Mem0, Zep/Graphiti | Research — only if they beat Hermes native + retrieval |
| Hardware (V2) | Raspberry Pi, ReSpeaker, Waveshare displays | Commodity reference BOM |

## Build (ours — because nothing good exists)

1. **The face renderer + expression protocol** — abstract expressive eyes with emotion
   packs. Almost no reusable OSS here (RoboEyes-class projects are far too low-fi).
   Likely our most-adopted standalone component.
2. **The perception→signals layer** — turning landmarks/keypoints into a small, honest
   vocabulary of signals ("seems confused", "left arm low") consumed by the brain.
3. **Yoga pose classification + form scoring** — geometry rules over keypoints for the
   10 poses, plus correction phrasing hooks.
4. **Placement policy engine** — skill config + global overrides → local/cloud routing
   per function. The Linux-portability story lives here.
5. **Skill format extensions** — `config.yaml`, `safety.md`, canvas assets, face packs on
   top of Hermes skills ([skills.md](skills.md)). Upstream what Hermes will take.
6. **Session/persona manager** — one-skill-at-a-time switching of persona, canvas theme,
   memory namespace.
7. **The simulator glue** — much smaller than first thought: Hermes Desktop provides the
   shell, voice loop, and canvas pane; we add the face window + perception service and
   the one-command start ([simulator.md](simulator.md)).
8. **The three launch skills** — Monk, Financial Advisor, Yoga Teacher.

## Rules of engagement

- Before building anything, a search + spike proves nothing glueable exists.
- Prefer extending upstream (especially Hermes) over forking; carry patches upstream.
- Every glued component sits behind a thin interface of ours, so a better replacement
  can be swapped in later (same reason Talus stays possible — see [brain.md](brain.md)).
