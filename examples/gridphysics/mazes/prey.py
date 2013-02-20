"""
A minimalist predator-prey environment with wrap-around.

@author: Tom Schaul
"""


def openmaze(size):
    res = ([' ']*size+['\n'])*size
    res[0] = 'A'
    res[size*size/2] = '0'
    return ''.join(res)


chasemaze_game = """
BasicGame 
    LevelMapping
        0 > prey        
    InteractionSet
        moving EOS  > wrapAround
        prey avatar > killSprite        
    SpriteSet         
        moving   >
            prey     > Missile speed=1 color=GREEN
            avatar   > OrientedAvatar draw_arrow=False                
    TerminationSet
        SpriteCounter stype=prey limit=0 win=True
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(chasemaze_game, openmaze(8))   