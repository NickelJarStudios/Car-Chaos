#!/usr/bin/env python
"""Copyright (c) 2013 Nash
http://slackingsource.wordpress.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
from carchaos import CarChaos
from argparse import ArgumentParser, FileType

if __name__=="__main__":
    argument_parser=ArgumentParser(prog="carchaos", add_help=True)
    argument_parser.add_argument("-w", "--windowed", dest="start_in_fullscreen", action="store_false", help="Set Windowed, as opposed to fullscreen.")
    argument_parser.add_argument("-f", "--fullscreen", dest="start_in_fullscreen", default=True, action="store_true", help="Sets fullscreen. Unless configured otherwise, enabled by default")
    argument_parser.add_argument("-d", "--dimensions", default=None, help="Sets width and height WxH.")#fullscreen
    argument_parser.add_argument("-c", "--configuration-file", default=None, type=FileType, help="Sets an alternate configuration file to use instead of the default.")
    argument_parser.add_argument("--fps", action="store_true", help="Shows the FPS (frames per second) in the top-left corner as the game is running.")
    arguments=vars(argument_parser.parse_args())#sys.argv will be used by default, so no need to specify.
    CarChaos(arguments).run()
else:
    print("Why did you import this?")
