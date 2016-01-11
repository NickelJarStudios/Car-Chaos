 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

from . import storage, player, level, interface, game_items
import sys
import os
import time
import re
try:
    import pygame, pygame.locals
except ImportError:
    print("""You don't have pygame installed. In order to use this application
        you must have pygame. See the README.md or README.txt file for
        instructions on how to get and install PyGame or run the installer.""")

credits=[
    "#Nickel Jar Studios",
    "",
    "Lead Programmer : Seth Nash",
    "Lead Map/Level Design : Brandan Balram",
    "Art/Sprite Picker : James T. Cowgill",
    "Database management : Jordan Jones",
    "",
    "Software Used",
    ":Python........................................................................Programming and Scripting.",
    ":SQLite.....................................................................................Database and storage.",
    ":Simple DirectMedia Layer................Visuals, Rendering, Content, Sound.",
    ":PyGame.............................................................................Python bindings to SDL.",
    "",
    "GNU Image Manipulator..............................................................Editing Images.",
    "Audacity.........................................Audio Editing, Creation and Modification."
    "",
    "#SPECIAL THANKS",
    "",
    "Fiona Nash, Emmanuel Nash, Kanye West, Jesus Christ, David Lopez, Lecrae Moore, Barack Obama"
]

class CarChaos:
    def __init__(self, command_line_input=None):
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        self.starting_time=time.time()
        self.info=pygame.display.Info()
        self.height, self.width=self.info.current_h, self.info.current_w
        if not command_line_input:
            command_line_input={}
        elif command_line_input["dimensions"]:
            command_line_input["width"], command_line_input["height"]=[int(i) for i in command_line_input["dimensions"].lower().split("x")]
            self.width, self.height=int(command_line_input["width"]), int(command_line_input["height"])
        settings=storage.load_settings(command_line_input["configuration_file"])
        settings.update((i, x) for i, x in command_line_input.iteritems() if x is not None)#Gives "settings.update(dict)" a dict of items from "command_line_input", where x isn't None (As opposed to using "not x" which would get rid of all false values and "x!=None" which would be slightly less readable).
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
        pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.height))
        if (time.time()-self.starting_time)<=.5:#5:
            if not self.widget_exists("nickel-splash-logo"):
                pygame.mouse.set_visible(False)#Hide cursor for splash-screen.
                self.add_widget(interface.Image(os.path.join("/".join(__file__.split("/")[:-1]), "images/nickel-jar-studios-logo-white.png"), (self.width*.5, self.height*.5, 200, 200)), "nickel-splash-logo")
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
            widget.draw(self.screen)
    
    def show_menu(self):
        self.set_state("start menu")
        self.in_menu=True
        self.background_color=(0, 0, 255)
        pygame.mouse.set_visible(True)
        font=pygame.font.SysFont(None, 30)#font.render("Car Chaos", 1, (255, 255, 255))
        #self.screen.blit(game_title, (self.width/2-30, self.height/4))
        #
        if not self.widget_exists("menu-play-button"):
            self.add_widget(interface.Label("Car Chaos", "Arial", (255, 255, 255), 
                150, position=(self.width/2, self.height/4)), "game-title")
            self.add_widget(interface.Button("Play", pygame.Color(90, 90, 90, 75),
         (self.width/2-87.5, self.height*.5-25, 175, 50), self.select_level, self.widget_grabber), "menu-play-button")
            self.add_widget(interface.Button("Options", pygame.Color(90, 90, 90, 75),
         (self.width/2-87.5, self.height*.5+50, 175, 50), None, self.widget_grabber), "menu-options-button")
            self.add_widget(interface.Button("Credits", pygame.Color(90, 90, 90, 75),
         (self.width/2-87.5, self.height*.5+125, 175, 50), self.roll_credits, self.widget_grabber), "menu-credits-button")
            self.add_widget(interface.Button("Exit", pygame.Color(90, 90, 90, 75),
         (self.width/2-87.5, self.height*.5+200, 175, 50), self.quit, self.widget_grabber), "menu-exit-button")
        
    def play_game(self):
        self.set_state("in game")
        self.in_menu=False
        if self.player and self.level:
            print(list(reversed(self.player.position())))
            self.screen.blit(self.player.image, tuple(reversed(self.player.position())))
        else:
            self.level=game_items.LevelOne()
            self.player=self.level.create_player()
            
    def select_level(self):
        self.set_state("level selector")
        self.in_menu=True
        self.background_color=(255, 255, 0)
        pygame.mouse.set_visible(True)
        font=pygame.font.SysFont(None, 30)
        level_selector_title=interface.Label("Select a level", "Arial")
        level_selector_title.set_position(self.width*.5, self.height*.1)
        self.add_widget(level_selector_title, "level-selector-text")
        menu_button=interface.Button("Menu", (255, 255, 255), (self.width*.1, self.height*.9, 100, 50), self.show_menu, self.window_grabber)
        self.add_widget(menu_button, "menu-button-selector")
        
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
        
    def set_state(self, state, clear_previous=True):
        if self.state!=state and clear_previous:
            self.clear_widgets()
        self.state=state
        
    def roll_credits(self):
        self.in_menu=False
        self.state="credits rolling"
        pygame.mouse.set_visible(False)
        middle=self.width*.5
        bottom=self.height
        if not self.widget_exists("credits-title-0"):
            self.background_color=(0, 0, 0)
            self.clear_widgets()
            for i, credit in enumerate(credits):
                self.run(True)
                credits_text=interface.Label(credit, "Ariel", (255, 255, 255), 20, (middle, bottom))
                credits_text.add_animation(interface.SlideAnimation(None, interface.UP, 2, .01))
                self.add_widget(credits_text, "credits-title-%d" %i)
                if ":" in credit:
                    bottom+=15
                else:
                    bottom+=25
                print("lel"+", ".join(self.widgets.keys()))
        elif self.widget_exists("credits-title-4") and self.widgets["credits-title-4"].position[1]<=50:
            self.clear_widgets()
            self.show_menu()
        
    
    width=640
    height=640
    fullscreen_enabled=True
    double_buffer_enabled=True
    state="off"
    widgets={}
    menu_open=True
    background_color=(0, 0, 0)
    current_widget=None
    in_menu=True
    player=None
    level=None
    
if __name__=="__main__":
    print("Please run from \"run.py,\" from this package's parent directory. Look for README or README.md for more details.")
