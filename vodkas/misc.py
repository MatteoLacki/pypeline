import argparse
import builtins
from datetime import datetime
from functools import wraps, update_wrapper
from inspect import signature
import json
import multiprocessing
from pathlib import Path
from time import time

def get_coresNo():
	"""Detect the number of cores."""
	return multiprocessing.cpu_count()


def catch_arguments(foo):
    """Wrap function so that it returns both the passed arguments and the value."""
    storage = []
    sign = signature(foo)
    @wraps(foo)
    def wrapper(*args, **kwds):
        _args = sign.bind(*args, **kwds)
        _args.apply_defaults()
        _args = dict(_args.arguments)
        _args.update(_args.pop('kwds', {}))
        storage.append(_args)
        return foo(*args, **kwds)
    return wrapper, storage


def store_args(storage):
    """Wrap function so that it returns both the passed arguments and the value."""
    def outer_wrapper(foo):
        sign = signature(foo)
        @wraps(foo)
        def wrapper(*args, **kwds):
            _args = sign.bind(*args, **kwds)
            _args.apply_defaults()
            _args = dict(_args.arguments)
            _args.update(_args.pop('kwds'))
            storage[foo.__name__] = _args
            return foo(*args, **kwds)
        return wrapper
    return outer_wrapper


class StoreWrap(dict):
    """Store the state of function calls."""
    def wrap(self, functions):
        """Wrap functions.

        Args:
            functions (list): some functions to wrap.

        Returns:
            list of wrapped functions."""
        def w(f):
            self[f.__name__] = []
            sign = signature(f)
            def wrapper(*args, **kwds):
                _args = sign.bind(*args, **kwds)
                _args.apply_defaults()
                _args = dict(_args.arguments)
                _args.update(_args.pop('kwds'))
                _args = {k:repr(v) for k,v in _args.items()}
                self[f.__name__].append(_args)
                return f(*args, **kwds)
            update_wrapper(wrapper, f)
            return wrapper
        return [w(f) for f in functions]


def now():
    """Current date in format YEAR-MONTH-DAY_HOUR-MINUTE-SECOND."""
    d = datetime.now()
    return "{}-{}-{}_{}-{}-{}".format(d.year,d.month,d.day,d.hour,d.minute,d.second)


# this might be reinventing the bloody logging.
class FuncState(dict):
    """Store the initial state of function calls and their timing."""
    def wrap(self, functions):
        """Wrap functions.

        Args:
            functions (list): some functions to wrap.

        Returns:
            list of wrapped functions."""
        def w(f):
            self[f.__name__] = []
            sign = signature(f)
            def wrapper(*args, **kwds):
                _args = sign.bind(*args, **kwds)
                _args.apply_defaults()
                _args = dict(_args.arguments)
                _args.update(_args.pop('kwds'))
                self[f.__name__].append(_args)
                t0 = time()
                r = f(*args, **kwds)
                t1 = time()
                self[f.__name__][-1]['__runtime__'] = t1 - t0
                return r
            update_wrapper(wrapper, f)
            return wrapper
        return [w(f) for f in functions]

    def json(self,
             logs_folder='C:/SYMPHONY_VODKAS/temp_logs',
             logs_server_folder = 'X:/SYMPHONY_VODKAS/temp_logs',
             log_prefix='',
             **kwds):
        """Dump function calls to jsons locally and on server.

        Args:
            logs_folder (str): Path to the folder storing locally the logs.
            logs_server_folder (str): Path to the folder storing remotely the logs.
            log_prefix (str): prefix to the names of the output logs.
            kwds: other arguments.
        """
        jetzt = now()
        for of in (logs_folder, logs_server_folder):
            of = Path(of)/(log_prefix + jetzt + ".json")
            with open(of, 'w') as f:
                json.dump(self, f, indent=4)




def monitor(*functions):
    """Get information on function call of enumerated functions.

    Args:
        *functions: some functions to wrap.

    Returns:
        The same functions followed by a storage dictionary."""
    mem = FuncState()
    functions = mem.wrap(functions)
    functions.append(mem)
    return functions
