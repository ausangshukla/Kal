# Canvas — where Jor teaches

Jor talks; the canvas shows. It's the whiteboard/projector for whatever Jor is teaching:
meditation guides, the monthly finance review, yoga reference poses with live overlay,
plus system surfaces like the memory editor and skill switcher.

## Locked decisions

- **Runs on the same PC/laptop as the brain.** (Any-screen-on-the-network can come later.)
- **V1 is minimal and one-directional** — Jor pushes content; Kal mostly watches —
  **with a designed path to dual interaction** (Kal typing/drawing/annotating and Jor
  seeing it) in V2.
- **V1 implementation: the Hermes Desktop preview pane.** The desktop app renders web
  pages, files, and tool output side-by-side with the conversation — skills push themed
  HTML/markdown into it. Build only the panels Hermes lacks. (See
  [simulator.md](simulator.md) for the spike on programmatic pane control.)

## What the canvas must show in V1

1. **Persona banner** — who Jor is right now (skill name, theme color). This is the
   explicit half of persona signaling; the face does the subtle half.
2. **Teaching content** — skill-provided: slides/markdown, images, timers (Monk),
   tables/charts (Advisor), reference pose + live skeleton overlay (Yoga).
3. **Memory view** — browse/edit what Jor remembers ([memory.md](memory.md)).
4. **Skill switcher & settings** — install/activate skills, activation mode, privacy and
   placement overrides.

## Path to dual interaction (V2)

Candidate glue: embed tldraw or Excalidraw as a shared surface both Jor and Kal can
draw on. Design the V1 canvas protocol (brain → canvas events) so a reverse channel
(canvas → brain) slots in without a rewrite.

## Open questions

- How much can Hermes's UI be skinned/extended before a thin custom web app is cheaper?
  (Spike early — first technical task after the simulator skeleton.)
- Does the yoga skill need the canvas full-screen across the room (readability from a
  yoga mat: big text, high contrast)?
