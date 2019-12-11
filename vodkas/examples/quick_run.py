"""Quick test project.
"""
import logging
from pathlib import Path

from vodkas import plgs, get_fastas
from vodkas.logging import get_task_no, get_logger

fastas = get_fastas('human')
raw_folder = Path(r"X:/SYMPHONY_VODKAS/standard_data/O190302_01.raw")
out_folder = Path(r"C:/SYMPHONY_VODKAS/temp/debug/O190302_01")

log_file = Path(r"C:/SYMPHONY_VODKAS/temp/debug/debug.log")
task_no = get_task_no(log_file)
log_format = f'{task_no} %(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=log_file, format=log_format, level=logging.INFO)
logger = get_logger('Debug', log_format, logging.INFO)

try:
	plgs(raw_folder, out_folder, fastas=fastas)
except KeyboardInterrupt:
	logger.critical('YOU INTERRUPTED ME')


task_no += 1
log_format = f'{task_no} %(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logger = get_logger('Debug', log_format, logging.INFO)

try:
	plgs(raw_folder, out_folder, fastas=fastas)
except KeyboardInterrupt:
	logger.critical('YOU INTERRUPTED ME')
