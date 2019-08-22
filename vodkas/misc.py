import multiprocessing
from inspect import signature
from functools import wraps, update_wrapper
from pathlib import Path
import json
from datetime import datetime


def get_coresNo():
	"""Detect the number of cores."""
	return multiprocessing.cpu_count()


def catch_arguments(foo):
    """Wrap function so that it returns both the passed arguments and the value."""
    sign = signature(foo)
    @wraps(foo)
    def wrapper(*args, **kwds):
        _args = sign.bind(*args, **kwds)
        _args.apply_defaults()
        _args = dict(_args.arguments)
        _args.update(_args.pop('kwds'))
        return _args, foo(*args, **kwds)
    return wrapper


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
    def wrap(self, functions_list):
        def w(f):
            self[f.__name__] = []
            sign = signature(f)
            def wrapper(*args, **kwds):
                _args = sign.bind(*args, **kwds)
                _args.apply_defaults()
                _args = dict(_args.arguments)
                _args.update(_args.pop('kwds'))
                self[f.__name__].append(_args)
                return f(*args, **kwds)
            update_wrapper(wrapper, f)
            return wrapper
        return [w(f) for f in functions_list]


def now():
    d = datetime.now()
    return "{}-{}-{}_{}-{}-{}".format(d.year,d.month,d.day,d.hour,d.minute,d.second)


class GreatWrap(StoreWrap):
    def json(self, *output_folders):
        jetzt = now()
        for of in output_folders:
            of = Path(of)/(jetzt + ".json")
            with open(of, 'w') as f:
                json.dump(self, f, indent=4)


def store_wrap(*functions_list):
    mem = GreatWrap()
    functions_list = mem.wrap(functions_list)
    functions_list.append(mem)
    return functions_list
