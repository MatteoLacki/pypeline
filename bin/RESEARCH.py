import argparse
import json
import logging
from pathlib import Path
from platform import system
from pprint import pprint
import sys
from tqdm import tqdm
from urllib.error import URLError

from docstr2argparse.parse import FooParser
from fs_ops.paths import find_suffixed_files
from fs_ops.csv import rows2csv
from waters.parsers import get_search_stats

from vodkas.fastas import fastas, fastas_gui
from vodkas.iadbs import iadbs, parameters_gui
from vodkas.json import dump2json
from vodkas.logging import store_parameters, MockSender
from vodkas.remote.sender import Sender, currentIP
from vodkas.xml_parser import create_params_file


# defaults
parameters_file = r'X:\SYMPHONY_VODKAS\search\215.xml'
log_file = 'C:/SYMPHONY_VODKAS/temp_logs/research.log' if system() == 'Windows' else '~/SYMPHONY_VODKAS/research.log'

mock = False
if mock:
    print('We are only mocking doing the RESEARCH!')


# CLIs
prompt = False # prompting only when using sendto/RESEARCH
try:
    prompt = sys.argv[1] == '_prompt_input_'
except IndexError:
    pass


if prompt:
    server_ip = sys.argv[2]
    Pep3D_Spectrum = sys.argv[3:]
else:
    ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                                 epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    FP = FooParser([fastas, iadbs])
    if system() == 'Windows': 
        FP.set_to_store_true(['mock'])
    else: # on Linux we can only mock.
        FP.mock()
        FP.del_args(['exe_path'])

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
    if args.iadbs_mock:
        print('We are only mocking doing the RESEARCH!')

    FP.parse_kwds(args.__dict__)

    server_ip       = args.server_ip
    log_file        = args.log_file
    fasta_file_tag  = args.fastas
    Pep3D_Spectrum  = args.Pep3D_Spectrum
    

######################################## Logging
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
log = logging.getLogger('RESEARCH.py')
try:
    print(f"Connecting to: {server_ip}")
    sender = Sender('RESEARCH', server_ip)
    logFun = store_parameters(log, sender)
except URLError as e:
    log.warning('Server down! Doing all things locally.')
    print(e)
    sender = MockSender()
    logFun = store_parameters(log, sender)

iadbs, create_params_file, get_search_stats = [logFun(f) for f in [iadbs, create_params_file, get_search_stats]]


if prompt:
    fasta_file = fastas(*fastas_gui())
    parameters_file = parameters_gui(parameters_file)
    iadbs_kwds = {'mock': mock}
else:
    fasta_file = fastas(fasta_file_tag, **FP.kwds['fastas'])
    iadbs_kwds = FP.kwds['iadbs']
    parameters_file = iadbs_kwds['parameters_file']
    del iadbs_kwds['parameters_file']



######################################## RESEARCH 
xmls = list(find_suffixed_files(Pep3D_Spectrum, ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
if xmls:
    print("analyzing folders:")
    pprint(xmls)
    for xml in tqdm(xmls):
        sender.update_group(xml)
        log.info(f"researching: {str(xml)}")
        try:
            iadbs_out = iadbs(xml, xml.parent, fasta_file, parameters_file, **iadbs_kwds)
            apex_out = iadbs_out.parent/iadbs_out.name.replace('_IA_workflow.xml', '_Apex3D.xml')
            params = create_params_file(apex_out, xml, iadbs_out) # for projectizer2.0
            with open(iadbs_out.parent/"params.json", 'w') as f:
                json.dump(params, f)
            search_stats = get_search_stats(iadbs_out)
            rows2csv(iadbs_out.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
        except Exception as e:
            log.warning(repr(e))
            print(e)
    log.info("Search redone.")
else:
    log.error('No xmls found.')
    print('No xmls found.')