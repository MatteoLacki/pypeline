r"""Quick test project.
"""
import logging
from pathlib import Path

from vodkas import plgs, get_fastas
from vodkas.misc import get_task_no

fastas = get_fastas('human')
raw_folder = Path(r"X:/SYMPHONY_VODKAS/standard_data/O190302_01.raw")
out_folder = Path(r"C:/SYMPHONY_VODKAS/temp/debug/O190302_01")
log_file = Path(r"C:/SYMPHONY_VODKAS/temp/debug/debug.log")

TASK_NO = get_task_no(log_file)
logging.basicConfig(filename=log_file,
                    format=f'{TASK_NO} %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = logging.getLogger('Debug')

try:
	plgs(raw_folder, out_folder, fastas=fastas)
except KeyboardInterrupt:
	logger.critical('YOU INTERRUPTED ME')


