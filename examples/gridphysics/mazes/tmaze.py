'''
VGDL example: a classical RL benchmark for memory

@author: Tom Schaul
'''

from mazegames import commonmaze_game

polarTmaze_game = commonmaze_game +"""
        avatar   > RotatingAvatar
    TerminationSet
        SpriteCounter stype=goal limit=1 win=True
"""

Tmaze_game = commonmaze_game +"""
        avatar   > MovingAvatar
    TerminationSet
        SpriteCounter stype=goal limit=1 win=True
"""


def tmaze(length):
    s =      "wwwwwwwww\n"
    s +=     "w0 4w2 0w\n"
    for _ in range(length-1):
        s += "ww www ww\n"
    s +=     "wm3www3mw\n"
    s +=     "wwwwwwwww\n"
    return s


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(polarTmaze_game, tmaze(4))    