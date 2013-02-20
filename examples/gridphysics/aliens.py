'''
VGDL example: a simplified variant of the classic space-invaders.

@author: Tom Schaul
'''


# the (initial) level as a block of characters 
aliens_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
w                              w
w1                             w
w000                           w
w000                           w
w                              w
w                              w
w                              w
w                              w
w    000      000000     000   w
w   00000    00000000   00000  w
w   0   0    00    00   00000  w
w                A             w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

# The game dynamics are specified as a paragraph of text
aliens_game="""
BasicGame
    SpriteSet
        base    > Immovable    color=WHITE
        avatar  > FlakAvatar   stype=sam
        missile > Missile
            sam  > orientation=UP    color=BLUE singleton=True
            bomb > orientation=DOWN  color=RED  speed=0.5
        alien   > Bomber       stype=bomb   prob=0.01  cooldown=3 speed=0.75
        portal  > SpawnPoint   stype=alien  delay=16   total=20
    
    LevelMapping
        0 > base
        1 > portal

    TerminationSet
        SpriteCounter      stype=avatar               limit=0 win=False
        MultiSpriteCounter stype1=portal stype2=alien limit=0 win=True
        
    InteractionSet
        avatar  EOS  > stepBack
        alien   EOS  > turnAround        
        missile EOS  > killSprite
        missile base > killSprite
        base missile > killSprite
        base   alien > killSprite
        avatar alien > killSprite
        avatar bomb  > killSprite
        alien  sam   > killSprite         
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    # parse, run and play.
    VGDLParser.playGame(aliens_game, aliens_level)    