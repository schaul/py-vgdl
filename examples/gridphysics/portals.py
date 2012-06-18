'''
VGDL example: a simple teleport-and-avoid-fire game. 

@author: Tom Schaul
'''

portal_level = """
wwwwwwwwwwwwwwwwwww
w1  w  v  <  wO  2w
wo iw        wx   w
wwwww      o wwwwww
w     w r      w ow
w <   wwwwwww    ww
w      x     <    w
wwwww     www     w
wr        i       w
wwwIw   v    x  www
wwwwwwwwwwwwwwwwwww
"""

portal_game = """
BasicGame
    SpriteSet
        bullet > color=ORANGE
            sitting  > Immovable
            random   > RandomNPC speedup=0.25
            straight > Missile   speedup=0.5
                vertical   > direction=UP
                horizontal > direction=LEFT
        structure > Immovable            
            wall  > 
            goal  > color=GREEN
            portalentry > Portal color=BLUE
                entry1 > stype=exit1 
                entry2 > stype=exit2
            portalexit  > color=BROWN
                exit1  >
                exit2  >
        avatar    > MovingAvatar
    
    InteractionSet
        goal   avatar > killSprite
        avatar bullet > killSprite
        avatar wall   > stepBack
        straight wall > changeDirection
        avatar portalentry > teleportToExit
        
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False
    
    LevelMapping
        w > wall
        < > horizontal
        v > vertical
        x > sitting
        r > random
        1 > avatar
        2 > goal
        i > entry1
        I > entry2
        o > exit1
        O > exit2
        
"""

if __name__ == "__main__":
    from core import VGDLParser
    VGDLParser.playGame(portal_game, portal_level)    