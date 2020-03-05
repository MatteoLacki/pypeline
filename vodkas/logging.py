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


class MockLog():
    def info(self, *args, **kwds):
        print(*args, **kwds)

class MockSender():
    def log(self, *args, **kwds):
        print(*args, **kwds)


def store_parameters(log=MockLog(), sender=MockSender()):
    """Store parameters of a function."""
    def wrapping(foo, 
                 store_input=True, 
                 store_runtime=True,
                 store_output=True):
        if store_input:
            sig = inspect.signature(foo)
            default_args = defaults(foo)
            default_args['__name__'] = foo.__name__
        @wraps(foo)
        def wrapper(*args, **kwds):
            log.info(f"Logging {foo.__name__}. Input: {store_input}. Runtime: {store_runtime}. Output: {store_output}.")
            if store_input:
                all_args = default_args.copy()
                all_args.update(sig.bind(*args,**kwds).arguments)
                log.info(dump2json(all_args))
            T0 = time()
            res = foo(*args, **kwds)
            T1 = time()
            if store_runtime:
                log.info(f"{foo.__name__} took: {T1-T0}")
            if store_output:
                log.info(dump2json(res))
            return res
        return wrapper
    return wrapping
