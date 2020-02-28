from functools import wraps
import inspect
import logging
from pathlib import Path
import sys
from time import time

from docstr2argparse.parse import defaults

from .json import dump2json


def get_task_no(log_file):
    """Parse the log file to get the task number."""
    log_file = Path(log_file)
    try:
        with log_file.open('r') as f:
            for l in f:
                pass
        return int(l.split(' ')[0]) + 1
    except (ValueError, FileNotFoundError):
        return 0


# TO DO: add possibility to dump to some DB.
# def get_logger(log_path, level=logging.INFO):
#     """Get a custom logger.

#     Args:
#         log_path (str): The path for the logger.
#         level (int): The code for log improtance.

#     Returns:
#         logging.logger: a custom logger.
#     """
#     log_path = Path(log_path)
#     logger_name = log_path.stem
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)
#     TASK_NO = get_task_no(log_path)
#     format_string = f'{TASK_NO} %(asctime)s:%(name)s:%(levelname)s:%(message)s:'
#     log_format = logging.Formatter(format_string)
#     # Creating and adding the console handler
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(log_format)
#     logger.addHandler(console_handler)
#     # Creating and adding the file handler
#     file_handler = logging.FileHandler(log_path, mode='a')
#     file_handler.setFormatter(log_format)
#     logger.addHandler(file_handler)
#     return logger

def get_logger(name, format='', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)
    if format:
        logging.Formatter(format)
        log_format = logging.Formatter(format)
    return logger


def get_plgs_format(task_no):
    return f'{TASK_NO} %(asctime)s:%(name)s:%(levelname)s:%(message)s:'


def __print_out_params(f):
    """Print out parameters that f is called with: test function."""
    sig = inspect.signature(f)
    def wrapped(*args, **kwds):
        all_args = defaults(f)
        all_args.update(sig.bind(*args, **kwds).arguments)
        print(all_args)
        return f(*args, **kwds)
    return wrapped


def log_parameters(log):
    """Log parameters of a function."""
    def wrapping(foo):
        sig = inspect.signature(foo)
        default_args = defaults(foo)
        default_args['__name__'] = foo.__name__
        @wraps(foo)
        def wrapper(*args, **kwds):
            all_args = default_args.copy()
            all_args.update(sig.bind(*args,**kwds).arguments)
            log.info(dump2json(all_args))
            T0 = time()
            res = foo(*args, **kwds)
            T1 = time()
            log.info(f"{foo.__name__} took: {T1-T0}")
            return res
        return wrapper
    return wrapping
