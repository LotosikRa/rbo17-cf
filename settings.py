import sys

# Game Rules
COLUMNS = 15
ROWS = 15
CHECKERS = 12
GOAL = 4

# Logging
ALGO_LOGFILE = 'algo.log'

# Design
COORDINATES = False
if sys.platform == 'win32':
    HEIGHT = 1
    WIDTH = 2
else:
    HEIGHT = 2
    WIDTH = 2
