'''
VGDL example: pick up as many gold bricks as possible, but not too many, or you'll sink.

@author: Tom Schaul
'''

overload_level = """
wwwwwwwwwwwwwwwwwww
wA  .  0     ..  Gw
w0  .  -     ..  0w
wwwww -    0 wwwwww
w     w        w 0w
w 0   wwwwwww    ww
w  0      0  0 0  w
wwwww     www    0w
w000      0    0  w
w000w        0  www
wwwwwwwwwwwwwwwwwww
"""

overload_game = """
BasicGame
    SpriteSet    
        structure > Immovable            
            goal  > color=GREEN
            marsh > color=BROWN
        gold  > Resource color=GOLD res_limit=10 # this limit is only used for visualizing progress
        moving >
            avatar > MovingAvatar            
            random > RandomNPC speed=1 cooldown=8
    InteractionSet
        gold moving     > collectResource
        gold moving     > killSprite
        moving wall     > stepBack
        moving marsh    > killIfHasMore      resource=gold limit=11
        goal avatar     > killIfOtherHasMore resource=gold limit=10
        
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False
    
    LevelMapping
        G > goal
        . > marsh
        0 > gold
        1 > random
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(overload_game, overload_level)    