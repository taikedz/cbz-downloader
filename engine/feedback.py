import sys
import os

""" Whether to print debug messages"""
debug_mode = False

def breakpoint(message):
    """Stop execution and display a message
    
    Requires debug_mode to be on
    """
    if not debug_mode:
        return

    feedback(message + " [<enter> or 'quit']> ", "35;1", end='')
    response = sys.stdin.readline().strip()

    if response == "quit":
        sys.exit(255)

def fail(message, code=1):
    """ Display red error message, and exit the program with status code
    """
    error(message)
    sys.exit(code)

def error(message):
    """ Display red message
    """
    feedback(message, "31;1")

def warn(message):
    """ Display yellow message
    """
    feedback(message, "33;1")

def info(message):
    """ Display green message
    """
    feedback(message, "32;1")

def debug(message):
    """ If debug mode is on, display blue message
    """
    if debug_mode:
        feedback(message, "34")

def feedback(message, colortag=None, stream=sys.stderr, end=os.linesep):
    """ Convenience function to print messages with an color code specification, by default to stderr
    """
    colorstring = ""
    colornull = ""
    if colortag != None:
        colorstring = "\033[%sm"%colortag
        colornull = "\033[0m"

    print(colorstring, end='' , file=stream)
    print(message    , end='' , file=stream)
    print(colornull  , end=end, file=stream, flush=True)
