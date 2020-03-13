from datetime import datetime
import json
import multiprocessing
from pathlib import Path
import inspect


def get_coresNo():
	"""Detect the number of cores."""
	return multiprocessing.cpu_count()


def now():
    """Current date in format YEAR-MONTH-DAY_HOUR-MINUTE-SECOND."""
    d = datetime.now()
    return "{}-{}-{}_{}-{}-{}".format(d.year,d.month,d.day,d.hour,d.minute,d.second)


def isType(x, classes=(int,float)):
    return any(isinstance(x, t) for t in classes)


def store_value(v):
    if isType(v, (int,float)):
        return v
    if isinstance(v, Path):
        return str(v)
    return repr(v)


def jsonDict(d):
    return {k:store_value(v) for k,v in d.items()}


def call_info(args):
    """Remove kwds (that only simplify argument passing in the wrappers)."""
    del args['kwds']
    return json.dumps(jsonDict(args))


def get_defaults(foo):
    """Get default settings to parameters of a function.

    Arguments:
        foo (function): A function to study.
    Returns:
        dict: mapping argument-default
    """
    s = inspect.signature(foo)
    return {a:v.default for a, v in s.parameters.items() if v.default is not inspect.Parameter.empty}


def test_get_defaults():
    def foo(a, b, c=10, d=23):
        pass
    assert get_defaults(foo) == {'c':10, 'd':23}

    def foo2(a, b, c=10, d=23, *args, **kwds):
        pass
    assert get_defaults(foo2) == {'c':10, 'd':23}


def prompt_timeout(algo, default=180):
        print(f"{algo} default = {default}")
        try:
            out = int(input('Enter a better value, or hit ENTER: '))
            if out == 0:
                print(f"Mocking {algo}.")
            if out < 0:
                print(f"Not running {algo}.")
            print()
            return out 
        except ValueError:
            print(f'Using default = {default} minutes.')
            print()
            return default