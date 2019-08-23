from vodkas.apex3d import apex3d, append_apex3d_args_to_parser
from docstring_parser import parse
from pprint import pprint

x = parse(apex3d.__doc__)
w = {p.arg_name: (p.type_name , p.description) for p in x.params}
pprint(w)

w['high_energy_thr']
w['lock_mass_z2']
w['unsupported_gpu']