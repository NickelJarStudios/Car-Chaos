#Main: ../run.py
"""Copyright (c) 2013 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
#import sqlite
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
from os import path
import json

def load_save_file(location, number):
    """Function for loading a save game file."""
    
    
def load_settings(location=None):
    global config
    config=ConfigParser()
    try:
        with open("config.cfg") as config_file:
            config.readfp(config_file)
    except IOError:
        print("No conifg.cfg found in current directory, continuing...")
    if location:
        config.read(location)
    else:
        config.read([path.realpath(path.expanduser(path.join(p))) for p in []])
    return dict(config.items("GameSettings"))
    
def relative_directory(file_location, directory):
    if directory.startswith("/"):
        return directory
    return path.join(file_location, directory)
    
def open_level_data(path):
    with open(path) as level_data:
        content=json.loads(level_data.read())
    return content
