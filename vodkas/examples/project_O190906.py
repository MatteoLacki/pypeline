r"""Sabine's project.

\\MSSERVER\obelix_rawdata\RAW\O1909
File names O190906_02 to _26


X:\SYMPHONY_VODKAS\fastas\custom\horny_mouse\20180515_up_mouse_reviewed_16970entries_and_171contaminants+hNECAB1+2_reverese.fasta
"""
import logging
from pathlib import Path
from pprint import pprint

from vodkas import plgs
from vodkas.misc import get_task_no

fastas = Path(r"X:/SYMPHONY_VODKAS/fastas/custom/horny_mouse/20180515_up_mouse_reviewed_16970entries_and_171contaminants+hNECAB1+2_reverese.fasta")
raw_folder = Path(r"O:/RAW/O1909/O190906_06.raw")
out_folder = Path(r"C:/SYMPHONY_VODKAS/temp/debug/O190906_06")
log_file = Path(r"C:/SYMPHONY_VODKAS/temp/debug/debug.log")
TASK_NO = get_task_no(log_file)

logging.basicConfig(filename=log_file,
                    format=f'{TASK_NO} %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = logging.getLogger('Debug')

try:
	plgs(raw_folder, out_folder, fastas=fastas)
except KeyboardInterrupt:
	print("Interrupted")
	logger.critical('YOU INTERRUPTED ME')

# logger parser.



