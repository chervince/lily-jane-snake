# Spec: Lily Jane's Snake

Status: ready-for-agent

A gentle, no-fail Snake game for a 5-year-old (Lily Jane), built to be installed on her Edubuntu machine and launched from a desktop icon.

## Problem Statement

A parent wants to give his 5-year-old daughter, Lily Jane, a game she can play by herself on her Edubuntu PC. The classic Snake game is unsuitable for her age: it is too fast, it punishes small mistakes with an abrupt "game over", it requires reading, and it has no easy way for a young child to start it. He needs a version that a 5-year-old can open on her own, understand without reading, and enjoy without ever being made to feel like she failed.

## Solution

A custom desktop Snake game, "Lily Jane's Snake", written in Python + Pygame and installable on Edubuntu via a one-time `install.sh` script that places a colourful double-click icon on her desktop. The game is deliberately forgiving and cute:

- The snake never dies — walls wrap around, and the snake may cross itself with no penalty.
- It moves slowly and at a constant speed, so she can see every turn coming.
- She steers with the four arrow keys only.
- Eating a fruit is pure reward: the snake grows, a happy sound plays, and a fruit counter ticks up.
- Big rounded, brightly-coloured graphics with a two-eyed smiling snake; her name greets her on a welcome screen.
- It runs full-screen so she cannot accidentally get lost in window controls.

The whole experience is tuned by a small `config.py` so the parent can adjust speed, mute sound, switch to windowed mode for development, and — later, as she grows — turn the classic "you can die" rules back on.

## User Stories

1. As Lily Jane, I want to open the game by double-clicking a colourful icon on my desktop, so that I can start playing without help.
2. As Lily Jane, I want to see my name "Lily Jane" and a smiling snake on the opening screen, so that I know this game is mine.
3. As Lily Jane, I want to start playing by pressing any arrow key, so that I don't have to read instructions or click a button.
4. As Lily Jane, I want to steer the snake with the up, down, left and right arrows, so that the controls match what I already recognise.
5. As Lily Jane, I want the snake to move slowly, so that I have time to decide where to turn.
6. As Lily Jane, I want the snake to keep moving at the same speed the whole time, so that the game never suddenly gets too hard.
7. As Lily Jane, I want the snake to reappear on the opposite side when it goes off an edge, so that I never lose by bumping into a wall.
8. As Lily Jane, I want nothing bad to happen when the snake crosses its own body, so that I am never punished for a mistake.
9. As Lily Jane, I want the snake to grow longer each time it eats a fruit, so that I can see that I did something good.
10. As Lily Jane, I want a happy sound to play when the snake eats a fruit, so that eating feels rewarding.
11. As Lily Jane, I want to see a counter with a fruit picture and a number that goes up, so that I can watch my progress and practise counting.
12. As Lily Jane, I want a new fruit to appear somewhere else each time I eat one, so that there is always a next goal.
13. As Lily Jane, I want the snake to look cute with two eyes and bright colours, so that it feels alive and friendly.
14. As Lily Jane, I want the fruit to look like a real apple, so that I recognise what to go for.
15. As Lily Jane, I want the game to fill the whole screen with big shapes, so that everything is easy to see.
16. As Lily Jane, I want the game to keep going forever, so that I can play as long as I like without a "game over".
17. As Lily Jane, I want to be able to turn the snake in any direction, so that I am never blocked or told my button press was wrong.
18. As the parent, I want to install the game with a single `install.sh` run, so that setup on her machine is quick and I only touch the terminal once.
19. As the parent, I want the installer to make sure Pygame is present, so that the game works even if her Edubuntu doesn't have it yet.
20. As the parent, I want the installer to place a desktop icon and an Applications-menu entry named "Lily Jane's Snake", so that she can find and launch it easily.
21. As the parent, I want a quit key (Escape) that she is unlikely to press by accident, so that I can close the game but she won't stumble out of it.
22. As the parent, I want the game to run full-screen for her but be switchable to a window, so that I can test it comfortably during development.
23. As the parent, I want the game speed to live in a config file, so that I can slow it down or speed it up as I watch her play and as she grows.
24. As the parent, I want a single config switch to mute the sound, so that she can play quietly when someone nearby is working.
25. As the parent, I want a single config switch that re-enables dying (hitting walls / self), so that the game can grow into a real challenge for her later without a rewrite.
26. As the parent, I want the on-screen text in English, so that the game doubles as light English exposure for her.
27. As the parent, I want the game logic to be cleanly separated from Pygame, so that the rules are covered by automated tests and I can trust changes I make later.

## Implementation Decisions

