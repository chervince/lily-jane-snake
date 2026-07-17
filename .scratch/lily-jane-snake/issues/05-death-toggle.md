# 05 — Death toggle (`mort_activee`)

**What to build:** A single config switch turns the game from the gentle no-fail sandbox into classic Snake, so it can grow into a real challenge as Lily Jane gets older — without a rewrite. When `mort_activee=True`, the snake dies on the classic fatal conditions (hitting an edge and/or crossing its own body), and the shell shows a simple game-over with an easy restart. The default stays off (no death).

**Blocked by:** 02

**Status:** ready-for-agent

- [x] The game core implements the fatal rules behind the `death_enabled` flag: with `death_enabled=True`, the snake entering its own body ends the run, and crossing an edge ends the run (instead of wrapping).
- [x] With `death_enabled=False` (default) behaviour is unchanged from ticket 01 — wrap-around, no self-death.
- [x] `config.py`'s `mort_activee` drives this flag; default remains `False`.
- [x] The shell handles the end-of-run state with a simple game-over and an easy restart (no punishing/guilt-inducing screen).
- [x] pytest tests cover both branches: with death off, edge-crossing wraps and self-overlap is harmless; with death on, edge-crossing and self-collision each end the run. The toggle is exercised by the rules, not merely declared.
