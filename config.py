"""Player-facing tuning for Lily Jane's Snake.

The four knobs are named in French to match the parent's working language;
the on-screen game text stays English. Editing this file is all the parent
needs to slow the game down, mute it, run it in a window for development, or
(later, as she grows) switch on the classic "you can die" rules.
"""

# Death rules. False = the gentle no-fail game (the right default for a
# 5-year-old). True = classic Snake: hitting an edge or your own body ends
# the run.
mort_activee: bool = False

# Speed, in grid cells per second, constant for the whole game. A slow 4-5
# gives her time to see every turn coming.
vitesse: float = 4.0

# Sound on/off. True = happy munch + start sounds; False = silent, so she can
# play while someone nearby is working.
son_active: bool = True

# Full-screen (True) so she cannot fall out into window controls, or windowed
# (False), which is handy while developing.
plein_ecran: bool = True
