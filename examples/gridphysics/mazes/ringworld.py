

portalmaze_game = """
BasicGame 
    LevelMapping
        1 > portal1
        2 > portal2
        3 > portal3
        4 > portal4
        G > goal
        
    InteractionSet
        avatar wall   > stepBack
        goal avatar   > killSprite
        avatar portal > teleportToExit

    SpriteSet         
        structure > Immovable
            goal    > color=GREEN
            portalexit >
                portal3 >
                portal4 >
            portal  > Portal color=BLUE 
                portal1 > stype=portal3
                portal2 > stype=portal4
            
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
"""

wrapmaze_game = """
BasicGame 
    LevelMapping
        G > goal
        
    InteractionSet
        avatar wall   > wrapAround offset=1
        goal avatar   > killSprite
        
    SpriteSet         
        structure > Immovable
            goal    > color=GREEN
        avatar > OrientedAvatar
            
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
"""

def portalringworld(length):
    assert length > 5
    s =      "www\n"
    s +=     "w2w\n"
    s +=     "w3w\n"
    for _ in range((length-1)/2-2):
        s += "w w\n"
    s += "wGw\n"
    for _ in range(length/2-2):
        s += "w w\n"
    s +=     "wAw\n"
    s +=     "w4w\n"
    s +=     "w1w\n"
    s +=     "www\n"
    return s


def ringworld(width):
    assert width > 1
    level = ["w"]*(width+2)+["\n"]
    level += ["w"]+[" "]*width+["w\n"]
    level += ["w"]*(width+2)+["\n"]
    level[int(width*1.5+3.5)] = 'G'    
    level[-(width+5)] = 'A'    
    level_str = ''.join(level)
    return level_str
    

if __name__ == "__main__":
    print ringworld(9)    
    from vgdl.core import VGDLParser
    VGDLParser.playGame(wrapmaze_game, ringworld(19))
    VGDLParser.playGame(portalmaze_game, portalringworld(19))