# Memory — how Jor remembers Kal

A companion who forgets is a gadget. Memory is what makes Jor's relationship with Kal
real across months and years.

## Locked decisions

- **Kal can see and edit Jor's memory of him.** Full transparency — a browsable, editable
  memory view (likely on the canvas). This is both an ethical stance and a
  differentiator vs. cloud assistants.
- **Privacy is configurable**, potentially differently per skill (the Monk's memories may
  be local-only; the Financial Advisor's may sync for continuity).
- **Start from Hermes Agent's memory** (persistent, local, readable markdown at
  `~/.hermes/`) and enhance — don't build a memory engine from scratch.

## What Jor must remember (requirements sketch)

| Kind | Example | Horizon |
|---|---|---|
| Facts about Kal | family, work, preferences, health constraints | Forever, editable |
| Emotional history | "gets frustrated when interrupted mid-flow" | Long, decaying confidence |
| Skill progress | Warrior II improving; hips still misaligned | Per skill, months |
| Commitments | "cut eating-out spend 20% this month" | Until resolved, then archived |
| Session summaries | what was taught, what landed, what confused | Rolling |

Namespacing: a shared "who Kal is" core + per-skill namespaces (set in skill config),
so the yoga teacher doesn't rummage through therapy notes unless Kal allows it.

## Research agenda (open — Q18/Q19)

1. Survey open-source memory systems and what to glue: Hermes native memory, Letta
   (MemGPT), Mem0, Zep/Graphiti — what does each add over plain markdown + retrieval?
2. Decay model: should memories fade (confidence decay, periodic consolidation) or
   persist until edited? What does a *coach* need vs. a *companion*?
3. Emotional memory: what representation is useful without being creepy or wrong?
   (Store observations + Jor's asks, not inferred diagnoses.)
4. Cross-skill leakage rules: when *should* the Financial Advisor know Kal had a rough
   month (Monk data)? Explicit consent flows.
5. Memory review ritual: does Jor periodically show Kal "here's what I've learned about
   you this month — correct me"?
