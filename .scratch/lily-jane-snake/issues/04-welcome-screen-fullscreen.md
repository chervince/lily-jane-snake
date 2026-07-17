# 04 — Welcome screen + full-screen + English text

**What to build:** When the game opens, Lily Jane sees a welcome screen with the title "Lily Jane's Snake", a smiling snake, her name "Lily Jane", and "Press an arrow to play" — all in English. Pressing any arrow starts the game. The game runs full-screen so she can't fall out into window controls, and the grid scales to fill her screen with big cells. A config switch flips to windowed mode for the parent's development.

**Blocked by:** 01

**Status:** ready-for-agent

- [x] A welcome screen shows: the title "Lily Jane's Snake", a smiling snake, the name "Lily Jane", and "Press an arrow to play". All on-screen text is English.
- [x] Pressing any arrow key on the welcome screen starts play.
- [x] `config.py` gains a `plein_ecran` knob (default `True`); when `True` the game runs full-screen, when `False` it runs in a window (for development).
- [x] In full-screen the grid (~15×12 large cells) scales to fill the screen; no fixed resolution is baked in — it adapts to the display.
- [x] The window/title caption and the on-screen title read "Lily Jane's Snake".
