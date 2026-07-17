# 06 — Installer + desktop launcher

**What to build:** The parent runs one script on Lily Jane's Edubuntu machine and the game is installed: copied into a folder under her home directory, Pygame made sure to be present, and a colourful double-click icon named "Lily Jane's Snake" placed on the desktop and in the Applications menu. She double-clicks the icon and the full-screen game she plays opens. The parent only touches the terminal once.

**Blocked by:** 04

**Status:** ready-for-agent

- [x] `install.sh` copies the game into a folder under the user's home (e.g. `~/Jeux/…`).
- [x] The installer ensures Pygame is available on the target machine (via `apt` `python3-pygame` or `pip`), so the game runs even if Edubuntu didn't have it.
- [x] The installer places a `.desktop` launcher with a code-supplied icon on the desktop and in the Applications menu, named "Lily Jane's Snake".
- [x] Double-clicking the icon launches the game in the mode she plays (full-screen welcome flow).
- [x] The parent runs the installer once from the terminal; no further terminal use is needed to play.
