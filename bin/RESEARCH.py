import argparse
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
from vodkas.logging import store_parameters
from vodkas.remote.sender import Sender, currentIP
from vodkas.xml_parser import print_parameters_file, create_params_file


prompt = False

try:
    prompt = sys.argv[1] == 'prompt_me_and_i_will_tell_you_the_future'
except IndexError:
    pass

if prompt:
    server_ip, log_file, parameters_file = sys.argv[2:5]
    Pep3D_Spectrum = sys.argv[5:]
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

    ap.add_argument('Pep3D_Spectrum', type=Path, nargs='+',
        help="Path(s) to outputs of Peptide3D. \
              If provided with a folder instead, \
              a recursive search for files matching '*_Pep3D_Spectrum.xml' is performed.")

    ap.add_argument('--log_file',
        type=lambda p: Path(p).expanduser().resolve(),
        help='Path to temporary outcome folder.',
        default= 'C:/SYMPHONY_VODKAS/temp_logs/research.log' if system() == 'Windows' else '~/SYMPHONY_VODKAS/research.log')

    ap.add_argument('--server_ip', 
                    type=str, 
                    help='IP of the server',
                    default=currentIP)

    FP.updateParser(ap)
    args = ap.parse_args()
    FP.parse_kwds(args.__dict__)
    log_file = args.log_file
    server_ip = args.server_ip
    Pep3D_Spectrum = args.Pep3D_Spectrum
    

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
    logFun = store_parameters(log)
iadbs, create_params_file, get_search_stats = [logFun(f) for f in [iadbs, create_params_file, get_search_stats]]


if prompt:
    fasta_file = fastas(*fastas_gui())
    parameters_file = parameters_gui(parameters_file)
    iadbs_kwds = {}
else:
    fasta_file = fastas(**FP.kwds['fastas'])
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
            iadbs_out = iadbs(xml, xml.parent, fasta_file, parameters_file, **FP.kwds['iadbs'])
            apex_out = iadbs_out.parent/iadbs_out.name.replace('_IA_workflow.xml', '_Apex3D.xml')
            params = create_params_file(apex_out, xml, iadbs_out) # for projectizer2.0
            search_stats = get_search_stats(iadbs_out)
            rows2csv(iadbs_out.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
        except Exception as e:
            log.warning(repr(e))
            print(e)
    log.info("Search redone.")
else:
    log.error('No xmls found.')
    print('No xmls found.')