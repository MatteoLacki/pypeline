import argparse
from docstr2argparse.parse import foo2argparse
import logging
from pathlib import Path
import platform
from pprint import pprint
import pandas as pd
import json
from tqdm import tqdm

from fs_ops.paths import find_suffixed_files
from fs_ops.csv import rows2csv
from waters.parsers import iaDBsXMLparser

from vodkas.fastas import get_fastas
from vodkas.json import dump2json
from vodkas.logging import get_logger
from vodkas.remote.sender import Sender
from vodkas.xml_parser import create_params_file


MOCK = True
if MOCK:
    from vodkas.iadbs import iadbs_mock as iadbs
else:
    from vodkas import iadbs


ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('--log_file', type=Path,
                help='Path to temporary outcome folder.',
                default={"Windows": 'C:/SYMPHONY_VODKAS/temp_logs/research.log',
                          "Linux":  Path('~/research.log').expanduser(),
                          "Darwin": Path('~/research.log').expanduser(),}[platform.system()])
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

try: # translate fastas to NCBIgeneralFastas and store it on the server.
    iadbs_kwds['fasta_file'] = get_fastas(args.fastas_path)
except FileNotFoundError:
    log.error(f"Fastas unreachable: {fastas}")
    exit()

server = Sender('RESEARCH', args.server_ip)

print(args.Pep3D_Spectrum)
xmls = list(find_suffixed_files(args.Pep3D_Spectrum, ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
print("analyzing folders:")
pprint(xmls)


for xml in tqdm(xmls):
    log.info(f"researching: {str(xml)}")
    try:
        iadbs_kwds['input_file'] = xml
        iadbs_kwds['output_dir'] = xml.parent
        server.send_pair('iadbs_args', dump2json(iadbs_kwds))
        iadbs_out, _, runtime = iadbs(**iadbs_kwds)

        apex_out = iadbs_out.parent/iadbs_out.name.replace('_IA_workflow.xml', '_Apex3D.xml')
        create_params_file(apex_out, xml, iadbs_out) # for projectizer2.0

        search_stats = iaDBsXMLparser(iadbs_out).info()
        server.send_pair("stats", dump2json(search_stats))
        rows2csv(iadbs_out.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
    except Exception as e:
        log.warning(repr(e))
log.info("Search redone.")
