import logging as lg
from settings import CALC_LOGFILE, TEAM_LOGFILE


# Calculator logger
calc_lg = lg.getLogger('Calculates')
calc_lg.setLevel(lg.INFO)
calc_file_handler = lg.FileHandler(CALC_LOGFILE, mode='a')
calc_file_handler.setLevel(lg.INFO)
calc_file_handler.setFormatter(lg.Formatter(fmt='%(asctime)s - %(levelname)s :: %(message)s'))
calc_lg.addHandler(calc_file_handler)

# Team logger
team_lg = lg.getLogger('Teams')
team_lg.setLevel(lg.INFO)
team_file_handler = lg.FileHandler(TEAM_LOGFILE, mode='a')
team_file_handler.setLevel(lg.INFO)
team_file_handler.setFormatter(lg.Formatter(fmt='%(asctime)s - %(message)s',
                                            datefmt='%H:%M'))
team_lg.addHandler(team_file_handler)
