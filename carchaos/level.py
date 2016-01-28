#main: ../run.py
"""Copyright (c) 2015 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

from .levels import LevelMap, LevelRegion
from .storage import open_level_data, relative_directory

class Level():
    """Level loaded after data."""
    


def load_level_from_file(self):
    return Level()
    
class LevelInfo:
    def __init__(self, data):
        self.data=data
        self.title=data["title"]
        self.description=data["description"]
        self.image=data["image"]
        
def load_level_info():
    return [LevelInfo(directory) for directory in [
        "levels/level01/meta.json", 
        "levels/level02/meta.json", 
        "levels/level03/meta.json"
    ]]
