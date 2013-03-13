'''
VGDL example: a simplified (static) Zelda variant: Link needs to find
his sword, use it to cut through enemies, find a key and open the door.

@author: Tom Schaul
'''

zelda_level = """
wwwwwwwwwwwww
wA ww   w   w
w     1   1 w
w www   ww +w
w w  1 wwwwww
w ww   1 0  w
w1 w  w  w  w
w kw   1 w Gw
wwwwwwwwwwwww
"""

        
rigidzelda_game = """
BasicGame frame_rate=10
    SpriteSet     
        structure > Immovable
            goal   > color=GREEN
            door   > color=LIGHTGREEN
            key    > color=YELLOW     
            sword  > color=RED
            slash  > Flicker limit=5  singleton=True
            avatar  > MovingAvatar 
                naked   > 
                nokey   > color=RED
                withkey > color=YELLOW
            monster > color=ORANGE
    LevelMapping
        G > goal
        k > key        
        + > sword
        A > naked
        0 > door
        1 > monster            
    InteractionSet
        avatar wall    > stepBack
        nokey door     > stepBack
        goal avatar    > killSprite        
        monster nokey  > killSprite        
        naked monster  > killSprite
        withkey monster> killSprite
        key  avatar    > killSprite
        sword avatar   > killSprite
        nokey key   > transformTo stype=withkey
        naked sword > transformTo stype=nokey                
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False              
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(rigidzelda_game, zelda_level)    