"""The pure game core for Lily Jane's Snake.

This module holds *all* the game rules and knows nothing about pygame,
rendering, sound, timing, or the operating system. It exposes an immutable
``GameState`` and a single transition function, ``step(state, input)``, where
``input`` is either a ``Tick`` (advance one cell) or a ``Turn`` (set a new
direction).

Keeping every rule here is what lets the tests trust the game, and what makes
"grow into a real challenge later" a core-level change rather than a rewrite.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field, replace

# A cell is a grid coordinate (x, y); a direction is a unit (dx, dy) step.
# y increases downward to match screen coordinates, so UP decreases y.
Cell = tuple[int, int]
Direction = tuple[int, int]

UP: Direction = (0, -1)
DOWN: Direction = (0, 1)
LEFT: Direction = (-1, 0)
RIGHT: Direction = (1, 0)

# The default play field: few, big cells so everything is easy for a young
# child to see. The core owns this so rules and rendering share one source.
GRID_W = 15
GRID_H = 12

# How a new fruit's cell is chosen from the cells that are currently free.
# Injecting this -- rather than calling a global random function -- is what
# makes fruit placement deterministic under test.
Pick = Callable[[Sequence[Cell]], Cell]


def _random_pick() -> Pick:
    """The real random placer used in play; tests inject their own."""
    rng = random.Random()
    return lambda free: rng.choice(free)


@dataclass(frozen=True)
class Tick:
    """Advance the snake one cell in its current direction."""


@dataclass(frozen=True)
class Turn:
    """Set a new direction. Any direction is accepted, including a reversal."""

    direction: Direction


Input = Tick | Turn


@dataclass(frozen=True)
class GameState:
    """An immutable snapshot of the whole game."""

    width: int
    height: int
    snake: tuple[Cell, ...]  # head first, tail last; length >= 1
    direction: Direction
    fruit: Cell
    fruits_eaten: int = 0
    death_enabled: bool = False
    game_over: bool = False
    # The injected fruit placer. Excluded from equality/repr so two states
    # compare by their game data, not by which random stream they happen to
    # carry.
    pick: Pick = field(default_factory=_random_pick, compare=False, repr=False)

    @property
    def head(self) -> Cell:
        return self.snake[0]


def new_game(
    width: int = GRID_W,
    height: int = GRID_H,
    *,
    death_enabled: bool = False,
    pick: Pick | None = None,
) -> GameState:
    """A fresh, centred snake of length 3 moving right, with a fruit off it."""
    placer = pick if pick is not None else _random_pick()
    cx, cy = width // 2, height // 2
    snake: tuple[Cell, ...] = ((cx, cy), (cx - 1, cy), (cx - 2, cy))
    fruit = placer(_free_cells(width, height, set(snake)))
    return GameState(
        width=width,
        height=height,
        snake=snake,
        direction=RIGHT,
        fruit=fruit,
        death_enabled=death_enabled,
        pick=placer,
    )


def step(state: GameState, action: Input) -> GameState:
    """The single transition: apply one tick or one turn to the state."""
    if state.game_over:
        return state
    if isinstance(action, Turn):
        return replace(state, direction=action.direction)
    return _advance(state)


def _advance(state: GameState) -> GameState:
    """Move the head one cell in the current direction; the body follows.

    Eating the fruit (head enters the fruit's cell) keeps the tail, so the
    snake grows by one, bumps the counter, and spawns a fresh fruit on a free
    cell. Otherwise the tail is dropped and the snake simply slides forward.
    """
    hx, hy = state.snake[0]
    dx, dy = state.direction
    target = (hx + dx, hy + dy)
    off_edge = not (0 <= target[0] < state.width and 0 <= target[1] < state.height)

    # With death on, running off an edge ends the run instead of wrapping.
    if state.death_enabled and off_edge:
        return replace(state, game_over=True)

    # Wrap: leaving one side re-enters the opposite side.
    new_head = (target[0] % state.width, target[1] % state.height)

    eating = new_head == state.fruit
    grown = (new_head, *state.snake)
    new_snake = grown if eating else grown[:-1]

    # With death on, entering the body the snake will occupy ends the run. The
    # tail cell is exempt when not eating, since it moves out of the way -- the
    # classic Snake rule. With death off, the same overlap is simply harmless.
    if state.death_enabled and new_head in new_snake[1:]:
        return replace(state, game_over=True)

    if not eating:
        return replace(state, snake=new_snake)

    free = _free_cells(state.width, state.height, set(new_snake))
    new_fruit = state.pick(free) if free else state.fruit
    return replace(
        state,
        snake=new_snake,
        fruit=new_fruit,
        fruits_eaten=state.fruits_eaten + 1,
    )


def _free_cells(width: int, height: int, occupied: set[Cell]) -> list[Cell]:
    """Every grid cell not currently occupied, in stable reading order."""
    return [
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in occupied
    ]
