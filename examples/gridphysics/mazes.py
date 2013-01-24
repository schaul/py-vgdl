'''
Maze-like games: find the exit in the minimal amount of time.

@author: Tom Schaul
'''

maze_level_1 = """
wwwwwww
w    0w
w     w
w1    w
wwwwwww
"""

maze_level_2 = """
wwwwwwwwwwwww
w1       w  w
w  w        w
w   w   w  ww
www w   wwwww
w       w 0 w
w          ww
w          ww
wwwwwwwwwwwww
"""

maze_level_3 = """
wwwwwwwwwwwww
w1   w  w  ww
w ww  w  w  w
w   ww  w  ww
www w w ww ww
w   w w w 0 w
w  w   w w ww
w    w     ww
wwwwwwwwwwwww
"""

office_layout = """
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww        
w 1   w     w     w     w     w     w        
w     w     w     w     w     w     w        
w     w     w     w     w     w     w        
w     w     w     w     w     w     w        
w     w     w     w     w     w     w        
w     w     w     w     w     w     w        
w     w     w     w     w     w     w        
w     w     w     w     w     w     w        
ww wwwww wwwww wwwww wwwww wwwww wwww        
w                                   w        
w                                   wwwwwwwww
w                                   w       w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww           w
                                w   w       w
                                w   w       w
                                w   w       w
                                w   wwwwwwwww
                                w   w       w
                                w           w
                                w   w       w
                                w   w       w
                                w   w       w
                                w   wwwwwwwww
                                w   w        
                                w 0 w        
                                wwwww        
"""
        
maze_game = """
BasicGame 
    SpriteSet         
        wall   > Immovable 
        goal   > Immovable color=GREEN
        avatar > MovingAvatar
    LevelMapping
        w > wall
        0 > goal
        1 > avatar                    
    InteractionSet
        avatar wall   > stepBack
        goal avatar   > killSprite                                
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(maze_game, maze_level_1)
    VGDLParser.playGame(maze_game, maze_level_2)
    VGDLParser.playGame(maze_game, maze_level_3)
    VGDLParser.playGame(maze_game, office_layout)
        