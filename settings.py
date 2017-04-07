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
MENU_WIDTH = 15
QUIT_BG = 'gold'
QUIT_FG = 'red'
CALCULATE_BG = 'green3'
CALCULATE_HIGHT = 10
RESET_BG = 'yellow2'
if sys.platform == 'win32':
    HEIGHT = 1
    WIDTH = 2
else:
    HEIGHT = 2
    WIDTH = 2
