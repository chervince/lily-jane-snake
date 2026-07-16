"""All the code-drawn graphics for Lily Jane's Snake.

No game rules live here -- these functions only turn a piece of state (or
nothing at all) into pixels. They are shared by the game shell (`main.py`) and
the installer's icon generator (`icon.py`), which is why the snake face is a
reusable helper.

Everything is drawn from shapes: bright rounded segments, a two-eyed smiling
head, and an apple-like fruit. There are no external image assets.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

# Board size lives in the core (the single source of truth shared by the rules
# and this rendering layer).
from snake_core import GRID_H, GRID_W

# A bright, friendly palette.
BG = (150, 210, 245)          # sky blue
BOARD_A = (200, 233, 170)     # light grassy green
BOARD_B = (185, 224, 152)     # slightly darker green (checkerboard)
SNAKE_BODY = (76, 178, 82)
SNAKE_BODY_EDGE = (56, 142, 60)
SNAKE_HEAD = (104, 202, 108)
EYE_WHITE = (255, 255, 255)
EYE_DARK = (33, 40, 48)
APPLE_RED = (226, 58, 58)
APPLE_HI = (255, 160, 160)
LEAF = (90, 180, 84)
STEM = (122, 76, 44)
TEXT = (40, 66, 44)
TITLE = (46, 120, 66)
NAME = (232, 92, 132)         # a cheerful pink for her name
PROMPT = (58, 88, 60)
PANEL = (255, 255, 255, 205)


@dataclass(frozen=True)
class Fonts:
    """Fonts sized relative to the screen so text scales with any display."""

    title: pygame.font.Font
    name: pygame.font.Font
    prompt: pygame.font.Font
    counter: pygame.font.Font


def make_fonts(screen_height: int) -> Fonts:
    # Font(None, ...) uses pygame's bundled font, so there is no dependency on
    # whatever fonts the target machine happens to have installed.
    return Fonts(
        title=pygame.font.Font(None, max(24, int(screen_height * 0.11))),
        name=pygame.font.Font(None, max(20, int(screen_height * 0.09))),
        prompt=pygame.font.Font(None, max(16, int(screen_height * 0.055))),
        counter=pygame.font.Font(None, max(16, int(screen_height * 0.075))),
    )


def board_layout(screen_size: tuple[int, int]) -> tuple[int, int, int]:
    """Square cell size and top-left board offset that centre the grid on any
    screen -- no fixed resolution is baked in."""
    sw, sh = screen_size
    cell = min(sw // GRID_W, sh // GRID_H)
    ox = (sw - cell * GRID_W) // 2
    oy = (sh - cell * GRID_H) // 2
    return cell, ox, oy


def _cell_rect(gx: int, gy: int, cell: int, ox: int, oy: int, inset: float) -> pygame.Rect:
    pad = int(cell * inset)
    return pygame.Rect(ox + gx * cell + pad, oy + gy * cell + pad, cell - 2 * pad, cell - 2 * pad)


def draw_board(surface: pygame.Surface, cell: int, ox: int, oy: int) -> None:
    surface.fill(BG)
    for gy in range(GRID_H):
        for gx in range(GRID_W):
            color = BOARD_A if (gx + gy) % 2 == 0 else BOARD_B
            pygame.draw.rect(surface, color, (ox + gx * cell, oy + gy * cell, cell, cell))


def draw_face(surface: pygame.Surface, cx: float, cy: float, size: float) -> None:
    """Two eyes and a smile, sized to `size` and centred on (cx, cy)."""
    eye_r = max(3, int(size * 0.14))
    pupil_r = max(2, int(size * 0.07))
    off_x = size * 0.22
    eye_y = cy - size * 0.10
    for sx in (-1, 1):
        ex = int(cx + sx * off_x)
        pygame.draw.circle(surface, EYE_WHITE, (ex, int(eye_y)), eye_r)
        pygame.draw.circle(surface, EYE_DARK, (ex, int(eye_y + eye_r * 0.25)), pupil_r)
    # A smile as a 5-point polyline: the middle sits lower than the ends, so it
    # always curves up into a smile regardless of pygame's arc conventions.
    smile = [
        (cx - size * 0.24, cy + size * 0.05),
        (cx - size * 0.12, cy + size * 0.19),
        (cx, cy + size * 0.23),
        (cx + size * 0.12, cy + size * 0.19),
        (cx + size * 0.24, cy + size * 0.05),
    ]
    pygame.draw.lines(surface, EYE_DARK, False,
                      [(int(x), int(y)) for x, y in smile], max(2, int(size * 0.06)))


def _draw_head(surface: pygame.Surface, cx: float, cy: float, size: float) -> None:
    """A rounded snake head with a smiling face, centred on (cx, cy)."""
    rect = pygame.Rect(0, 0, int(size), int(size))
    rect.center = (int(cx), int(cy))
    pygame.draw.rect(surface, SNAKE_HEAD, rect, border_radius=int(size * 0.40))
    draw_face(surface, rect.centerx, rect.centery, size)


def draw_snake(surface: pygame.Surface, snake: tuple, cell: int, ox: int, oy: int) -> None:
    """Body segments first, then the smiling head on top."""
    radius = int(cell * 0.36)
    for gx, gy in snake[1:]:
        rect = _cell_rect(gx, gy, cell, ox, oy, inset=0.07)
        pygame.draw.rect(surface, SNAKE_BODY, rect, border_radius=radius)
        pygame.draw.rect(surface, SNAKE_BODY_EDGE, rect, width=max(1, int(cell * 0.03)),
                         border_radius=radius)
    hx, hy = snake[0]
    _draw_head(surface, ox + (hx + 0.5) * cell, oy + (hy + 0.5) * cell, cell * 0.92)


def draw_apple(surface: pygame.Surface, cx: float, cy: float, size: float) -> None:
    """A recognisable apple: two red lobes, a highlight, a stem and a leaf."""
    r = size * 0.40
    for dx in (-r * 0.42, r * 0.42, 0.0):
        pygame.draw.circle(surface, APPLE_RED, (int(cx + dx), int(cy + r * 0.10)), int(r))
    pygame.draw.circle(surface, APPLE_HI, (int(cx - r * 0.35), int(cy - r * 0.35)),
                       max(2, int(r * 0.18)))
    pygame.draw.line(surface, STEM, (int(cx), int(cy - r * 0.7)),
                     (int(cx + r * 0.06), int(cy - r * 1.15)), max(2, int(size * 0.06)))
    leaf = pygame.Rect(0, 0, int(r * 0.8), int(r * 0.5))
    leaf.center = (int(cx + r * 0.5), int(cy - r * 1.0))
    pygame.draw.ellipse(surface, LEAF, leaf)


def draw_counter(surface: pygame.Surface, count: int, fonts: Fonts) -> None:
    """A little apple + number panel in the top-left, big and readable."""
    text = fonts.counter.render(str(count), True, TEXT)
    icon = text.get_height()
    pad = int(icon * 0.5)
    gap = int(icon * 0.4)
    panel_w = pad * 2 + icon + gap + text.get_width()
    panel_h = pad * 2 + icon
    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(panel, PANEL, panel.get_rect(), border_radius=panel_h // 3)
    surface.blit(panel, (20, 20))
    draw_apple(surface, 20 + pad + icon / 2, 20 + panel_h / 2, icon)
    surface.blit(text, (20 + pad + icon + gap, 20 + (panel_h - text.get_height()) // 2))


def _draw_welcome_snake(surface: pygame.Surface, w: int, h: int) -> None:
    n = 7
    seg = int(min(w, h) * 0.075)
    spacing = int(seg * 1.15)
    y0 = int(h * 0.42)
    start_x = w // 2 - spacing * (n - 1) // 2
    pts = [(start_x + i * spacing, y0 + int(seg * 0.8 * math.sin(i * 0.7))) for i in range(n)]
    for x, y in pts[:-1]:
        pygame.draw.circle(surface, SNAKE_BODY, (x, y), seg // 2)
        pygame.draw.circle(surface, SNAKE_BODY_EDGE, (x, y), seg // 2, max(1, seg // 16))
    hx, hy = pts[-1]
    _draw_head(surface, hx, hy, seg)


def draw_welcome(surface: pygame.Surface, fonts: Fonts, t_ms: int) -> None:
    """Title, a smiling snake, her name, and a gently pulsing arrow prompt."""
    surface.fill(BG)
    w, h = surface.get_size()
    _blit_centred(surface, fonts.title.render("Lily Jane's Snake", True, TITLE), w // 2, int(h * 0.14))
    _draw_welcome_snake(surface, w, h)
    _blit_centred(surface, fonts.name.render("Lily Jane", True, NAME), w // 2, int(h * 0.64))
    prompt = fonts.prompt.render("Press an arrow to play", True, PROMPT)
    prompt.set_alpha(int(140 + 115 * abs(math.sin(t_ms / 500.0))))
    _blit_centred(surface, prompt, w // 2, int(h * 0.82))


def draw_game_over(surface: pygame.Surface, count: int, fonts: Fonts) -> None:
    """A gentle end screen -- never punishing or guilt-inducing."""
    w, h = surface.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 90))
    surface.blit(overlay, (0, 0))
    _blit_centred(surface, fonts.title.render("Let's try again!", True, (255, 255, 255)),
                  w // 2, int(h * 0.36))
    # "You ate N" with a little apple to its right.
    count_text = fonts.name.render(f"You ate {count}", True, NAME)
    cy = int(h * 0.52)
    apple = fonts.name.get_height()
    left = w // 2 - (count_text.get_width() + apple) // 2
    surface.blit(count_text, (left, cy - count_text.get_height() // 2))
    draw_apple(surface, left + count_text.get_width() + apple / 2, cy, apple)
    _blit_centred(surface, fonts.prompt.render("Press an arrow to play", True, (240, 240, 240)),
                  w // 2, int(h * 0.70))


def _blit_centred(surface: pygame.Surface, text: pygame.Surface, cx: int, cy: int) -> None:
    surface.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))


def render_snake_icon(size: int) -> pygame.Surface:
    """A standalone snake-head icon on a transparent background (for the
    desktop launcher)."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    margin = int(size * 0.08)
    body = pygame.Rect(margin, margin, size - 2 * margin, size - 2 * margin)
    pygame.draw.rect(surface, SNAKE_HEAD, body, border_radius=int(size * 0.28))
    pygame.draw.rect(surface, SNAKE_BODY_EDGE, body, width=max(2, int(size * 0.03)),
                     border_radius=int(size * 0.28))
    draw_face(surface, size / 2, size / 2, size * 0.9)
    return surface
