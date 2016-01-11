"""Copyright (c) 2013 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import pygame
from operator import sub
import time

UP=-1
DOWN=1
LEFT=-1
RIGHT=1

class Widget(object):
    """Base class for all widgets"""
    def dimensions(self):
        return self.x, self.y, self._surface.get_width(), self._surface.get_height()
    
    def set_current_widget_grabber(self, grabber):
        self.grabber=grabber
        
    def set_select_widgets(self, left, top, right, bottom):
        self.left_widget=left
        self.top_widget=top
        self.right_widget=right
        self.bottom_widget=bottom
    
    def draw(self, display=None):
        for animation in self.animations:
            animation.update_animation()
        
    def add_animation(self, animation):
        animation.set_widget(self)
        self.animations.append(animation)
        
    def __del__(self):
        print("Bye")
        for animation in self.animations:
            del animation
            print(len(self.animations))
    
    x, y=0, 0
    animations=[]
        
class Label(Widget):
    """A text widget"""
    def __init__(self, text, font, color=(255, 255, 255), size=20, position=(0, 0), bold=False, italic=False, antialias=True, grabber=None):
        self.text=text
        self.color=color
        self.font=pygame.font.SysFont(font, int(size), bold, italic)
        self.antialiasing=antialias
        self.position=position
        self.x, self.y=position
        self._surface=self.font.render(self.text, antialias, color)
        self.grabber=grabber
        
    def set_background_color(self, color):
        self.background_color=color
        
    def set_color(self, color):
        self.color=color
        
    def set_position(self, x=None, y=None):
        if None in (x, y):
            x, y=self.x, self.y
        self.position=(x, y)
        
    def set_antialiasing(self, antialias):
        self.antialiasing=antialias
    
    def draw(self, display):
        super(Label, self).draw(display)
        self.display=display
        result=self.font.render(self.text, self.antialiasing, self.color)
        display.blit(result, (self.position[0]-result.get_width()*.5, self.position[1]-result.get_height()*.5))
        self.width, self.height=result.get_size()
        self._surface=result
        
    background_color=None

class Button(Widget):
    def __init__(self, text, color=(0, 0, 80), dimensions=(0, 0, 50, 100), call=None, grabber=None):
        self.color=color
        self.highlight_color=tuple(map(sub, (255, 255, 255), self.color[:2]+(.75,)))
        self.x, self.y, self.width, self.height=dimensions
        self.label=Label(text, "ariel", (255-color[0], 255-color[1], 255-color[2]), self.height*.75, (self.x+self.width*.5, self.y+self.height*.5))
        self.call=call
        self.grabber=grabber
        
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
        super(Button, self).draw()
        if display==None:
            display=self.display
        elif self.display!=display:
            self.display=display
        self._surface=pygame.draw.rect(display, self.color, self.dimensions())
        self.display=display
        mouse_x, mouse_y=pygame.mouse.get_pos()
        if type(self.label.text)==str:
            font=pygame.font.SysFont(None, 
                display.get_height()/12)
            self.label.draw(display)
        elif type(self.text)==pygame.Surface:
            display.blit(self.text)
        if self.x<=mouse_x<=self.x+self.width and self.y<=mouse_y<=self.y+self.height:
            self.set_hovered(True)
            if pygame.mouse.get_pressed()[0] and self.call:
                self.call()
        else:
            self.set_hovered(False)
        
    def set_hovered(self, mode=True):
        if mode:
            self.hovered=mode
            self.color=self.highlight_color
            return
        self.hovered=mode
        self.color=self.highlight_color
        
    display=None
        
class Image(Widget):
    """An image widget"""
    def __init__(self, source, dimensions, grabber=None):
        self.source=source
        self.x, self.y, self.width, self.height=dimensions
        self.grabber=grabber
        
    def dimensions(self):
        return (self.x, self.y, self.width, self.height)
        
    def draw(self, display):
        super(Image, self).draw()
        display.blit(pygame.image.load(self.source), (self.x-self.width*.5, self.y-self.height*.5))
        
class Animation(object):
    """Base class for all widget animations"""
    def set_widget(self, widget):
        self.widget=widget
        self.x=widget.x
        self.y=widget.y
        
    def __del__(self):
        print("\n"*40)
    
class SlideAnimation(Animation):
    def __init__(self, vertical_direction, horizontal_direction, speed=1, rate=1):
        super(SlideAnimation, self).__init__()
        self.horizontal_direction=horizontal_direction
        self.vertical_direction=vertical_direction
        self.speed=speed
        self.last_update=time.time()
        self.rate=rate
    
    def update_animation(self):
        if time.time()>=self.last_update+self.rate:
            if self.horizontal_direction!=None:
                self.y+=self.horizontal_direction*self.speed
            if self.vertical_direction!=None:
                self.x+=self.vertical_direction*self.speed
            self.widget.set_position(self.x, self.y)
            self.last_update=time.time()
        
        
    last_update=0
