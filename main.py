"""The thin Pygame shell for Lily Jane's Snake.

This is the only place pygame, the display, timing, the keyboard and sound
meet. It holds *no game rules*: it maps the four arrow keys to `Turn` inputs
and Escape to quit, drives `Tick` inputs at the configured cadence, reads the
state the core hands back, and draws it. Every rule lives in `snake_core`.

Run it directly for development (`python3 main.py`); on Lily Jane's machine the
desktop launcher runs the same entry point.
"""

from __future__ import annotations

import pygame

import config
import graphics
import snake_core
import sound_fx

TITLE = "Lily Jane's Snake"

# Scenes the shell moves between.
WELCOME = "welcome"
PLAYING = "playing"
GAME_OVER = "game_over"

ARROW_TO_DIRECTION = {
    pygame.K_UP: snake_core.UP,
    pygame.K_DOWN: snake_core.DOWN,
    pygame.K_LEFT: snake_core.LEFT,
    pygame.K_RIGHT: snake_core.RIGHT,
}
ARROW_KEYS = frozenset(ARROW_TO_DIRECTION)

# Fallback for every config knob, so an older or hand-edited config.py that is
# missing a setting still runs (with the default) instead of crashing. These
# mirror the shipped defaults in config.py.
_DEFAULTS = {
    "mort_activee": False,
    "vitesse": 4.0,
    "son_active": True,
    "plein_ecran": True,
}


def _cfg(name: str):
    """Read a config knob, falling back to its default if config.py lacks it."""
    return getattr(config, name, _DEFAULTS[name])


def _make_screen() -> pygame.Surface:
    if _cfg("plein_ecran"):
        # (0, 0) asks pygame for the desktop's own resolution -- no fixed size.
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # A 15:12 window for comfortable development.
    return pygame.display.set_mode((900, 720))


def _fresh_game() -> snake_core.GameState:
    # Board size comes from the core's defaults (its single source of truth).
    return snake_core.new_game(death_enabled=_cfg("mort_activee"))


def run() -> None:
    pygame.init()
    screen = _make_screen()
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(graphics.render_snake_icon(64))
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    fonts = graphics.make_fonts(screen.get_height())
    sounds = sound_fx.Sounds(enabled=_cfg("son_active"))

    sounds.play_start()
    state = _fresh_game()
    scene = WELCOME

    # Constant cadence: `vitesse` cells per second, accumulated across frames so
    # the pace is independent of the frame rate.
    tick_interval = 1.0 / max(_cfg("vitesse"), 0.5)
    since_tick = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in ARROW_KEYS:
                    if scene == PLAYING:
                        state = snake_core.step(
                            state, snake_core.Turn(ARROW_TO_DIRECTION[event.key])
                        )
                    else:
                        # On the welcome or game-over screen, any arrow starts a
                        # fresh game -- the only keys she ever needs.
                        state = _fresh_game()
                        since_tick = 0.0
                        scene = PLAYING

        if scene == PLAYING:
            since_tick += dt
            while since_tick >= tick_interval:
                since_tick -= tick_interval
                before = state.fruits_eaten
                state = snake_core.step(state, snake_core.Tick())
                if state.fruits_eaten > before:
                    sounds.play_munch()
                if state.game_over:
                    scene = GAME_OVER
                    break

        _draw(screen, scene, state, fonts)
        pygame.display.flip()

    pygame.quit()


def _draw(
    screen: pygame.Surface,
    scene: str,
    state: snake_core.GameState,
    fonts: graphics.Fonts,
) -> None:
    if scene == WELCOME:
        graphics.draw_welcome(screen, fonts, pygame.time.get_ticks())
        return

    cell, ox, oy = graphics.board_layout(screen.get_size())
    graphics.draw_board(screen, cell, ox, oy)
    gx, gy = state.fruit
    graphics.draw_apple(screen, ox + (gx + 0.5) * cell, oy + (gy + 0.5) * cell, cell * 0.9)
    graphics.draw_snake(screen, state.snake, cell, ox, oy)
    graphics.draw_counter(screen, state.fruits_eaten, fonts)
    if scene == GAME_OVER:
        graphics.draw_game_over(screen, state.fruits_eaten, fonts)


if __name__ == "__main__":
    run()
