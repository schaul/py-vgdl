'''
VGDL example: a simple artillery game. Basic components for "Tank Wars".

@author: Tom Schaul
'''


artillery_game = """
BasicGame
    SpriteSet    
        pad    > Immovable color=BLUE 
        avatar > AimedAvatar stype=bullet
        bullet > Missile physicstype=GravityPhysics speed=25 singleton=True
            
    TerminationSet
        SpriteCounter stype=pad    win=True     
        SpriteCounter stype=avatar win=False     
           
    InteractionSet
        wall bullet > killSprite 
        bullet wall > killSprite 
        pad bullet > killSprite
        avatar wall > stepBack
        avatar EOS > stepBack
        bullet EOS > killSprite

    LevelMapping
        G > pad
"""

artillery_level = """
wwwwwwwwwwwwwwwwwwwwww
w        w    w      w
w           www      w
w             w     ww
w           G        w
w   w                w
w    www          w  w
w      wwwwwww  www  w
w              ww    w
w  G            w    w
w  ww  G           G w
wA    wwwwww         w
wwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(artillery_game, artillery_level)
        