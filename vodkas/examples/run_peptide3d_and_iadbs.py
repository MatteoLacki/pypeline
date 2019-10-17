from vodkas import peptide3d, iadbs
from vodkas.fastas import get_fastas
from vodkas import
from pathlib import Path

from vodkas.xml_parser import create_params_file

p = Path(r'C:\SYMPHONY_VODKAS\temp\2019-095\O190920_21')
a = p/'O190920_21_Apex3D.bin'
o, _ = peptide3d(a, p)

fastas = get_fastas('human')
i, _ = iadbs(o.with_suffix('.xml'), p, fastas)

create_params_file(a, o, i)
