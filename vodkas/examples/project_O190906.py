r"""Sabine's project.

\\MSSERVER\obelix_rawdata\RAW\O1909
File names O190906_02 to _26

C:\SYMPHONY_VODKAS\temp\2019-080

X:\SYMPHONY_VODKAS\fastas\custom\horny_mouse\20180515_up_mouse_reviewed_16970entries_and_171contaminants+hNECAB1+2_reverese.fasta
"""
import logging
from pathlib import Path
from pprint import pprint

from vodkas import plgs
from vodkas.logging import get_logger

fastas = Path(r"X:/SYMPHONY_VODKAS/fastas/custom/horny_mouse/20180515_up_mouse_reviewed_16970entries_and_171contaminants+hNECAB1+2_reverese.fasta")
raw_folder = Path(r"O:/RAW/O1909/O190906_06.raw")
out_folder = Path(r"C:/SYMPHONY_VODKAS/temp/debug/O190906_06")


log_file = Path(r"C:/SYMPHONY_VODKAS/temp/debug/debug.log")
logging.basicConfig(filename=log_file, level=logging.INFO)
logger = get_logger(log_file)


TASK_NO = get_task_no(log_path)

try:
	plgs(raw_folder, out_folder, fastas=fastas)
except KeyboardInterrupt:
	print("Interrupted")
	logger.critical('YOU INTERRUPTED ME')

# logger parser.



