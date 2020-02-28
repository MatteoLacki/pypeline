%load_ext autoreload
%autoreload 2
import logging
from vodkas.logging import log_parameters
from pathlib import Path
import sys

log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename='/home/matteo/SYMPHONY_VODKAS/test.log',
                    format=log_format,
                    level=logging.INFO)
log = logging.getLogger('TEST')
# log.addHandler(logging.StreamHandler(sys.stdout))
# log = get_logger('RERUN_IADBS', log_format)
# log.info('hahaha')
# add name of the function, and time it.


def test(a, b=10, c=20, *args, **kwds):
    """hahah"""
    return a,b,c,args,kwds



test_logging = log_parameters(log)(test)
x = test_logging(10, Path('.'))
test.__name__


