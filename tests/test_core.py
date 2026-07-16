"""Behavioural tests for the pure game core.

Everything here drives the core through its single public seam --
``step(state, input)`` -- and asserts on the returned state. Nothing reaches
into rendering, timing, pygame, or sound; there is nothing else to reach into,
which is the whole point of the seam.
"""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from snake_core import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Cell,
    Direction,
    GameState,
    Pick,
    Tick,
    Turn,
    step,
)


def make(
    snake: Sequence[Cell],
    direction: Direction,
    *,
    width: int = 15,
    height: int = 12,
    death_enabled: bool = False,
    fruit: Cell = (0, 0),
    pick: Pick | None = None,
) -> GameState:
    """Build a state; the default fruit placer deterministically picks the
    first free cell in reading order."""
    placer: Pick = pick if pick is not None else (lambda free: free[0])
    return GameState(
        width=width,
        height=height,
        snake=tuple(snake),
        direction=direction,
        fruit=fruit,
        death_enabled=death_enabled,
        pick=placer,
    )


# --- Ticket 01: walking snake ------------------------------------------------


def test_tick_moves_head_one_cell_and_body_follows() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT)
    nxt = step(state, Tick())
    assert nxt.snake == ((6, 5), (5, 5), (4, 5))


def test_tick_keeps_length_when_not_eating() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT)
    assert len(step(state, Tick()).snake) == 3


def test_turn_sets_direction_without_moving() -> None:
    state = make([(5, 5), (4, 5)], RIGHT)
    turned = step(state, Turn(UP))
    assert turned.direction == UP
    assert turned.snake == state.snake  # a turn does not move the snake


def test_turn_then_tick_moves_in_the_new_direction() -> None:
    state = make([(5, 5), (4, 5)], RIGHT)
    moved = step(step(state, Turn(UP)), Tick())
    assert moved.snake[0] == (5, 4)


def test_180_reversal_is_accepted_and_not_fatal() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT)
    reversed_ = step(state, Turn(LEFT))
    assert reversed_.direction == LEFT  # any direction is accepted
    folded = step(reversed_, Tick())
    assert folded.game_over is False  # folding onto itself never ends the game


@pytest.mark.parametrize(
    ("head", "direction", "expected_head"),
    [
        ((0, 5), LEFT, (14, 5)),    # off the left edge -> back on the right
        ((14, 5), RIGHT, (0, 5)),   # off the right edge -> back on the left
        ((7, 0), UP, (7, 11)),      # off the top edge -> back at the bottom
        ((7, 11), DOWN, (7, 0)),    # off the bottom edge -> back at the top
    ],
)
def test_wraps_around_every_edge(
    head: Cell, direction: Direction, expected_head: Cell
) -> None:
    state = make([head], direction)
    nxt = step(state, Tick())
    assert nxt.snake[0] == expected_head
    assert nxt.game_over is False  # crossing an edge is never fatal by default


def test_crossing_own_body_is_harmless_by_default() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT)
    folded = step(step(state, Turn(LEFT)), Tick())
    assert folded.snake[0] in folded.snake[1:]  # the head really overlaps the body
    assert folded.game_over is False


# --- Ticket 02: fruit, growth & counter --------------------------------------


def test_eating_grows_the_snake_by_exactly_one() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, fruit=(6, 5))
    nxt = step(state, Tick())
    assert nxt.snake == ((6, 5), (5, 5), (4, 5), (3, 5))  # tail kept, head added


def test_eating_increments_the_counter() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, fruit=(6, 5))
    assert step(state, Tick()).fruits_eaten == 1


def test_not_eating_leaves_the_counter_unchanged() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, fruit=(0, 0))
    assert step(state, Tick()).fruits_eaten == 0


def test_fruit_placement_is_deterministic_via_the_injected_source() -> None:
    # A fixed placer gives a fixed outcome, with no dependency on real
    # randomness: the first free cell in reading order is (0, 0).
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, fruit=(6, 5))
    assert step(state, Tick()).fruit == (0, 0)


def test_respawned_fruit_is_never_on_the_snake() -> None:
    offered: list[Sequence[Cell]] = []

    def spy(free: Sequence[Cell]) -> Cell:
        offered.append(free)
        return free[0]

    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, fruit=(6, 5), pick=spy)
    nxt = step(state, Tick())
    # The core only ever offers the placer cells that are free of the snake...
    assert offered and all(cell not in nxt.snake for cell in offered[0])
    # ...so wherever the fruit lands, it is never on the snake.
    assert nxt.fruit not in nxt.snake


# --- Ticket 05: death toggle -------------------------------------------------


def test_edge_crossing_ends_the_run_when_death_enabled() -> None:
    state = make([(14, 5)], RIGHT, death_enabled=True)
    assert step(state, Tick()).game_over is True


def test_self_collision_ends_the_run_when_death_enabled() -> None:
    # Reversing folds the head onto the neck; with death on, that ends the run.
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, death_enabled=True)
    dead = step(step(state, Turn(LEFT)), Tick())
    assert dead.game_over is True


def test_edge_crossing_wraps_when_death_disabled() -> None:
    state = make([(14, 5)], RIGHT, death_enabled=False)
    nxt = step(state, Tick())
    assert nxt.game_over is False
    assert nxt.snake[0] == (0, 5)  # it wrapped instead of dying


def test_self_collision_is_harmless_when_death_disabled() -> None:
    state = make([(5, 5), (4, 5), (3, 5)], RIGHT, death_enabled=False)
    folded = step(step(state, Turn(LEFT)), Tick())
    assert folded.game_over is False


def test_step_is_a_no_op_once_the_run_is_over() -> None:
    dead = step(make([(14, 5)], RIGHT, death_enabled=True), Tick())
    assert dead.game_over is True
    # Further inputs do nothing until the shell starts a new game.
    assert step(dead, Tick()) == dead
    assert step(dead, Turn(UP)) == dead
