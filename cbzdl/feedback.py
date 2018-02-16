import sys
import os

debug_mode = False
breakpoints = False

def breakpoint(message):
    if not debug_mode:
        return
    if not breakpoints:
        return

    feedback(message + " [<enter> or 'quit']> ", "35;1", end='')
    response = sys.stdin.readline().strip()

    if response == "quit":
        sys.exit(255)

def fail(message, code=1):
    error(message)
    sys.exit(code)

def error(message):
    feedback(message, "31;1")

def warn(message):
    feedback(message, "33;1")

def info(message):
    feedback(message, "32;1")

def debug(message):
    if debug_mode:
        feedback(message, "34")

def feedback(message, colortag, stream=sys.stderr, end=os.linesep):
    print("\033[%sm"%colortag, end='', file=stream)
    print(message, end='', file=stream)
    print("\033[0m", file=stream, end=end, flush=True)
