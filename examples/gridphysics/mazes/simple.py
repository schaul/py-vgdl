'''
A few simple layouts for maze-like games: find the exit in the minimal amount of time.

@author: Tom Schaul
'''

maze_level_1 = """
wwwwww
w   Gw
w    w
wAw  w
wwwwww
"""

maze_level_1b = """
wwwwww
w   Gw
w  w w
wA  ww
wwwwww
"""

maze_level_2 = """
wwwwwwwwwwwww
wA       w  w
w   w   w  ww
www w   wwwww
w       w G w
w    w     ww
wwwwwwwwwwwww
"""

maze_level_3 = """
wwwwwwwwwwwww
wA   w  w  ww
w ww  w  w  w
w   ww  w  ww
www w w ww ww
w   w w w G w
w  w   w w ww
w    w     ww
wwwwwwwwwwwww
"""

office_layout = """
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
w A   w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
w     w     w     w     w     w     wwwwwwwww
ww wwwww wwwww wwwww wwwww wwwww wwwwwwwwwwww
w                                   wwwwwwwww
w                                   wwwwwwwww
w                                   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww           w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   wwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww           w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   wwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   wwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww G wwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

office_layout_2 = """
wwwwwwwwwwwwwwwwwww
w A   w     w     w
w     w     w     w
w     w     w     w
w     w     w     w
ww wwwww wwwww wwww
w                Gw
wwwwwwwwwwwwwwwwwww
"""


corridor2 = """
wwwwwwwwwwwwww
w        wwwww
w   ww   wwwww
w m ww m wwwww
w wwwwww wwwww
w   ww   wwwww
w  bww wwwwwww
w      w    Gw
wwwwwwAw   www
w      w m www
w  mww w wwwww
w   ww   wwwww
w wwwwww wwwww
w   ww m wwwww
w  mww   wwwww
w        wwwww
wwwwwwwwwwwwww
"""
        

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    from mazegames import polarmaze_game, maze_game
    VGDLParser.playGame(maze_game, maze_level_1)
    VGDLParser.playGame(maze_game, maze_level_2)
    VGDLParser.playGame(maze_game, maze_level_3)
    VGDLParser.playGame(polarmaze_game, corridor2)
    VGDLParser.playGame(polarmaze_game, office_layout_2)
    VGDLParser.playGame(polarmaze_game, office_layout)
        