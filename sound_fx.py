"""Code-generated sound effects for Lily Jane's Snake.

Two short, friendly sounds -- a "munch/ding" when a fruit is eaten and a rising
start jingle when the game opens -- are synthesised at runtime with nothing but
the Python standard library (`wave` + `math`). There are no audio files to ship
or license, and no background music.

This lives in the shell only; the pure game core stays free of audio. A single
config switch (`son_active`) mutes everything.
"""

from __future__ import annotations

import io
import math
import struct
import wave
from collections.abc import Iterator

import pygame

SAMPLE_RATE = 44100

# (frequency in Hz, duration in seconds) note lists.
_MUNCH = [(784.0, 0.05), (1175.0, 0.11)]                       # a bright rising ding
_START = [(523.0, 0.08), (659.0, 0.08), (784.0, 0.10), (1047.0, 0.16)]  # C-E-G-C jingle


def _tone(freq: float, dur: float, volume: float = 0.4) -> Iterator[int]:
    """A sine tone with a short attack and release so it never clicks."""
    n = max(1, int(SAMPLE_RATE * dur))
    attack = max(1, int(SAMPLE_RATE * 0.005))
    release_from = int(n * 0.7)
    for i in range(n):
        env = min(1.0, i / attack)
        if i >= release_from:
            env *= max(0.0, (n - i) / max(1, n - release_from))
        yield int(volume * env * 32767 * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))


def _wav_bytes(notes: list[tuple[float, float]]) -> bytes:
    """Render a note list to a mono 16-bit WAV, in memory, via `wave`."""
    samples: list[int] = []
    for freq, dur in notes:
        samples.extend(_tone(freq, dur))
    frames = struct.pack("<%dh" % len(samples), *samples)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(frames)
    return buf.getvalue()


class Sounds:
    """Loads and plays the two effects, honouring the `enabled` switch.

    If audio is muted or no audio device is available (e.g. a headless test
    machine), every `play_*` call is a silent no-op -- the game never crashes
    over sound.
    """

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled
        self._start: pygame.mixer.Sound | None = None
        self._munch: pygame.mixer.Sound | None = None
        if not enabled:
            return
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
            self._start = pygame.mixer.Sound(io.BytesIO(_wav_bytes(_START)))
            self._munch = pygame.mixer.Sound(io.BytesIO(_wav_bytes(_MUNCH)))
        except (pygame.error, NotImplementedError):
            # No audio device (pygame.error) or a pygame built without the
            # mixer module (NotImplementedError): stay silent, keep playing.
            self.enabled = False

    def play_start(self) -> None:
        if self._start is not None:
            self._start.play()

    def play_munch(self) -> None:
        if self._munch is not None:
            self._munch.play()
