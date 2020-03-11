import argparse
import json
import logging
from pprint import pprint
from pathlib import Path
from platform import system
from tqdm import tqdm
import sys
from urllib.error import URLError

from docstr2argparse.parse import FooParser
from fs_ops.csv import rows2csv
from fs_ops.paths import find_folders
from waters.parsers import get_search_stats

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fastas import fastas, fastas_gui
from vodkas.fs import find_free_path, move_folder, network_drive_exists
from vodkas.iadbs import parameters_gui
from vodkas.json import dump2json
from vodkas.header_txt import parse_header_txt
from vodkas.logging import store_parameters, MockSender
from vodkas.remote.sender import Sender, currentIP
from vodkas.xml_parser import create_params_file


DEBUG = True

mock_apex3d = False
mock_peptide3d = False
mock_iadbs = False
if mock_apex3d or mock_peptide3d or mock_iadbs:
    print(f'We are mocking: apex3d {mock_apex3d}, peptide3d {mock_peptide3d}, iadbs {mock_iadbs}')


# defaults
parameters_file = Path(r'X:\SYMPHONY_VODKAS\search\215.xml')
local_output_folder = Path(r'C:/SYMPHONY_VODKAS/temp' if system() == 'Windows' else '~/SYMPHONY_VODKAS/temp')
log_file = Path('C:/SYMPHONY_VODKAS/temp_logs/plgs.log' if system() == 'Windows' else '~/SYMPHONY_VODKAS/plgs.log')
net_folder = Path(('Y:/TESTRES2' if DEBUG else 'Y:/RES') if system() == 'Windows' else '')


# CLIs
prompt = False
try:
    prompt = sys.argv[1] == '_prompt_input_'
except IndexError:
    pass

if prompt:
    server_ip = sys.argv[2]
    raw_folders = sys.argv[3:]

else:######################################## CLI
    ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    FP = FooParser([fastas, apex3d, peptide3d, iadbs])
    if system() == 'Windows': 
        FP.set_to_store_true(['mock'])
    else: # on Linux we can only mock.
        FP.mock()
        FP.del_args(['exe_path'])

    ap.add_argument('fastas', type=Path,
                    help='Path to fastas, or a short tag (human, wheat, ...).')

    ap.add_argument('raw_folders', type=Path, nargs='+',
        help='Path(s) to raw folder(s), \
        or paths that will be recursively searched for ".raw" folders.')

    ap.add_argument('--local_output_folder', type=Path,
                    help='Path to temporary outcome folder.',
                    default=local_output_folder)

    ap.add_argument('--log_file',
        type=lambda p: Path(p).expanduser().resolve(),
        help='Path to temporary outcome folder.',
        default=log_file)

    ap.add_argument('--net_folder', type=Path,
                    help=f"Network folder for results. Set to '' (empty word) if you want to skip copying.",
                    default=net_folder)

    ap.add_argument('--no_peptide3d', action='store_true',
                    help='Do not run peptide3d.')

    ap.add_argument('--no_iadbs', action='store_true',
                    help='Do not run iadbs.')

    ap.add_argument('--server_ip', 
                    type=str, 
                    help='IP of the server',
                    default=currentIP)

    FP.updateParser(ap)
    args = ap.parse_args()
    FP.parse_kwds(args.__dict__)

    fasta_file_tag  = args.fastas
    raw_folders     = args.raw_folders
    local_output_folder = args.local_output_folder
    log_file        = args.log_file
    net_folder      = args.net_folder
    no_peptide3d    = args.no_peptide3d
    no_iadbs        = args.no_iadbs
    server_ip       = args.server_ip




######################################## Logging
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
log = logging.getLogger('PLGS.py')
try:
    print(f"Connecting to: {server_ip}")
    sender = Sender('PLGS', server_ip)
    logFun = store_parameters(log, sender)
except URLError as e:
    log.warning('Server down! Doing all things locally.')
    print(e)
    sender = MockSender()
    logFun = store_parameters(log, sender)

