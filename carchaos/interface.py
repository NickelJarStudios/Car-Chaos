"""Copyright (c) 2013 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import pygame
from operator import sub

class Widget:
    """Base class for all widgets"""
    def dimensions(self):
        return self.x, self.y, self._surface.get_width(), self._surface.get_height()
        
class Label(Widget):
    """A text widget"""
    def __init__(self, text, font, color, size, position, bold=False, italic=False, antialias=True):
        self.text=text
        self.color=color
        self.font=pygame.font.SysFont(font, int(size), bold, italic)
        self.antialiasing=antialias
        self.position=position
        self.x, self.y=position
        self._surface=self.font.render(self.text, antialias, color)
        
    def set_background_color(self, color):
        self.background_color=color
        
    def set_color(self, color):
        self.color=color
        
    def set_position(self, x, y):
        self.position=(x, y)
        
    def set_antialiasing(self, antialias):
        self.antialiasing=antialias
    
    def draw(self, display):
        self.display=display
        result=self.font.render(self.text, self.antialiasing, self.color)
        display.blit(result, (self.position[0]-result.get_width()*.5, self.position[1]-result.get_height()*.5))
        self._surface=result
        
    background_color=None

class Button(Widget):
    def __init__(self, text, color=(0, 0, 80), dimensions=(0, 0, 50, 100), call=None):
        self.color=color
        self.highlight_color=(255-color[0], 255-color[1], 255-color[2])
        self.x, self.y, self.width, self.height=dimensions
        self.label=Label(text, "ariel", (255, 255, 255), self.height*.75, (self.x+self.width*.5, self.y+self.height*.5))
        self.call=call
        
    def set_text(self, text):
        self.text=text
        
    def set_size(self, width, height):
        self.width=width
        self.height=height
        
    def set_position(self, x, y):
        self.x=x
        self.y=y
        
    def set_color(self, color):
        self.color=color
        self.highlight_color=(255-color[0], 255-color[1], 255-color[2])
        
    def set_callback(self, call):
        self.call=call
        
    def dimensions(self):
        return (self.x, self.y, self.width, self.height)
        
    def draw(self, display):
        self._surface=pygame.draw.rect(display, self.color, self.dimensions())
        self.display=display
        mouse_x, mouse_y=pygame.mouse.get_pos()
        if type(self.label.text)==str:
            font=pygame.font.SysFont(None, 
                display.get_height()/12)
            #self.label.set_position((self.x+self.width/3)*(display.get_height()/display.get_width()), self.y+5)
            self.label.draw(display)
        elif type(self.text)==pygame.Surface:
            display.blit(self.text)
        if self.x<=mouse_x<=self.x+self.width and self.y<=mouse_y<=self.y+self.height:
            self.set_hovered(True)
            if pygame.mouse.get_pressed()[0] and self.call:
                self.call()
        
    def set_hovered(self, mode=True):
        self.hovered=mode
        self.color=tuple(map(sub, (255, 255, 255), self.color[:2]+(.75,)))
        
class Image(Widget):
    """An image widget"""
    def __init__(self, source, dimensions):
        self.source=source
        self.x, self.y, self.width, self.height=dimensions
        
    def dimensions(self):
        return self.dimensions
        
    def draw(self, display):
        display.blit(pygame.image.load(self.source), (self.x-self.width*.5, self.y-self.height*.5))
