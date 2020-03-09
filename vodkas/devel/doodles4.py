%load_ext autoreload
%autoreload 2
from pprint import pprint
from collections import OrderedDict, namedtuple, defaultdict

from docstr2argparse.parse import ParserDisambuigationComplex
from docstr2argparse.parse import defaults, parse_google, foo2argparse

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fastas import get_fastas


foos = [get_fastas, apex3d, peptide3d, iadbs]
ARG = namedtuple('ARG', 'name o_name info')

class FooParser(object):
    def __init__(self, foos):
        foo2args = OrderedDict()
        for foo in foos:
            args = foo2argparse(foo, 
                                get_short=False,
                                positional=False,
                                args_prefix= foo.__name__+'_')
            foo2args[foo.__name__] = OrderedDict((o, ARG(n,o,h)) for n,o,h in args)
        self.foo2args = foo2args

    def modify_infos(self, mod_list):
        for foo, arg, info_field, info_field_value in mod_list:
            self.foo2args[foo][arg].info[info_field] = info_field_value
    
    def __getitem__(self, x):
        return self.foo2args[x[0]][x[1]].info[x[2]]

    def __setitem__(self, x, y):
        self.foo2args[x[0]][x[1]].info[x[2]] = y

    def parse(self, parsed_args_dict):
        parsed = defaultdict(dict)
        for arg, val in parsed_args_dict.items():
            foo, o_name = arg.split('_', 1)
            if foo in self.foo2args and o_name in self.foo2args[foo]:
                parsed[foo][o_name] = val
        return dict(parsed)              

    def print(self):
        pprint(self.foo2args)        

FP = FooParser(foos)
FP['iadbs','mock','action'] = "store_true"
FP['iadbs','mock','action']

fp = FP.parse({'iadbs_mock':True, 'apex3d_cuda':True, 'iadbs_path':'~/Symp'})
fp['iadbs']
