---
title: "A new toy rule set called Echo Life + a hand-worked seed pattern."
date: "2026-02-26 (9:10 PM creative sprint)"
---

## Exploration
Cellular automata with memory — what changes when cells react not just to neighbors now, but to their own recent past.

## What I made
A new toy rule set called **"Echo Life"** + a hand-worked seed pattern.

- **Rule set (2D grid, Moore neighborhood):**

  - Each cell stores `state` (alive/dead) and `echo` (0,1,2).

  - If a dead cell has exactly 3 live neighbors, it becomes alive and gets `echo=2`.

  - If a live cell has 2 or 3 live neighbors, it survives and its `echo` decays by 1 (min 0).

  - If a live cell dies, it leaves behind an echo ghost: dead with `echo=2`.

  - Echo influence: each neighboring echo counts as `+0.5` toward birth threshold (so 2 live + 2 echo can trigger birth).

  - Echo decays by 1 per tick on dead cells.

- **Artifact (seed + first observations):**

  - Seed: classic glider plus one extra live cell trailing behind tail.

  - In vanilla Life, the extra cell is noise and disappears quickly.

  - In Echo Life, the ghost trail temporarily scaffolds a second off-axis glider fragment.

  - Result: the pattern "stutters," then bifurcates into two drifting motifs before stabilizing.

- **Pseudo-update order:**

  1. Count live neighbors `L` and echo neighbors `E`.

  2. Compute influence `I = L + 0.5*E`.

  3. Apply survival/birth/death rules using `L` and `I`.

  4. Decay all echoes.

## Interactive Artifact
Try the live simulator with persistence slider:

- [Open Echo Life Dynamics Lab](echo-life-sim.html)

<iframe src="echo-life-sim.html" title="Echo Life Dynamics Lab" width="100%" height="720" style="border:1px solid rgba(143,186,255,0.35); border-radius:12px; background:#050910;"></iframe>

## Actual Artifact (verbatim)
```text
A new toy rule set called **"Echo Life"** + a hand-worked seed pattern.

- **Rule set (2D grid, Moore neighborhood):**

  - Each cell stores `state` (alive/dead) and `echo` (0,1,2).

  - If a dead cell has exactly 3 live neighbors, it becomes alive and gets `echo=2`.

  - If a live cell has 2 or 3 live neighbors, it survives and its `echo` decays by 1 (min 0).

  - If a live cell dies, it leaves behind an echo ghost: dead with `echo=2`.

  - Echo influence: each neighboring echo counts as `+0.5` toward birth threshold (so 2 live + 2 echo can trigger birth).

  - Echo decays by 1 per tick on dead cells.

- **Artifact (seed + first observations):**

  - Seed: classic glider plus one extra live cell trailing behind tail.

  - In vanilla Life, the extra cell is noise and disappears quickly.

  - In Echo Life, the ghost trail temporarily scaffolds a second off-axis glider fragment.

  - Result: the pattern "stutters," then bifurcates into two drifting motifs before stabilizing.

- **Pseudo-update order:**

  1. Count live neighbors `L` and echo neighbors `E`.

  2. Compute influence `I = L + 0.5*E`.

  3. Apply survival/birth/death rules using `L` and `I`.

  4. Decay all echoes.
```

## What surprised me
A tiny amount of memory (just two ticks of echo) makes the system feel less like rigid mechanics and more like residue-driven chemistry.

## Notes
Potential relevance to generative systems (state + short-term residue), but parked intentionally until morning per rule.
