import sys

# Game Rules
COLUMNS = 15
ROWS = 15
CHECKERS = 12
GOAL = 4

# Logging
CALC_LOGFILE = 'calc.log'
TEAM_LOGFILE = 'teams.log'

# Design
COORDINATES = True

FIELD_BACKGROUND = 'grey'

MENU_WIDTH = 20
MENU_BACKGROUND = 'red'

QUIT_BG = 'white'
QUIT_FG = 'gold'
QUIT_HEIGHT = 3
QUIT_PADY = 10

DRAW_BG = 'CadetBlue1'

RESET_BG = 'yellow2'

SAVE_HIGHT = 5
SAVE_BG = 'green3'

DB_HEIGHT = 1
DB_WIDTH = 1
DB_PAD = 3

if sys.platform == 'win32':
    DB_WIDTH *= 2
