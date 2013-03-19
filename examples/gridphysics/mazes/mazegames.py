'''
Shared definitions for maze games.

@author: Tom Schaul
'''



commonmaze_game = """
BasicGame 
    LevelMapping
        m > wallmark
        . > floortile 
        G > goal
        2 > portalentry
        3 > portalexit
        4 > avatar portalentry
        
    InteractionSet
        avatar wall        > stepBack
        avatar wallmark    > stepBack
        goal avatar        > killSprite
        avatar portalentry > teleportToExit

    SpriteSet         
        structure > Immovable
            wallmark     > color=ORANGE
            floortile    > color=WHITE shrinkfactor=0.5
            goal         > color=GREEN
            portalentry  > Portal color=BLUE stype=portalexit
            portalexit   > color=BROWN"""

maze_game = commonmaze_game + """
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
"""

polarmaze_game = commonmaze_game +"""
        avatar   > RotatingAvatar
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
"""
