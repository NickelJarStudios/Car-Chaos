 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

from . import storage, player, level, interface
import sys
import os
import time
try:
    import pygame, pygame.locals
except ImportError:
    print("""You don't have pygame installed. In order to use this application
        you must have pygame. See the README.md or README.txt file for
        instructions on how to get and install PyGame or run the installer.""")
        

class CarChaos:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        self.starting_time=time.time()
        self.info=pygame.display.Info()
        #self.height, self.width=self.info.current_h, self.info.current_w
        self.screen=pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN if self.fullscreen_enabled else pygame.RESIZABLE)
        self.menu_open=True
        
    def run(self):
        while True:
            self.update_graphics()
            #self.adjust_size()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.quit()
                elif event.type==pygame.KEYDOWN:
                    keys=pygame.key.get_pressed()
                    if keys[pygame.K_q]:
                        self.quit()
                elif event.type==pygame.VIDEORESIZE:
                    self.adjust_size()
            pygame.display.update()
    
    def update_graphics(self):
        pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.height))
        if (time.time()-self.starting_time)<=5:
            if not self.widget_exists("nickel-splash-logo"):
                self.add_widget(interface.Image(os.path.join("/".join(__file__.split("/")[:-1]), "images/nickel-jar-studios-logo-white.png"), (self.width*.5, self.height*.5, 200, 200)), "nickel-splash-logo")
                print(self.width)
                self.add_widget(interface.Label("Nickel Jar Studios", "Ariel", (255, 255, 255), 15, (self.width*.5, self.height*.5), True), "nickel-splash-title")
                copyright_text=interface.Label(u"Copyright © Brandan Balram, James Cogwil, Jordan Jones, Seth Nash", None, (255, 255, 255), 15, (self.width*.3, self.height*.9), True)
                copyright_text.set_position(copyright_text.dimensions()[2]*.5, self.height-copyright_text.dimensions()[3])
                self.add_widget(copyright_text, "nickel-splash-copyright")
        elif self.menu_open:
            self.show_menu()
            self.remove_widget("nickel-splash-logo")
            self.remove_widget("nickel-splash-title")
            #self.remove_widget("nickel-splash-copyright")
        for widget in self.widgets.values():
            widget.draw(self.screen)
    
    def show_menu(self):
        self.state="start menu"
        self.background_color=(0, 0, 255)
        pygame.mouse.set_visible(True)
        font=pygame.font.SysFont(None, 30)
        game_title=font.render("Car Chaos", 1, (255, 255, 255))
        self.screen.blit(game_title, (self.width/2-30, self.height/4))
        if not self.widget_exists("menu-play-button"):
            self.add_widget(interface.Button("Play", pygame.Color(90, 90, 90, 75),
         (self.width/2-50, self.height*.5-25, 100, 50)), "menu-play-button")
            self.add_widget(interface.Button("Options", pygame.Color(90, 90, 90, 75),
         (self.width/2-87.5, self.height*.5+50, 175, 50)), "menu-options-button")
            self.add_widget(interface.Button("Exit", pygame.Color(90, 90, 90, 75),
         (self.width/2-50, self.height*.5+125, 100, 50), self.quit), "menu-exit-button")
        
    def quit(self):
        pygame.font.quit()
        pygame.quit()
        sys.exit()
        
    def adjust_size(self):
        start_adjustment={
            "start menu":self.show_menu
        }.get(self.state, self.show_menu)()
    
    def add_widget(self, widget, widget_id):
        if not self.widget_exists(widget_id) and widget:
            self.widgets[widget_id]=widget
    
    def remove_widget(self, widget_id):
        if self.widget_exists(widget_id):
            self.widgets.pop(widget_id)
    
    def widget_exists(self, widget_id):
        return widget_id in self.widgets
    
    width=640
    height=640
    fullscreen_enabled=not False
    double_buffer_enabled=True
    state="off"
    widgets={}
    menu_open=True
    background_color=(0, 0, 0)

if __name__=="__main__":
    car_chaos=CarChaos()
