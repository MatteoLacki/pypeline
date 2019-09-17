from pathlib import Path
from pprint import pprint

l = lambda x: list(x.glob('*'))

PP = Path("/mnt/ms/obelix_rawdata/ARCHIVIERT")
PP = Path("/mnt/ms/idefix_rawdata/ARCHIVIERT")
big_folders = [p for p in PP.glob('*') if p.is_dir()]

def are_header_files_all_there(P):
    folders_with_header_txt = {p.parent.name for p in P.glob("*/_HEADER.txt")}
    all_folders = {p.name for p in P.glob('*') if p.is_dir()}
    return folders_with_header_txt == all_folders

for P in big_folders:
    if not are_header_files_all_there(P):
        for p in P.glob('*'):
            if not (p/"_HEADER.txt").is_file():
                pprint(l(p))

from vodkas.header_txt import parse_header_txt
p = Path("/mnt/ms/idefix_rawdata/ARCHIVIERT/I1903/I190301_01.raw/_HEADER.TXT")
d = parse_header_txt(p)
d['Acquired Name']


# consistency check 