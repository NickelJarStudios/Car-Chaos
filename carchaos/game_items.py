"""Copyright (c) 2013 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import pygame
import os

class Tile:
    def __init__(self, image_source, penetrable, z=0):
        self.image=pygame.image.load(os.path.join("/".join(__file__.split("/")[:-1]), image_source))
        self.image.convert()
        self.z_level=z
        
class Car(object):
    def __init__(self, image_source, vehicle_type, default_speed, player_controlled=False):
        self.set_image(os.path.join("/".join(__file__.split("/")[:-1]), image_source))
        self.type=vehicle_type
        self.default_speed=default_speed
        self.speed=default_speed
        
    def set_image(self, source):
        self.image=pygame.image.load(os.path.join("/".join(__file__.split("/")[:-1]), source))
        self.image.convert_alpha()
        
    def move_forward(self):
        self.x+=self.speed
        
    def move_right(self):#In this case, slide right
        self.y+=self.speed*.25
        
    def move_back(self):#Reverse
        self.x-=self.speed
        
    def move_left(self):
        self.y-=self.speed*.25
        
    def position(self):
        return self.x, self.y
        
    def draw(self, display, width, height):
        display.blit(self.image, width*.5, height*.5)
    
    x=0
    y=0
        

class PlayerCar(Car):
    def __init__(self):
        super(PlayerCar, self).__init__("images/sprites/carsprite.png", 0, 50, True)
        
class Level(object):
    def __init__(self):
        print("Sup fam?")
        
    def render_tiles(self):
        for y in range(len(map_layout)):
            for x in map_layout[y]:
                tile_layout[y][x]=self.create_tile(x)
                print(x+","),
            print("")
            
    def create_player(self):
        self.player=PlayerCar()
        return self.player
                
    def create_tile(self, tile_id):
        if tile_id==0:
            return Tile("images/sprites/road-lane.png", True)
    map_layout=[[]]
    tile_layout=[[]]
    
class LevelOne(Level):
    def __init__(self):
        super(LevelOne, self).__init__()
        
