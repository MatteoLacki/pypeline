from datetime import datetime
import json
import multiprocessing


def get_coresNo():
	"""Detect the number of cores."""
	return multiprocessing.cpu_count()


def now():
    """Current date in format YEAR-MONTH-DAY_HOUR-MINUTE-SECOND."""
    d = datetime.now()
    return "{}-{}-{}_{}-{}-{}".format(d.year,d.month,d.day,d.hour,d.minute,d.second)


def isType(x, classes=(int,float)):
    return any(isinstance(x, t) for t in classes)


def jsonDict(d):
    return {k:v if isType(v) else repr(v) for k,v in d.items()}


def call_info(args):
    """Remove kwds (that only simplify argument passing in the wrappers)."""
    del args['kwds']
    return json.dumps(jsonDict(args))
