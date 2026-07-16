"""Generate the desktop launcher icon (a smiling snake head) as a PNG.

Usage:  python3 icon.py [output.png]

Run by ``install.sh`` at install time. It draws the icon in code (reusing the
game's own graphics) and needs no display -- the SDL "dummy" drivers below let
pygame run headless, so this works even over SSH or during an unattended
install.
"""

from __future__ import annotations

import os
import sys

# Must be set before pygame imports/initialises SDL.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402  (import after setting SDL env)

import graphics  # noqa: E402


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "icon.png"
    pygame.init()
    try:
        pygame.image.save(graphics.render_snake_icon(256), out)
    finally:
        pygame.quit()
    print(f"Wrote icon to {out}")


if __name__ == "__main__":
    main()
