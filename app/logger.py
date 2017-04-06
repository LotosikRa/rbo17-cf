import logging
from settings import ALGO_LOGFILE


logging.basicConfig(filename=ALGO_LOGFILE,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s :: %(message)s')