apex3d, peptide3d, iadbs, create_params_file, get_search_stats = [logFun(f) for f in [apex3d, peptide3d, iadbs, create_params_file, get_search_stats]]


######################################## Fastas
if prompt:
    no_peptide3d = input('Run Peptide3D: press ENTER. Stop it: write "no": ') == 'no'
    if not no_peptide3d:
        no_iadbs = input('Run iaDBs (search): press ENTER. Stop it: write "no": ') == 'no' 
    else:
        no_iadbs = True


if not no_peptide3d and not no_iadbs:
    if prompt:
        fasta_file = fastas(*fastas_gui())
        parameters_file = parameters_gui(parameters_file)
        apex3d_kwds = {'mock': mock_apex3d}
        peptide3d_kwds = {'mock': mock_peptide3d}
        iadbs_kwds = {'mock': mock_iadbs}
    else:
        fasta_file = fastas(fasta_file_tag, **FP.kwds['fastas'])
        apex3d_kwds = FP.kwds['apex3d']
        peptide3d_kwds = FP.kwds['peptide3d']
        iadbs_kwds = FP.kwds['iadbs']
        parameters_file = iadbs_kwds['parameters_file']
        del iadbs_kwds['parameters_file']


######################################## Network drives.
if system() == 'Windows' and not net_folder == '' and not network_drive_exists(net_folder):
    log.warning(f"no network drive for {net_folder}: saving locally")


######################################## PLGS 
assert len(raw_folders), "No raw folders passed!!!"
raw_folders = list(find_folders(raw_folders))
assert len(raw_folders), "No raw folders found!!!"
log.info(f"analyzing folders: {dump2json(raw_folders)}")
pprint(raw_folders)

for raw_folder in tqdm(raw_folders):
    # try:
    if not raw_folder.is_dir():
        log.error(f"missing: {raw_folder}")
        continue
    log.info(f"analyzing: {raw_folder}")
    sender.update_group(raw_folder)
    acquired_name = raw_folder.stem
    header_txt = parse_header_txt(raw_folder/'_HEADER.TXT')
    sample_set = header_txt['Sample Description'][:8]
    #                   C:/SYMPHONY_PIPELINE/2019-008/O191017-04
    local_folder = local_output_folder/sample_set/acquired_name
    a = apex3d(raw_folder, local_folder,**apex3d_kwds)
    if not no_peptide3d:
        p = peptide3d(a.with_suffix('.bin'), local_folder,**peptide3d_kwds)
        if not no_iadbs:
            i= iadbs(p, local_folder, fasta_file, parameters_file, **iadbs_kwds)
            params = create_params_file(a, p, i) # for projectizer2.0
            with open(a.parent/"params.json", 'w') as f:
                json.dump(params, f)
            search_stats = get_search_stats(i)
            rows2csv(i.parent/'stats.csv',
                     [list(search_stats), list(search_stats.values())])
    if net_folder:
        #                     Y:/TESTRES/2019-008
        net_set_folder = net_folder/sample_set
        net_set_folder.mkdir(parents=True, exist_ok=True)
        # if reanalysing, the old folder is preserved, 
        # and a version number appended to the new one
        # e.g.              Y:/TESTRES/2019-008/O191017-04
        # replaced with:    Y:/TESTRES/2019-008/O191017-04__v1
        net_folder = find_free_path(net_folder/sample_set/acquired_name)
        try:
            move_folder(local_folder, net_folder)
            if local_folder.parent.exists() and not local_folder.parent.glob('*'):
                local_folder.parent.rmdir()
            log.info(f"moved {raw_folder} to {net_folder}")
        except RuntimeError as e:
            log.warning(f"not copied '{raw_folder}': {repr(e)}")
    else:
        log.info(f"saved '{raw_folder}' locally") 
    # except Exception as e:
    #     log.error(f"error: {repr(e)}")

log.info('PLGS finished.')