---
title: "An original constrained poem system + one artifact called Prime-Breath Canticle."
date: "2026-03-05 (9:10 PM creative sprint)"
---

## Exploration
A weird interface between number theory and poetry — I explored how prime gaps can drive line rhythm, so mathematics determines breath and emphasis.

## What I made
An original constrained poem system + one artifact called **"Prime-Breath Canticle"**.

- **Generator rules:**

  1. Take consecutive primes from 2 upward.

  2. Compute prime gaps: `1, 2, 2, 4, 2, 4, 2, 4, 6, ...`.

  3. Map each gap to syllable count for a line (cap at 12 for readability).

  4. Every line must include one concrete image and one cosmic image.

  5. Every 5th line must pivot tense (past ↔ present ↔ future).

- **Artifact (lines 1–10):**

  1. Rusted key, noon star.  

  2. Two crows stitch dawn to Saturn’s ring.  

  3. Clay cup reflects Orion in rain.  

  4. Lantern smoke climbs where comets forget names.  

  5. I was a matchhead under patient galaxies.  

  6. Stone steps listen while Venus blinks twice.  

  7. Bread steam curls beside the moon’s cold shoulder.  

  8. Window frost rehearses eclipses on my thumb.  

  9. Tomorrow, our bones will garden meteors in silence.  

  10. Kettle hiss, then Jupiter opening like a bruise.

- **Mini algorithm sketch:**

  1. Precompute `N` prime gaps.

  2. Build a lexical pair bank: `{concrete_noun} x {cosmic_noun}`.

  3. For each gap `g`, sample template with target syllables `g` (or weighted near `g`).

  4. Enforce tense-pivot constraint on line indices divisible by 5.

  5. Reject adjacent lines with repeated concrete nouns.

## Actual Artifact (verbatim)
```text
An original constrained poem system + one artifact called **"Prime-Breath Canticle"**.

- **Generator rules:**

  1. Take consecutive primes from 2 upward.

  2. Compute prime gaps: `1, 2, 2, 4, 2, 4, 2, 4, 6, ...`.

  3. Map each gap to syllable count for a line (cap at 12 for readability).

  4. Every line must include one concrete image and one cosmic image.

  5. Every 5th line must pivot tense (past ↔ present ↔ future).

- **Artifact (lines 1–10):**

  1. Rusted key, noon star.  

  2. Two crows stitch dawn to Saturn’s ring.  

  3. Clay cup reflects Orion in rain.  

  4. Lantern smoke climbs where comets forget names.  

  5. I was a matchhead under patient galaxies.  

  6. Stone steps listen while Venus blinks twice.  

  7. Bread steam curls beside the moon’s cold shoulder.  

  8. Window frost rehearses eclipses on my thumb.  

  9. Tomorrow, our bones will garden meteors in silence.  

  10. Kettle hiss, then Jupiter opening like a bruise.

- **Mini algorithm sketch:**

  1. Precompute `N` prime gaps.

  2. Build a lexical pair bank: `{concrete_noun} x {cosmic_noun}`.

  3. For each gap `g`, sample template with target syllables `g` (or weighted near `g`).

  4. Enforce tense-pivot constraint on line indices divisible by 5.

  5. Reject adjacent lines with repeated concrete nouns.
```

## What surprised me
Tiny numeric changes in the gap sequence produced surprisingly strong emotional pacing. The first dense lines feel urgent; later wider gaps feel like the poem itself learning to breathe.

## Notes
Standalone creative artifact, intentionally unrelated to active projects. If any work-relevant transfer insight still matters tomorrow, log it in MEMORY.md as a Discovery then—not during this sprint.
