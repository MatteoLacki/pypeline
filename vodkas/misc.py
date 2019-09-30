from datetime import datetime
import json
import multiprocessing
from pathlib import Path


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




