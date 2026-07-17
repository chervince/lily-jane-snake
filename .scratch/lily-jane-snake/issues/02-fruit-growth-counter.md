# 02 — Fruit, growth & counter

**What to build:** An apple appears on the grid. When the snake's head reaches the apple it eats it: the snake grows one segment longer, an on-screen fruit counter ticks up by one, and a fresh apple appears somewhere else that is never on the snake's body. Playing now has a point — drive around, eat apples, watch the snake get longer and the number climb.

**Blocked by:** 01

**Status:** ready-for-agent

- [x] The game core state carries the fruit's cell and a fruit counter.
- [x] Fruit placement uses an injected random source (RNG or placement callback), not a global random call, so tests are deterministic.
- [x] When the head enters the fruit's cell: the snake grows by exactly one segment, the counter increments by one, and a new fruit spawns on a free cell — never on any cell occupied by the snake.
- [x] The Pygame shell draws the fruit as a recognisable apple (not a bare square) and shows the counter on screen as a fruit picture plus a number (e.g. "🍎 7"), big and readable.
- [x] pytest tests cover: eating grows the snake by one, the counter increments, and the respawned fruit is never on the snake — all deterministically via the injected random source.
