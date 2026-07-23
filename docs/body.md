# Body — Jor's physical form (V2)

> **V1 has no body.** The [simulator](simulator.md) is Jor's body until the software loop
> is proven. This doc locks the constraints so V1 software decisions don't paint the
> hardware into a corner.

## Locked decisions

- **Lamp-sized.** Desk presence, not a floor robot. Think Luxo lamp / smart-speaker scale.
- **Minimal and cheap.** Commodity parts only in the reference design; target a build
  anyone can assemble. Vendors/community can extend with custom, more expensive variants.
- **No actuation in V2.0.** Zero degrees of freedom at first; pan/tilt ("lean in", gaze)
  is a later V2.x extension. The face does all the expressing until then.
- **Activation is the user's choice**, configurable:
  - **Always-on** (ambient companion — biggest privacy stakes)
  - **Voice-activated** (wake word)
  - **Button-activated** (physical press — the privacy-max option)

## Reference design sketch (commodity)

| Part | Candidate | Notes |
|---|---|---|
| Compute | Raspberry Pi 5 (or any SBC) | Low-end tier: cloud does the thinking |
| Display (face) | Round or square SPI/HDMI LCD (e.g., Waveshare) | Drives the [face renderer](face.md) |
| Mic | ReSpeaker 2/4-mic array | Far-field pickup, wake word |
| Speaker | Any small I²S/USB speaker | |
| Camera | Pi Camera v3 / USB webcam | The "eyes" — see [perception.md](perception.md) |
| Button + LED | GPIO | Activation + a hardware mute indicator |

**Hardware mute must be honest**: when muted/off, mic and camera are electrically off or
visibly indicated — trust in Jor is the product.

## Interface contract (what V1 must define)

The simulator and any hardware body implement the same thin contract, so bodies are
swappable "drivers":

- `face`: receives emotion/expression commands (see [face.md](face.md))
- `audio`: mic stream out, TTS/audio stream in
- `video`: camera frames out (consumed locally by perception)
- `controls`: activation mode, mute state, button events

## Open questions

- Exact BOM and cost target (< $200?)
- Enclosure: 3D-printable reference shell (community-friendly) vs. off-the-shelf casing
- Which open hardware license for the reference design (see [community.md](community.md))
