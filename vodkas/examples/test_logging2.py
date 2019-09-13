from vodkas.examples.test_logging import apex3d

from functools import wraps
from inspect import getcallargs, getargspec
from collections import OrderedDict, Iterable
from itertools import *
import logging

def flatten(l):
    """Flatten a list (or other iterable) recursively"""
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def getargnames(func):
    """Return an iterator over all arg names, including nested arg names and varargs.
    Goes in the order of the functions argspec, with varargs and
    keyword args last if present."""
    (argnames, varargname, kwargname, _) = getargspec(func)
    return chain(flatten(argnames), ifilter(None, [varargname, kwargname]))

def getcallargs_ordered(func, *args, **kwargs):
    """Return an OrderedDict of all arguments to a function.
    Items are ordered by the function's argspec."""
    argdict = getcallargs(func, *args, **kwargs)
    return OrderedDict((name, argdict[name]) for name in getargnames(func))

def describe_call(func, *args, **kwargs):
    yield "Calling %s with args:" % func.__name__
    for argname, argvalue in getcallargs_ordered(func, *args, **kwargs).iteritems():
        yield "\t%s = %s" % (argname, repr(argvalue))

def log_to(logger_func):
    """A decorator to log every call to function (function name and arg values).
    logger_func should be a function that accepts a string and logs it
    somewhere. The default is logging.debug.
    If logger_func is None, then the resulting decorator does nothing.
    This is much more efficient than providing a no-op logger
    function: @log_to(lambda x: None).
    """
    if logger_func is not None:
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for line in describe_call(func, *args, **kwargs):
                    logger_func(line)
                return func(*args, **kwargs)
            return wrapper
    else:
        decorator = lambda x: x
    return decorator

logdebug = log_to(logging.debug)
apex3d = logdebug(apex3d)
logging.basicConfig(level=logging.INFO, filename='test.log')


apex3d('a', 'b')
import signature
signature(apex3d)