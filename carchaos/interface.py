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

class Event(object):
    def __init__(self, name, call=None, *args):
        self.name=name
        self.call=call
        self.args=args
        
    def call(self):
        self.call_count+=1
        if call:
            self.call(*self.args)
            self.call_success+=1
            
    def set_call(self, call):
        self.call=call
    call_count=0
    call_success=0

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
        for animation in self.animations:
            del animation
        
    def set_position(self, x=None, y=None):
        if None in (x, y):
            x, y=self.x, self.y
        self.position=(x, y)
        self.x, self.y=x, y
        
    def set_meta(self, key, value):
        self.meta_data[key]=value
    
    meta_data={}
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
        
    def set_antialiasing(self, antialias):
        self.antialiasing=antialias
    
    def draw(self, display):
        super(Label, self).draw(display)
        #self.display=display
        result=self.font.render(self.text, self.antialiasing, self.color)
        display.blit(result, (self.position[0]-result.get_width()*.5, self.position[1]-result.get_height()*.5))
        #self.width, self.height=result.get_size()
        #self._surface=result
        
    def set_text(self, text):
        self.text=text
    background_color=None
    
class Rectangle(Widget):
    def __init__(self, color, dimensions, border=0):
        self.color=color
        self.dimensions=dimensions
        self.shape=pygame.Rect(*dimensions)
        self.border=border
    
    def draw(self, display):
        super(Rectangle, self).draw(display)
        pygame.draw.rect(display, self.color, self.shape, self.border)

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
        super(Button, self).draw(display)
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
        
    def set_text_color(self, *color):
        self.label.set_color(color)
        
    display=None
        
class Image(Widget):
    """An image widget"""
    def __init__(self, source, dimensions, grabber=None):
        self.source=source
        self.x, self.y, self.width,  self.height=dimensions
        self.position=(self.x, self.y)
        self.grabber=grabber
        self.surface=pygame.image.load(self.source)
        print(source)
        if len(dimensions)>2 and None not in dimensions[2:]:
            print(dimensions)
            print(dimensions[2:])
            self.surface=pygame.transform.scale(self.surface, [int(i) for i in dimensions[2:]])
        
    def dimensions(self):
        return (self.x, self.y, self.width, self.height)
        
    def draw(self, display):
        super(Image, self).draw()
        display.blit(self.surface, (self.x-self.width*.5, self.y-self.height*.5, self.width, self.height))
        
class Animation(object):
    """Base class for all widget animations"""
    def set_widget(self, widget):
        self.widget=widget
        self.x=widget.x
        self.y=widget.y
        
    def __del__(self):
        print("\n"*40)
    
    def start(self):
        self.playing=True
        
    def stop(self):
        self.playing=False
        
    def toggle(self):
        self.playing=False if self.playing else True
    
    playing=False
    
    
class SlideAnimation(Animation):
    def __init__(self, vertical_direction, horizontal_direction, speed=1, rate=1, started=False):
        super(SlideAnimation, self).__init__()
        self.horizontal_direction=horizontal_direction
        self.vertical_direction=vertical_direction
        self.speed=speed
        self.last_update=time.time()
        self.rate=rate
        self.playing=started
    
    def update_animation(self):
        t=time.time()
        if t>=self.last_update+self.rate and self.playing:
            if self.horizontal_direction!=None:
                self.y+=self.horizontal_direction*self.speed
            if self.vertical_direction!=None:
                self.x+=self.vertical_direction*self.speed
            self.widget.set_position(self.x, self.y)
            self.last_update=time.time()
        if self.playing and self.limit!=0 and t>=self.limit+self.limit_start:
            self.playing=False
            self.limit=0
            
            
    def reverse_direction(self, horizontal=None, vertical=None):
        if horizontal:
            self.horizontal_direction*=-1
        if vertical:
            self.vertical_direction*=-1
        
    def set_direction(self, horizontal=None, vertical=None):
        if horizontal:
            self.vertical_direction=horizontal
        if vertical:
            self.vertical_direction=vertical
    
    def start(self, limit=None):
        super(SlideAnimation, self).start()
        self.limit_start=time.time()
        print(limit)
        if limit:
            self.limit=limit
    
    def toggle(self, limit=None):
        if self.playing:
            return self.stop()
        self.start(limit)
        
    def set_slide_event(self, call):
        #slide_event=Event("slide", call)
        #self.slide_event=slide_event
        slide_event.set_call(call)
        events.append(self.slide_event)
            
    
    events=[]    
    last_update=0
    limit_start=0
    limit=0
    slide_event=Event("slide")
    
