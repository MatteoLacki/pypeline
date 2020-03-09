%load_ext autoreload
%autoreload 2
from pprint import pprint
from collections import OrderedDict, namedtuple
import logging

from docstr2argparse.parse import FooParser
from docstr2argparse.parse import defaults, parse_google, foo2argparse

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fastas import get_fastas
from vodkas.logging import store_parameters

foos = [get_fastas, apex3d, peptide3d, iadbs]
ARG = namedtuple('ARG', 'name o_name info')



FP = FooParser(foos)
pprint(FP)

FP['iadbs']['mock'].info['action'] = "store_true"
FP['iadbs']['mock'].info['action']
FP.parse_kwds({'iadbs_mock':True, 'apex3d_cuda':True, 'iadbs_path':'~/Symp'})
FP.kwds['iadbs']
FP['iadbs']

