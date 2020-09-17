import argparse
import json
import logging
from pathlib import Path
import platform
from pprint import pprint
import sys
from tqdm import tqdm
from urllib.error import URLError

from docstr2argparse.parse import FooParser
from fs_ops.paths import find_suffixed_files
from fs_ops.csv import rows2csv
from waters.parsers import get_search_stats

from vodkas import on_windows
from vodkas.fastas import fastas, fastas_gui
from vodkas.iadbs import iadbs, parameters_gui
from vodkas.logging_alco import get_sender_n_log_Fun
from vodkas.remote.sender import currentIP
from vodkas.xml_parser import create_params_file
from vodkas.misc import prompt_timeout

log_file = Path('C:/SYMPHONY_VODKAS/temp_logs/research.log' if on_windows else '~/SYMPHONY_VODKAS/plgs.log').expanduser().resolve()

prompt = False # prompting only when using sendto/RESEARCH
try:
    prompt = sys.argv[1] == '_prompt_input_'
except IndexError:
    pass

FP = FooParser([fastas, iadbs])

if prompt:
    server_ip = sys.argv[2]
    Pep3D_Spectrum = sys.argv[3:]
else:
    ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                                 epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    ap.add_argument('fastas', type=Path,
                    help='Path to fastas, or a short tag (human, wheat, ...).')

    ap.add_argument('Pep3D_Spectrum', type=Path, nargs='+',
        help="Path(s) to outputs of Peptide3D. \
              If provided with a folder instead, \
              a recursive search for files matching '*_Pep3D_Spectrum.xml' is performed.")

    ap.add_argument('--log_file',
        type=lambda p: Path(p).expanduser().resolve(),
        help='Path to temporary outcome folder.',
        default=log_file)

    ap.add_argument('--server_ip', 
                    type=str, 
                    help='IP of the server',
                    default=currentIP)

    FP.updateParser(ap)
    args = ap.parse_args()
    FP.parse_kwds(args.__dict__)

    server_ip       = args.server_ip
    log_file        = args.log_file
    fasta_file_tag  = args.fastas
    Pep3D_Spectrum  = args.Pep3D_Spectrum
    


logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
log = logging.getLogger('RESEARCH.py')
sender, logFun = get_sender_n_log_Fun(log, server_ip)
iadbs, create_params_file, get_search_stats = \
    [logFun(f) for f in [iadbs, create_params_file, get_search_stats]]


if prompt:
    print('WARNING: THIS SCRIPT OVERWRITES PREVIOUS *_IA_workflow.xml FILES, params.json, AND stats.csv')
    print()
    print('Set timeouts [in minutes] for iaDBS:')
    iadbs_kwds = {'timeout': prompt_timeout('iaDBs', 180)}
    fasta_file = fastas(*fastas_gui())
    parameters_file = parameters_gui(FP['iadbs']['parameters_file'].info['default'])
else:
    fasta_file = fastas(fasta_file_tag, **FP.kwds['fastas'])
    iadbs_kwds = FP.kwds['iadbs']
    parameters_file = iadbs_kwds['parameters_file']
    del iadbs_kwds['parameters_file']

assert len(Pep3D_Spectrum), "No Peptide3D spectra passed on input!!!"
xmls = list(find_suffixed_files(Pep3D_Spectrum, ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
assert len(xmls), "No Peptide3D spectra found!!!"
log.error('No xmls found.')


print("analyzing folders:")
pprint(xmls)
for xml in tqdm(xmls):
    sender.update_group(xml)
    log.info(f"researching: {str(xml)}")
    try:
        iadbs_xml = iadbs(xml, xml.parent, fasta_file, parameters_file, **iadbs_kwds)
        if iadbs_xml is not None:
            apex_out = iadbs_xml.parent/iadbs_xml.name.replace('_IA_workflow.xml', '_Apex3D.xml')
            params = create_params_file(apex_out, xml, iadbs_xml) # for projectizer2.0
            with open(iadbs_xml.parent/"params.json", 'w') as f:
                json.dump(params, f)
            search_stats = get_search_stats(iadbs_xml)
            rows2csv(iadbs_xml.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
    except Exception as e:
        log.warning(repr(e))
        print(e)
    print()
log.info("Search redone.")
