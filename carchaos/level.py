#main: ../run.py
"""Copyright (c) 2015 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

from .levels import LevelMap, LevelRegion
from .storage import open_level_data, relative_directory, get_levels_directory
import imp
import os
from pygame import Surface

class LevelError(Exception):
    """When there is an issue with the level, you use this, homie."""

class Level():
    """Level loaded after data."""
    def __init__(self, level_info, directory):
        self.surface=Surface((self.x, self.y))
        self.level_info=level_info
        self.name=level_info.data["module"]
        self.directory=directory
        self.path=os.path.join(directory, level_info.data["main-file"])
        self.started=False
        self.level_play=None
        self.resources=vars(level_info.data["resources"])
        self.level_content={}
        
    def load_game(self):
        self.module=imp.load_source(self.name, self.path)
        
    def start(self):
        self.started=True
        try:
            self.level_play=self.module.start_level(self, [])
        except AttributeError:
            if not self.module:
                raise LevelError("Module not loaded.")
            else:
                raise LevelError("The game file is not properly created.")
    
    def update(self):
        if self.level_play and self.started:
            self.level_play.update()
    
    def set_surface(self, surface):
        self.surface=surface
        
    def set_content(self, content):
        self.level_content=content
        
    def add_content(self, key, value):
        self.level_content[key]=value
        
    def get_content(self, key):
        return self.level_content[key]
        
    def delete_content(self, key):
        del self.level_content[key]
    x, y, width, height=0, 0, 1000, 1000
    
class LevelInfo:
    def __init__(self, data, location):
        self.data=data
        self.title=data["title"]
        self.description=data["description"]
        self.image=data["image"]
        self.folder_location=location
        self.level=None
        
    def set_folder_location(self, location):
        self.folder_location=location
    
    def create_level(self):
        self.level=Level(self, self.folder_location, self.resources)
        return self.level
    folder_location=os.path.join(get_levels_directory(), "/levels/")
        

def load_level_from_file(self):
    return Level()
    
def load_level_info():
    levels=[]
    for directory in ["level01/meta.json", "level02/meta.json", "level03/meta.json"]:
        try:
            levels.append(LevelInfo(open_level_data(relative_directory("/".join(__file__.split("/")[:-2])+"/levels", directory)), os.path.join(get_levels_directory(), "/".join(directory.split("/")[:-1]))))
        except IOError:
            print("Failed to load level: "+directory)#Add an error message.
    return levels
