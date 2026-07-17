# 01 — Walking snake (tracer bullet)

**What to build:** A window opens showing a cute, two-eyed snake sitting on a grid. Pressing the arrow keys steers the snake; it moves one cell at a time, slowly and at a constant speed, and wraps around when it leaves any of the four edges. It never dies. Pressing Escape closes the game. This is the skeleton the rest of the feature hangs on: it stands up the pure game core, the thin Pygame shell, the config file, and the test suite — all end to end, so a person can actually drive a snake around.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [x] A pure game-core module exists with no `import pygame` and no rendering/sound/timing — just an immutable state (snake body cells, direction, grid size, `death_enabled` flag) and a `step(state, input)` transition where `input` is a *tick* (advance one cell) or a *turn* (set direction).
- [x] One tick moves the head one cell in the current direction and the body follows.
- [x] A turn changes direction; a 180° reversal is accepted and folds the snake harmlessly (no crash, no game-over).
- [x] The snake wraps around at each of the four edges (leaves one side, re-enters the opposite side).
- [x] With `death_enabled=False` (default), nothing ever ends the game — including the head crossing its own body.
- [x] A Pygame shell opens a window, draws the grid and a cute snake (rounded bright segments, two eyes on the head), maps the four arrow keys to `turn` inputs, drives `tick` inputs at the configured cadence, and quits on Escape.
- [x] A `config.py` exists with `vitesse` (constant speed, cells/sec, slow default ~4–5) and `mort_activee=False`; changing `vitesse` visibly changes the pace.
- [x] pytest tests in `tests/` cover: movement per tick, turning, 180° reversal being harmless, wrap-around at all four edges, and no-death-on-self behaviour — all against the pure core, with no Pygame.
