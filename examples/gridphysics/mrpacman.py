'''
VGDL example: a modified version of Pacman, but this time ghosts that uses A* to chase the player. 


@author: Chong-U Lim
'''


pacman_game = """
BasicGame
    SpriteSet
        food > Immovable
            pellet > color=WHITE shrinkfactor=0.8
            power  > color=LIGHTGREEN shrinkfactor=0.5
        nest > SpawnPoint
            redspawn > stype=red
            orangespawn > stype=orange
            bluespawn > stype=blue
            pinkspawn > stype=pink
        moving >
            ghost > AStarChaser stype=hungry cooldown=3
                red    > color=LIGHTRED    singleton=True
                blue   > color=LIGHTBLUE   singleton=True
            ghost > Chaser stype=hungry cooldown=3
                pink   > color=PINK        singleton=True
                orange > color=LIGHTORANGE singleton=True
            pacman > OrientedAvatar 
                hungry  > color=YELLOW
                powered > color=ORANGE            
            
    InteractionSet
        hungry  power > transformTo stype=powered 
        powered ghost > transformTo stype=hungry
        power hungry  > killSprite
        ghost powered > killSprite
        hungry ghost  > killSprite
        food pacman > killSprite
        moving wall > stepBack        
        moving EOS  > wrapAround        
        
    LevelMapping
        0 > power
        . > pellet
        A > hungry
        1 > redspawn red
        2 > bluespawn blue
        3 > pinkspawn pink
        4 > orangespawn orange
        
    TerminationSet
        SpriteCounter stype=food   win=True     
        SpriteCounter stype=pacman win=False     
    
"""

pacman_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w............ww............w
w.wwww.wwwww.ww.wwwww.wwww.w
w0wwww.wwwww.ww.wwwww.wwww0w
w.wwww.wwwww.ww.wwwww.wwww.w
w..........................w
w.wwww.ww.wwwwwwww.ww.wwww.w
w.wwww.ww.wwwwwwww.ww.wwww.w
w......ww....ww....ww......w
wwwwww.wwwww ww wwwww.wwwwww
wwwwww.wwwww ww wwwww.wwwwww
wwwwww.ww          ww.wwwwww
wwwwww.ww          ww.wwwwww
wwwwww.ww www  www ww.wwwwww
      .   ww1234ww   .      
wwwwww.ww wwwwwwww ww.wwwwww
wwwwww.ww          ww.wwwwww
wwwwww.ww          ww.wwwwww
wwwwww.ww wwwwwwww ww.wwwwww
wwwwww.ww wwwwwwww ww.wwwwww
w............ww............w
w.wwww.wwwww.ww.wwwww.wwww.w
w0wwww.wwwww.ww.wwwww.wwww0w
w...ww.......A........ww...w
www.ww.ww.wwwwwwww.ww.ww.www
www.ww.ww.wwwwwwww.ww.ww.www
w......ww....ww....ww......w
w.wwwwwwwwww.ww.wwwwwwwwww.w
w.wwwwwwwwww.ww.wwwwwwwwww.w
w..........................w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(pacman_game, pacman_level)    