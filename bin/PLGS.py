import argparse
import logging
from pprint import pprint
from pathlib import Path
from platform import system
from tqdm import tqdm
from urllib.error import URLError

from docstr2argparse.parse import FooParser
from fs_ops.csv import rows2csv
from fs_ops.paths import find_folders
from waters.parsers import get_search_stats

from vodkas.fastas import fastas
from vodkas import apex3d, peptide3d, iadbs
from vodkas.fs import find_free_path, move_folder, network_drive_exists
from vodkas.header_txt import parse_header_txt
from vodkas.logging import store_parameters, MockSender
from vodkas.remote.sender import Sender, currentIP
from vodkas.xml_parser import create_params_file
from vodkas.json import dump2json


DEBUG = True

######################################## CLI
ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

FP = FooParser([fastas, apex3d, peptide3d, iadbs])
if system() == 'Windows': 
    FP.set_to_store_true(['mock','prompt'])
else: # on Linux we can only mock.
    FP.set_to_store_true(['prompt'])
    FP.mock()
    FP.del_args(['exe_path'])

ap.add_argument('path_to_fastas', 
                help='Fucking fastas.')

ap.add_argument('raw_folders', type=Path, nargs='+',
                help='Path(s) to raw folder(s), or paths that will be recursively searched for ".raw" folders.')

ap.add_argument('--local_output_folder', type=Path,
                help='Path to temporary outcome folder.',
                default=r'C:/SYMPHONY_VODKAS/temp' if system() == 'Windows' else '~/SYMPHONY_VODKAS/temp')

ap.add_argument('--log_file',
    type=lambda p: Path(p).expanduser().resolve(),
    help='Path to temporary outcome folder.',
    default= 'C:/SYMPHONY_VODKAS/temp_logs/plgs.log' if system() == 'Windows' else '~/SYMPHONY_VODKAS/plgs.log')

ap.add_argument('--net_folder', type=Path,
                help=f"Network folder for results. Set to '' (empty word) if you want to skip copying.",
                default=('Y:/TESTRES2' if DEBUG else 'Y:/RES') if system() == 'Windows' else '')

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


######################################## Logging
logging.basicConfig(filename=args.log_file, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
log = logging.getLogger('PLGS.py')
try:
    sender = Sender('PLGS', args.server_ip)
    logFun = store_parameters(log, sender)
except URLError:
    log.warning('Server down! Doing all things locally.')
    print('Server down! Doing all things locally.')
    sender = MockSender()
    logFun = store_parameters(log, sender)

apex3d, peptide3d, iadbs, create_params_file, get_search_stats = [logFun(f) for f in [apex3d, peptide3d, iadbs, create_params_file, get_search_stats]]


######################################## Network drives.
if system() == 'Windows' and not args.net_folder == '' and not network_drive_exists(args.net_folder):
    log.warning(f"no network drive for {args.net_folder}: saving locally")

if not network_drive_exists(args.fastas_db):
    log.warning(f"network drive absent: {args.fastas_db}")


###### translate fastas to NCBIgeneralFastas and store it on the server
if not args.no_iadbs:
    fastas = fastas(args.path_to_fastas, **FP.kwds['fastas'])


######################################## PLGS 
raw_folders = list(find_folders(args.raw_folders))
log.info(f"analyzing folders: {dump2json(raw_folders)}")
pprint(raw_folders)

for raw_folder in tqdm(raw_folders):
    try:
        if not raw_folder.is_dir():
            log.error(f"missing: {raw_folder}")
            continue
        log.info(f"analyzing: {raw_folder}")
        sender.update_group(raw_folder)
        acquired_name = raw_folder.stem
        header_txt = parse_header_txt(raw_folder/'_HEADER.TXT')
        sample_set = header_txt['Sample Description'][:8]
        #                   C:/SYMPHONY_PIPELINE/2019-008/O191017-04
        local_folder = args.local_output_folder/sample_set/acquired_name
        a = apex3d(raw_folder, local_folder,**FP.kwds['apex3d'])
        if not args.no_peptide3d:
            p = peptide3d(a.with_suffix('.bin'), local_folder,**FP.kwds['peptide3d'])
            if not args.no_iadbs:
                i= iadbs(p, local_folder, fastas,**FP.kwds['iadbs'])
                create_params_file(a, p, i) # for projectizer2.0
                search_stats = get_search_stats(i)
                rows2csv(i.parent/'stats.csv',
                         [list(search_stats), list(search_stats.values())])
        if args.net_folder:
            #                     Y:/TESTRES/2019-008
            net_set_folder = args.net_folder/sample_set
            net_set_folder.mkdir(parents=True, exist_ok=True)
            # if reanalysing, the old folder is preserved, 
            # and a version number appended to the new one
            # e.g.              Y:/TESTRES/2019-008/O191017-04
            # replaced with:    Y:/TESTRES/2019-008/O191017-04__v1
            net_folder = find_free_path(args.net_folder/sample_set/acquired_name)
            try:
                move_folder(local_folder, net_folder)
                if local_folder.parent.exists() and not local_folder.parent.glob('*'):
                    local_folder.parent.rmdir()
                log.info(f"moved {raw_folder} to {net_folder}")
            except RuntimeError as e:
                log.warning(f"not copied '{raw_folder}': {repr(e)}")
        else:
            log.info(f"saved '{raw_folder}' locally") 
    except Exception as e:
        log.error(f"error: {repr(e)}")

log.info('PLGS finished.')