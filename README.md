# Lily Jane's Snake

Lily Jane's Snake is a gentle, no-fail Snake game for a 5-year-old, written in
Python and Pygame. By default the snake never dies: it moves slowly at a
constant speed, wraps around the screen edges, and passes harmlessly through
itself. Every fruit is pure reward — the snake grows, a happy sound plays, and
an on-screen counter ticks up. The game runs full-screen and launches from a
double-click desktop icon, so a young child can play on her own without
reading.

It's built for an Edubuntu machine but runs on any desktop Linux with Python 3
and Pygame.

## Features

The game is deliberately forgiving and cute:

- **No failure by default.** The snake wraps around walls and crosses itself
  with no penalty, so a mistake never ends the game.
- **Slow, constant speed.** There's time to see every turn coming, and the
  game never speeds up.
- **Four arrow keys only.** Any direction is accepted, including a reversal, so
  a button press is never "wrong."
- **Fruit, growth, and a counter.** Eating an apple grows the snake, plays a
  sound, and raises an on-screen count for early counting practice.
- **Cute, code-drawn graphics.** A two-eyed smiling snake and an apple, drawn
  entirely in code with no image files.
- **English on-screen text.** The welcome screen greets "Lily Jane" and doubles
  as light English exposure.
- **A parent-tunable config.** Four settings control speed, sound, full-screen,
  and a future "you can die" mode.

## Requirements

The game runs on any desktop Linux that has these:

- Python 3.10 or later (preinstalled on Edubuntu).
- Pygame (the installer adds it for you if it's missing).

## Installing the game

The installer copies the game into your home folder and puts a double-click
icon on the desktop and in the Applications menu. You run it once from a
terminal.

1. Get the game onto the machine by cloning the repository:

   ```bash
   git clone https://github.com/chervince/lily-jane-snake.git
   cd lily-jane-snake
   ```

   You can also copy the project folder across on a USB stick and open a
   terminal in it.

2. Run the installer:

   ```bash
   ./install.sh
   ```

   The first run installs Pygame if it's missing (it may ask for your password
   once), draws the launcher icon, and writes the desktop launcher.

3. Double-click the **Lily Jane's Snake** icon to play.

After this, no terminal is needed to play.

## Updating the game

Re-running the installer is how you ship a new version. It refreshes the game
code but keeps your `config.py`, so any speed or sound settings you've tuned on
the machine are never lost.

<!-- prettier-ignore -->
> [!IMPORTANT]
> An update never overwrites an existing `config.py`. Your per-child settings
> (speed, sound, death mode) are preserved across updates.

To update a machine that already has the game installed:

1. Get the new version. If you cloned with Git, pull the latest code:

   ```bash
   cd lily-jane-snake
   git pull
   ```

   If you install from a USB stick, copy the new project folder across instead.

2. Re-run the installer from the project folder:

   ```bash
   ./install.sh
   ```

   The code files are refreshed, and the installer prints "Keeping your
   existing config.py" to confirm your settings are untouched.

3. If the game is open, press **Escape** and reopen it to load the new version.

### Resetting the settings to the defaults

To discard your local settings and return to the shipped defaults, delete the
installed config and re-run the installer:

```bash
rm ~/Jeux/lily-jane-snake/config.py
./install.sh
```

### Older config files keep working

If a new version adds a setting that your preserved `config.py` doesn't have,
the game falls back to that setting's default instead of failing. Add the new
line to your `config.py` whenever you want to change it.

## Configuration

The four settings live in `config.py`. They're named in French to match the
parent's working language, while the on-screen game text stays English. Edit
the file and relaunch the game to apply a change.

| Setting | What it does | Default |
| --- | --- | --- |
| `mort_activee` | Turns on classic "you can die" rules: hitting a wall or yourself ends the run. Leave it off for the gentle game. | `False` |
| `vitesse` | Speed in grid cells per second, constant for the whole game. | `4.0` |
| `son_active` | Turns the sound effects on or off. | `True` |
| `plein_ecran` | Runs full-screen (`True`) or in a window (`False`, handy for development). | `True` |

Once the game is installed, the file to edit is
`~/Jeux/lily-jane-snake/config.py`.

## Playing

The welcome screen shows the title, a smiling snake, and the name "Lily Jane."

1. Press any **arrow key** to start.
2. Steer with the **up**, **down**, **left**, and **right** arrows.
3. Guide the snake onto the apples to grow it and raise the counter.
4. Press **Escape** to quit.

With `mort_activee` turned on, a gentle "Let's try again!" screen appears when
the run ends; press an arrow to play again.

## Development

The game logic is a pure module, `snake_core.py`, with no Pygame, timing, or
sound. A thin Pygame shell (`main.py`, `graphics.py`, `sound_fx.py`) wraps it.
The core carries all the rules, which keeps them testable and makes future
changes — like tuning the death mode — core-level edits rather than a rewrite.

Set up a virtual environment and install the tools:

```bash
python3 -m venv .venv
.venv/bin/pip install pytest mypy pygame
```

Run the test suite (20 tests that drive the core through its single
`step(state, input)` seam):

```bash
.venv/bin/python -m pytest
```

Type-check the core:

```bash
.venv/bin/python -m mypy
```

To play in a window while developing, set `plein_ecran = False` in `config.py`
and run:

```bash
.venv/bin/python main.py
```

### Project structure

The code is split into a pure core and a thin shell around it:

| Path | Purpose |
| --- | --- |
| `snake_core.py` | Pure game rules: the state and the `step(state, input)` transition. No Pygame. |
| `main.py` | The Pygame shell: window, input, timing, and scenes. Holds no rules. |
| `graphics.py` | Code-drawn snake, apple, counter, welcome screen, and icon. |
| `sound_fx.py` | Sound effects synthesized with the Python standard library. |
| `config.py` | The four parent-tunable settings. |
| `icon.py` | Generates the launcher icon, used by the installer. |
| `install.sh` | The one-time installer, which also updates an existing install. |
| `tests/test_core.py` | Tests for the game core. |

The originating spec and tickets live in `.scratch/lily-jane-snake/`.
