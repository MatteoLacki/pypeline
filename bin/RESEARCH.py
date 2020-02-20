import argparse
from docstr2argparse.parse import foo2argparse
from pathlib import Path

from vodkas import iadbs
from vodkas.fastas import get_fastas

ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*iaDBs_worflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)

for n,_,h in foo2argparse(get_fastas)[1]:
    ap.add_argument(n, **h)

ap.add_argument('raw_folders', type=Path, nargs='+',
                help='Path(s) to raw folder(s).')  
_, params = foo2argparse(iadbs)
for n,o,h in params:
    if n[:2] == '--': # optional argument
        ap.add_argument(n,**h)

args = ap.parse_args()
print(args.__dict__)

try:
    fastas = get_fastas(args.fastas_path)
except FileNotFoundError:
    log.error(f"Fastas unreachable: {fastas}")
    exit()






