# Community — building Jor like Linux

The ambition: Jor is developed in the open, Linux-style — a small trusted kernel, an
ecosystem where anyone can extend, and maximum adoption.

## Locked decisions

- **Maximum adoption: anything by anyone.** Permissive licensing — recommend
  **Apache-2.0** for code (patent grant matters for a hardware-adjacent project; MIT as
  the simpler alternative). Hardware reference designs under **CERN-OHL-P** (permissive)
  or CC-BY. Skills may be **FOSS or commercial** — the skill API is the boundary, not
  the license.
- **Kernel + extensions model:**
  - **Kernel** (few trusted maintainers, founder as BDFL initially): agent runtime glue,
    skill API/format, memory system, face/expression protocol, body interface contract,
    placement policy engine, safety framework.
  - **Userspace** (anyone, no permission needed): skills, face/emotion packs, hardware
    variants, canvas themes, perception improvements, language packs.
- **The simulator is the contributor on-ramp** — no hardware required, ever, to
  contribute ([simulator.md](simulator.md)).
- **Safety-first curation** for skills touching mental health, money, or the body: a
  small *curated* set ships with Jor; the open registry question stays open until
  there's a trust mechanism ([skills.md](skills.md)).

## Naming

"Jor" and "Kal" (Superman's father Jor-El and Kal-El, with "-El" dropped) are **internal
codenames for now**. Assessment:

- *Jor-El* and *Kal-El* are DC Comics characters; the names function as trademarks in
  entertainment. Using full names publicly invites a cease-and-desist.
- Truncated *Jor* / *Kal* are less exposed — short common syllables, and trademark
  claims need likelihood of confusion within a product category — but a project that
  *markets itself on the Superman story* ("become Superman", "Jor teaches Kal") builds
  the association deliberately, which is exactly what strengthens a confusion claim.
- **Action before going public**: pick a clean public name (keep Jor/Kal internally),
  run a trademark search on it, and drop Superman references from public materials.
  Track as a pre-launch checklist item.

## Contributor experience (V1 must-haves)

1. `git init` + push to a public repo when founder is ready; these docs are the seed.
2. One-command simulator start; a "write your first skill in 15 minutes" tutorial.
3. Skill template repo + `safety.md` requirements.
4. CONTRIBUTING.md defining kernel vs userspace and how patches reach the kernel.
5. CI on the simulator (scripted sessions as integration tests).

## Open questions

- Governance formalization trigger: at what contributor count does BDFL + trusted
  maintainers need written process (an RFC system like Rust's, or Linux-style
  subsystem maintainers)?
- Where does the community live (GitHub Discussions / Discord / Zulip)?
- Trademark/entity: register the eventual public name? A foundation someday?
