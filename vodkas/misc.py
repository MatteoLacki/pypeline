import multiprocessing
from inspect import signature
from functools import wraps, update_wrapper
from pathlib import Path
import json
from datetime import datetime
import builtins
import argparse


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
                self[f.__name__].append(_args)
                return f(*args, **kwds)
            update_wrapper(wrapper, f)
            return wrapper
        return [w(f) for f in functions]


def now():
    """Current date in format YEAR-MONTH-DAY_HOUR-MINUTE-SECOND."""
    d = datetime.now()
    return "{}-{}-{}_{}-{}-{}".format(d.year,d.month,d.day,d.hour,d.minute,d.second)


class GreatWrap(StoreWrap):
    """Is to StoreWrap as Great Gatsby was to mere Gatsby."""
    def json(self, *output_folders):
        jetzt = now()
        for of in output_folders:
            of = Path(of)/(jetzt + ".json")
            with open(of, 'w') as f:
                json.dump(self, f, indent=4)


def store_wrap(*functions):
    """Add to functions a storage for the arguments they were called with.

    Args:
        *functions: some functions to wrap.

    Returns:
        The same functions followed by a storage dictionary."""
    mem = GreatWrap()
    functions = mem.wrap(functions)
    functions.append(mem)
    return functions


def create_parser(parsed_doc, description=''):
    """Create a new parser based on the parsed_doc"""
    if not description:
        description = parsed_doc.short_description
    return argparse.ArgumentParser(description=description)


def add_args(parsed_doc, parser):
    """Add parsed parameters to the CLI (arg)parser."""
    for p in parsed_doc.params:
        try:
            _type = getattr(builtins, p.type)
            parser.add_argument(p.arg_name, type=_type, help=p.description)
        except AttributeError:
            parser.add_argument(p.arg_name, help=p.description)
