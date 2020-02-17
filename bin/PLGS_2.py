import argparse
from pprint import pprint
from pathlib import Path

from vodkas import plgs
from vodkas.plgs import parse_optional_plgs_args
from vodkas.fs import find_free_path, move_folder

DEBUG = True
net_folder = 'Y:/TESTRES' if DEBUG else 'Y:/RES'


plgs_desc, plgs_args, arg2foo = parse_optional_plgs_args()
ap = argparse.ArgumentParser(description=plgs_desc)
ap.add_argument('raw_folders',
                type=Path,
                nargs='+',
                help='Path(s) to raw folder(s).')
ap.add_argument('--temp_folder',
                type=Path,
                help='Path to temporary outcome folder.',
                default='C:/SYMPHONY_VODKAS/temp')
ap.add_argument('--log_file',
                type=Path,
                help='Path to temporary outcome folder.',
                default='C:/SYMPHONY_VODKAS/temp_logs/plgs.log')
ap.add_argument('--net_folder',
                type=Path,
                help=f"Network folder for results. Set to '' (empty word) if you want to skip copying [default = {net_folder}].",
                default=net_folder)

for n,h in plgs_args:
    ap.add_argument(n,**h)
args = ap.parse_args().__dict__

from collections import defaultdict
args_sep = defaultdict(dict)
for p, (f, o) in arg2foo.items():
    args_sep[f+'_kwds'][o] = args[p]


print(args['raw_folders'])
print(args['temp_folder'])
pprint(args_sep)
pprint(args)