**Technology**
- Python 3 + Pygame. Python 3 is preinstalled on Edubuntu; Pygame is installed by the installer if missing (via `apt` `python3-pygame` or `pip`, at the implementer's discretion).

**Architecture — one seam**
- A **pure game-core module** holds all game rules and is completely free of Pygame, rendering, sound, timing, and OS concerns.
- The game core exposes an immutable state and a single **`step(state, input)`** transition function. `input` is one of:
  - a **tick** — advance the snake one cell in its current direction;
  - a **turn** — set a new direction (any direction is accepted, including a 180° reversal, which folds the snake harmlessly).
- State carried by the core: the snake's body as an ordered list of grid cells, current direction, the fruit's cell, the fruit counter, the grid dimensions, and the `death_enabled` flag.
- **Fruit placement takes an injected random source** (an RNG or placement callback) rather than calling a global random function, so the behaviour is deterministic under test. A newly spawned fruit must never land on a cell occupied by the snake.
- A thin **Pygame shell** wraps the core and is responsible only for: initialising Pygame, full-screen vs windowed display, mapping arrow-key events to `turn` inputs and Escape to quit, driving `tick` inputs at the configured cadence (this is where `vitesse` lives), drawing the welcome screen and gameplay, and generating/playing sound. The shell holds no game rules.

**Game rules (all in the core)**
- The snake moves exactly one cell per tick.
- Edges wrap: leaving one side re-enters the opposite side.
- Eating a fruit (head enters the fruit's cell) grows the snake by one segment, increments the fruit counter, and spawns a new fruit off the snake.
- With `death_enabled = False` (the default), the snake entering its own body or an edge is never fatal. With `death_enabled = True`, the classic fatal rules apply (edge and/or self-collision end the run) — this toggle must be exercised by the rules, not just declared.

**Configuration — `config.py`, four knobs**
- `mort_activee` (death enabled) — default `False`.
- `vitesse` (speed, cells per second, constant) — a slow default around 4–5.
- `son_active` (sound on) — default `True`.
- `plein_ecran` (full-screen) — default `True`; set `False` for windowed development.

**Presentation & content**
- Grid roughly 15×12 large cells (few, big cells for visibility), scaled to fill the screen.
- Graphics are **drawn by code** (rounded shapes, bright colours, a two-eyed smiling snake head, an apple-like fruit) — no external image assets in V1.
- Title / window caption / launcher name: **"Lily Jane's Snake"**. Welcome screen shows the title, a smiling snake, the name "Lily Jane", and "Press an arrow to play". All on-screen text is in **English**.
- Two **code-generated** sound effects (a fruit-eaten "munch/ding" and a start sound), synthesised at build time with the Python standard library (`wave` + `math`) so there are no extra runtime dependencies and no audio-file licensing concerns. Both honour `son_active`.

**Distribution**
- `install.sh`: copies the game into a folder under the user's home (e.g. `~/Jeux/…`), ensures Pygame is available, and installs a `.desktop` launcher (with a code-supplied icon) onto the desktop and into the Applications menu. The parent runs it once.

## Testing Decisions

- **What makes a good test here:** it exercises only the game core's *external behaviour* through `step(state, input)` — given a state and an input, assert the next state. Tests must not reach into rendering, timing, Pygame, or sound, and must not assert on private/implementation details.
- **Framework:** pytest, tests in `tests/`. There is no prior art in this (previously empty) repo, so pytest is established here as the convention for the game core.
- **Module under test:** the pure game core only. The Pygame shell is intentionally not unit-tested; it is verified by playing the game.
- **Behaviours to cover through the single seam:**
  - one tick moves the head one cell in the current direction, and the body follows;
  - a `turn` input changes direction; a 180° reversal is accepted and does not end the game;
  - wrap-around at each of the four edges;
  - with `death_enabled=False`: the head entering its own body does **not** end the game, and crossing an edge does **not** end the game;
  - with `death_enabled=True`: the corresponding fatal condition **does** end the game (guards the future toggle);
  - eating a fruit grows the snake by exactly one, increments the counter, and spawns a new fruit that is never on the snake (using the injected RNG for determinism);
  - the fruit counter reflects the number of fruits eaten.
- Determinism is achieved by injecting the random source for fruit placement, so no test depends on real randomness.

## Out of Scope

- Real illustration assets (PNG art) for the snake, fruit, and background — V1 draws everything in code.
- Real/downloaded audio files and background music — V1 synthesises two simple effects in code.
- A tuned "death"/difficulty experience — the `mort_activee` toggle and its rules exist and are tested, but designing and balancing the fatal mode is deferred.
- Speed ramping / levels, multiple fruit types, obstacles, power-ups.
- High scores, persistence, or save files.
- Mouse/touch/gamepad controls, WASD, or any control scheme beyond the four arrow keys.
- Packaging as a single self-contained executable (e.g. PyInstaller); V1 relies on Python + Pygame on the target machine.
- Multi-language UI; V1 is English-only (with the fixed name "Lily Jane").

## Further Notes

- The four config knobs are intentionally named in French to match the parent's working language, while the player-facing UI text is English — this split is deliberate.
- Keeping every rule in the pure core is what makes the "grow into a real challenge later" path cheap: enabling death, changing speed, or adding scoring should mostly be core-level changes with matching tests, not a shell rewrite.
- The wrap-around and no-self-death defaults mean an arbitrarily long snake is always valid; the core must not assume the snake fits without overlap.
- Target platform is Edubuntu (Ubuntu-based, GNOME, X11/Wayland); full-screen via Pygame should adapt to the child's screen resolution automatically, so no fixed resolution is baked in.
