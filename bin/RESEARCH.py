import argparse
from docstr2argparse.parse import foo2argparse
import logging
from pathlib import Path
import platform
from pprint import pprint
import json

from fs_ops.paths import find_suffixed_files

from vodkas.fastas import get_fastas
from vodkas.iadbs import iadbs
from vodkas.logging import get_logger
from vodkas.research import research


ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('--log_file', type=lambda p: Path(p).expanduser().resolve(),
                help='Path to temporary outcome folder.',
                default={"Windows": 'C:/SYMPHONY_VODKAS/temp_logs/research.log',
                         "Linux":   '~/SYMPHONY_VODKAS/research.log',
                         "Darwin":  '~/SYMPHONY_VODKAS/research.log'}[platform.system()])
ap.add_argument('--server_ip', type=str, help='IP of the server', default='0.0.0.0')
for n,o,h in foo2argparse(get_fastas, get_short=False):
    ap.add_argument(n, **h)
ap.add_argument('Pep3D_Spectrum',
                type=Path,
                nargs='+',
                help="Path(s) to outputs of Peptide3D. If provided with a folder instead, a recursive search for files matching '*_Pep3D_Spectrum.xml' is performed.")
iadbs_kwds = foo2argparse(iadbs, args_prefix='iadbs_', positional=False, get_short=False)
for n,o,h in iadbs_kwds:
    ap.add_argument('--iadbs_'+o,**h)
args = ap.parse_args()
iadbs_kwds = {o: args.__dict__[n.replace('--','')] for n,o,h in iadbs_kwds}

log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=args.log_file, format=log_format, level=logging.INFO)
log = get_logger('RERUN_IADBS', log_format)

xmls = list(find_suffixed_files(args.Pep3D_Spectrum, ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
print("analyzing folders:")
pprint(xmls)
research(xmls, args.fastas_path, iadbs_kwds, log, args.server_ip)
