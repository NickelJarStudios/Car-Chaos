 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

from . import storage, player, level, interface, game_items, maps, stuff
import sys
import os
import time
import re
from copy import deepcopy

try:
    import pygame, pygame.locals
except ImportError:
    print("""You don't have pygame installed. In order to use this application
        you must have pygame. See the README.md or README.txt file for
        instructions on how to get and install PyGame or run the installer.""")

with open("/".join(os.path.dirname(__file__).split("/")[:-1])+"/credits.txt") as credits_file:
    credits=credits_file.read().decode("string_escape").splitlines()
    
class CarChaos:
    def __init__(self, command_line_input=None):
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        self.timer=pygame.time.Clock()
        stuff.clock=self.timer
        self.starting_time=time.time()
        self.info=pygame.display.Info()
        self.height, self.width=self.info.current_h, self.info.current_w
        pygame.key.set_repeat(100, 100)
        if not command_line_input:
            command_line_input={}
        elif command_line_input["dimensions"]:
            command_line_input["width"], command_line_input["height"]=[int(i) for i in command_line_input["dimensions"].lower().split("x")]
            self.width, self.height=int(command_line_input["width"]), int(command_line_input["height"])
        settings=storage.load_settings(command_line_input["configuration_file"])
        settings.update((i, x) for i, x in command_line_input.iteritems() if x is not None)#Gives "settings.update(dict)" a dict of items from "command_line_input", where x isn't None (As opposed to using "not x" which would get rid of all false values and "x!=None" which would be slightly less readable).
        self.show_frame_rate=settings["fps"]
        self.screen=pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN if settings["start_in_fullscreen"] else pygame.RESIZABLE)
        self.menu_open=True
        
    def run(self, update_once=False):
        while not update_once:
            self.update_graphics()
            #self.adjust_size()
            for event in pygame.event.get():
                keys=pygame.key.get_pressed()
                if event.type==pygame.QUIT:
                    self.quit()
                elif event.type==pygame.KEYDOWN:
                    for key, binding in self.key_bindings["down"].iteritems():
                        if keys[key]:
                            command=self.command_bindings["down"].get(binding, None)
                            if command and type(command[0])!=list:
                                command[0]()
                    if keys[pygame.K_q]:
                        self.quit()
                    elif self.in_menu and self.current_widget:
                        if keys[pygame.K_UP]:
                            self.current_widget.go_up()
                        elif keys[pygame.K_RIGHT]:
                            self.current_widget.go_right()
                        elif keys[pygame.K_DOWN]:
                            self.current_widget.go_down()
                        elif keys[pygame.K_LEFT]:
                            self.current_widget.go_left()
                if self.state=="in game":
                    self.play_game()
                if self.state=="in game" and self.player:
                    if keys[pygame.K_w]:
                        self.player.move_forward()
                    elif keys[pygame.K_w] and keys[pygame.K_d]:
                        self.player.move_forward()
                        self.player.move_right()
                    elif keys[pygame.K_w] and keys[pygame.K_a]:
                        self.player.move_forward()
                        self.player.move_left()
                    elif keys[pygame.K_s]:
                        self.player.move_back()
                    elif keys[pygame.K_d]:
                        self.player.move_back()
                        self.player.move_right()
                    elif keys[pygame.K_s] and keys[pygame.K_a]:
                        self.player.move_back()
                        self.player.move_left()
                
                elif event.type==pygame.VIDEORESIZE:
                    self.width, self.height=event.size
                    self.adjust_size()
            pygame.display.update()
            time.sleep(0.00001)
    
    def update_graphics(self):
        if self.keep_background:
            self.screen.fill(self.background_color)
        if self.show_frame_rate:
            if not self.widget_exists("fps-label"):
                self.fps_label=interface.Label("FPS...", None, (10, 255, 255), 20, (25, 15))
                self.add_widget(self.fps_label, "fps-label")
            self.fps_label.set_text("FPS: %d" %self.timer.get_fps())
        if (time.time()-self.starting_time)<=.5:#5:
            if not self.widget_exists("nickel-splash-logo"):
                pygame.mouse.set_visible(False)#Hide cursor for splash-screen.
                self.add_widget(interface.Image(storage.relative_directory("/".join(__file__.split("/")[:-1]), "images/nickel-jar-studios-logo-white.png"), (self.width*.5, self.height*.5, 200, 200)), "nickel-splash-logo")
                self.add_widget(interface.Label("Nickel Jar Studios", "Ariel", (255, 255, 255), 15, (self.width*.5, self.height*.5), True), "nickel-splash-title")
                copyright_text=interface.Label(u"Copyright © Brandan Balram, James Cowgill, Jordan Jones, Seth Nash", None, (255, 255, 255), 15, (self.width*.3, self.height*.9), True)
                copyright_text.set_position(copyright_text.dimensions()[2]*.5, self.height-copyright_text.dimensions()[3])
                self.add_widget(copyright_text, "nickel-splash-copyright")
                software_used_text=interface.Label("Created with Python, PyGame and SDL amongst other software.", None)
                software_used_text.set_position(self.width-copyright_text.dimensions()[2]*.6, software_used_text.dimensions()[3])
                self.add_widget(software_used_text, "software-used-splash-credit")
                print(pygame.mixer.Sound("sounds/coin drop.ogg").play())
                
        elif self.menu_open:
            self.remove_widget("nickel-splash-logo")
            self.remove_widget("nickel-splash-title")
            self.remove_widget("software-used-splash-credit")#Keep copyright text for the first time the menu is shown.
            self.adjust_size()
        elif self.player:
            self.play_game()
        for widget in self.widgets.values():
            widget.draw(self.screen)########
            print(self.widgets)
        self.timer.tick()
    
    def show_menu(self):
        self.set_state("start menu")
        pygame.mouse.set_visible(True)
        font=pygame.font.SysFont(None, 30)#font.render("Car Chaos", 1, (255, 255, 255))
        #self.screen.blit(game_title, (self.width/2-30, self.height/4))
        #
        if not self.widget_exists("menu-play-button"):
            self.in_menu=True
            self.update_background=True
            self.background_color=(0, 0, 255)
            self.add_widget(interface.Label("Car Chaos", "Arial", (255, 255, 255), 
                150, position=(self.width/2, self.height/4)), "game-title")
            self.add_widget(interface.Button("Play", pygame.Color(150, 150, 150, 255),
         (self.width/2-87.5, self.height*.5-25, 175, 50), self.select_level, self.widget_grabber), "menu-play-button")
            self.add_widget(interface.Button("Options", pygame.Color(150, 150, 90, 75),
         (self.width/2-87.5, self.height*.5+50, 175, 50), None, self.widget_grabber), "menu-options-button")
            self.add_widget(interface.Button("Credits", pygame.Color(150, 90, 90, 75),
         (self.width/2-87.5, self.height*.5+125, 175, 50), self.roll_credits, self.widget_grabber), "menu-credits-button")
            self.add_widget(interface.Button("Exit", pygame.Color(90, 90, 90, 75),
         (self.width/2-87.5, self.height*.5+200, 175, 50), self.quit, self.widget_grabber), "menu-exit-button")
        
    def play_game(self):
        #self.set_state("in game")
        #self.in_menu=False
        pygame.draw.rect(self.screen, (255, 255, 255), (100, 0, self.width*.5, self.height))
        self.level.update()
            
    def play_level(self, level_info=None):
        level_info=self.selected_level if not level_info else level_info#kek
        pygame.mouse.set_visible(False)
        self.clear_widgets()
        #self.keep_background=False
        self.set_state("in game")
        self.in_menu=False
        try:
            self.level=level_info.create_level()
            self.screen.fill((255, 255, 255))
            self.level.set_surface(self.screen)
            self.level.load_game()
            self.level.start()
        except level.LevelError as e:
            self.show_error(e)
    
    def select_level(self):
        self.set_state("level selector")
        pygame.mouse.set_visible(True)
        font=pygame.font.SysFont(None, 30)
        if not self.widget_exists("level-selector-text"):
            self.in_menu=True
            self.keep_background=True
            self.background_color=(255, 55, 55, .6)
            for i in self.slide_animations:
                del i
            self.slide_animations=[]
            level_selector_title=interface.Label("Select a level", "Arial")
            level_selector_title.set_position(self.width*.5, self.height*.1)
            self.add_widget(level_selector_title, "level-selector-text")
            menu_button=interface.Button("Menu", (255, 255, 255), (self.width*.1, self.height*.9, 100, 50), self.show_menu, self.widget_grabber)
            self.add_widget(menu_button, "menu-button-selector")
            self.add_widget(level_selector_title, "level-selector-text")
            load_level_button=interface.Button("Load from file", (255, 255, 255), (self.width*.2, self.height*.9, 200, 50), None, self.widget_grabber)
            self.add_widget(load_level_button, "load-button-selector")
            w=(self.width-50)/3
            floating=self.height/3
            for x, level_object in enumerate(level.load_level_info()):
                lev=deepcopy(level_object)
                image=interface.Image(os.path.join("/".join(os.path.dirname(__file__).split("/")[:-1]), lev.folder_location, lev.image), (w/3+400*x, floating, w*.75, self.height*.25), self.widget_grabber)
                slide_animation=interface.SlideAnimation(interface.LEFT, None, 2, .005)
                slide_animation.set_meta("level", lev)
                self.slide_animations.append(slide_animation)
                image.add_animation(slide_animation)
                self.add_widget(image, "level-preview-%d" %x)
                text=interface.Label(lev.title, "Arial", (255, 255, 255), 25, (w/3+400*x, floating*1.45))                  
                slide_animation=interface.SlideAnimation(interface.LEFT, None, 2, .005)
                slide_animation.set_meta("level", lev)#Set_meta just adds it to a dict
                self.slide_animations.append(slide_animation)
                text.add_animation(slide_animation)
                self.add_widget(text, "level-title-%d" %x)
            #self.add_widget(interface.Rectangle((0,0,0,.4), ((0, self.height*.5), (self.width, self.height))), "background-level-selector")
            self.play_button=interface.Button("Play", (255, 255, 255), (self.width-self.width*.35, self.height*.75, 200, 100))
            self.add_widget(self.play_button, "play-button")
            self.add_widget(interface.Button("Previous", (255, 255, 255), (self.width-self.width*.35, self.height*.9, 125, 50), lambda :[(f.set_direction(None, interface.RIGHT), f.toggle(1)) for f in self.slide_animations], self.widget_grabber), "previous-level-selector")
            self.add_widget(interface.Button("Next", (255, 255, 255), (self.width-self.width*.2, self.height*.9, 75, 50), lambda :[(f.set_direction(None, interface.LEFT), f.toggle(1)) for f in self.slide_animations], self.widget_grabber), "next-level-selector")
            self.bind_command("down", "right", lambda :[(f.set_direction(None, interface.LEFT), f.toggle(1)) for f in self.slide_animations])
            self.bind_command("down", "left", lambda :[(f.set_direction(None, interface.RIGHT), f.toggle(1)) for f in self.slide_animations])
            self.level_title=interface.Label("Level", "Arial", (255, 255, 255), 30, (self.width*.5, floating*1.6))
            self.add_widget(self.level_title, "level-title-selector")
            
        for animation in self.slide_animations:
            if 0<animation.x<self.width/3:
                text=""
                if type(animation.widget)==interface.Label:
                    text=animation.widget.text
                elif type(animation.widget)==interface.Image:
                    text=animation.widget.source
                self.level_title.set_text(text+str(id(animation.meta_data)))#Quickest way of checking without leaving the program
                self.play_button.set_text("Play "+text)
                self.selected_level=animation.meta_data["level"]
                self.play_button.set_callback(self.play_level)#Put everything on a surface so that the world can move around with the car, while not interrupting the physics.
        #if self.widgets["level-preview-0"].x>=self.width-50:#Create bounds for level instead.
        #    [f.set_direction(None, interface.RIGHT) for f in self.slide_animations]
        #elif self.widgets["level-preview-%d" %(len(self.slide_animations)-1)].x<=-50:
        #    [f.set_direction(None, interface.LEFT) for f in self.slide_animations]
                continue
        
    def quit(self):
        pygame.font.quit()
        pygame.quit()
        sys.exit()
        
    def adjust_size(self):
        start_adjustment={
            "start menu":self.show_menu,
            "in game":self.play_game,
            "level selector":self.select_level,
            "credits rolling":self.roll_credits
        }.get(self.state, self.show_menu)()
    
    def add_widget(self, widget, widget_id):
        if not self.widget_exists(widget_id) and widget:
            self.widgets[widget_id]=widget
    
    def remove_widget(self, widget_id):
        if self.widget_exists(widget_id):
            del self.widgets[widget_id]
    
    def widget_exists(self, widget_id):
        return widget_id in self.widgets
        
    def widget_grabber(self):
        return self.current_widget
        
    def clear_widgets(self):
        self.widgets.clear()
        self.widgets={}
        
    def set_state(self, state, clear_previous=True):
        if self.state!=state and clear_previous:
            self.clear_widgets()
        self.state=state
        
    def roll_credits(self):
        self.state="credits rolling"
        pygame.mouse.set_visible(False)
        middle=self.width*.5
        bottom=self.height
        if not self.widget_exists("credits-title-0"):
            self.in_menu=False
            self.keep_background=True
            self.background_color=(0, 255, 0)
            self.clear_widgets()
            for i, credit in enumerate(credits):
                self.run(True)
                credits_text=interface.Label(credit, "Ariel", (255, 255, 255), 25, (middle, bottom))
                credits_text.add_animation(interface.SlideAnimation(None, interface.UP, 2, .005, started=True))
                self.add_widget(credits_text, "credits-title-%d" %i)
                if ":" in credit:
                    bottom+=15
                else:
                    bottom+=25
        elif self.widget_exists("credits-title-22") and self.widgets["credits-title-22"].position[1]<=-50:
            self.clear_widgets()
            self.show_menu()
        
    
    def bind_command(self, state, command, call, destination=None):
        self.command_bindings[state][command]=(call, destination)
    
    def clear_commands(self):
        for group in ["down", "released", "pressed"]:
            self.command_bindings[group]=[]
    
    def show_error(error, message, severity=1):
        print("[%d]%s: %s" %(severity, str(error), message))
    
    width=640
    height=640
    fullscreen_enabled=True
    double_buffer_enabled=True
    state="off"
    widgets={}
    menu_open=True
    background_color=(0, 0, 0)
    keep_background=True
    current_widget=None
    slide_animations=[]
    key_bindings={
        "down":{
            pygame.K_RIGHT:"right",
            pygame.K_LEFT:"left"
        }
    }
    command_bindings={
        "down":{
        }
    }
    in_menu=True
    player=None
    level=None
    show_frame_rate=False
    
if __name__=="__main__":
    print("Please run from \"run.py,\" from this package's parent directory. Look for README or README.md for more details.")
