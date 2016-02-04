from pygame import draw, Rect

class Level:
    def __init__(self, surface, content):
        self.surface=surface
        
    #def update()
    def update(self):
        draw.rect(self.surface, (0, 10, 0), (0, 0, 10, 10))
        draw.rect(self.surface, (0, 40, 0), (50, 50, 100, 100))

def start_level(level_object, content):
    return Level(level_object.surface, content)#Content should just be a list of stuff from maps.py
    
