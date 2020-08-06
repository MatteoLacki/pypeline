import argparse
import json
import logging
from pathlib import Path
from subprocess import TimeoutExpired
import sys
from urllib.error import URLError

from docstr2argparse.parse import FooParser
from fs_ops.csv import rows2csv
from fs_ops.paths import find_folders
from waters.parsers import get_search_stats

from vodkas import apex3d, peptide3d, iadbs, on_windows, currentIP
from vodkas.fastas import fastas, fastas_gui
from vodkas.fs import find_free_path, move_folder, network_drive_exists
from vodkas.iadbs import parameters_gui
from vodkas.json import dump2json
from vodkas.header_txt import parse_header_txt
from vodkas.logging_alco import store_parameters, MockSender
from vodkas.remote.sender import Sender, currentIP
from vodkas.xml_parser import create_params_file


DEBUG = True

# defaults
local_output_folder = Path(r'C:/SYMPHONY_VODKAS/temp' if on_windows else '~/SYMPHONY_VODKAS/temp').expanduser().resolve()
log_file = Path('C:/SYMPHONY_VODKAS/temp_logs/plgs.log' if on_windows else '~/SYMPHONY_VODKAS/plgs.log').expanduser().resolve()
net_folder = Path('Y:/RES') if on_windows else ''

# CLIs
prompt = False
try:
    prompt = sys.argv[1] == '_prompt_input_'
except IndexError:
    pass

FP = FooParser([fastas, apex3d, peptide3d, iadbs])

if prompt:
    server_ip = sys.argv[2]
    raw_folders = sys.argv[3:]
else:
    ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

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

    ap.add_argument('--net_folder',
                    help=f"Network folder for results. Set to '' (empty word) if you want to skip copying.",
                    default=net_folder)

    ap.add_argument('--server_ip', 
                    type=str, 
                    help='IP of the server',
                    default=currentIP)

    ap.add_argument('--pipeline',
                    help='Are we running a pipeline?',
                    action='store_true')

    FP.updateParser(ap)
    args = ap.parse_args()
    FP.parse_kwds(args.__dict__)

    fasta_file_tag  = args.fastas
    raw_folders     = args.raw_folders
    if args.pipeline:
        # need to translate the paths.
        raw_folders = [samplename2networkpath(rf, acceptableDriveNames=('I','O')) for rf in raw_folders]

    local_output_folder = args.local_output_folder
    log_file        = args.log_file
    net_folder      = args.net_folder
    server_ip       = args.server_ip




logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
log = logging.getLogger('PLGS.py')
sender, logFun = get_sender_n_log_Fun(log, server_ip)
apex3d, peptide3d, iadbs, create_params_file, get_search_stats = \
    [logFun(f) for f in [apex3d, peptide3d, iadbs, create_params_file, get_search_stats]]



if prompt:
    print('Set timeouts [in minutes]:')  
    apex3d_kwds = {'timeout': prompt_timeout('Apex3D', 180)}
    assert apex3d_kwds['timeout'] >= 0, "If you are not running Apex3D, then why do you select raw folders?"
    peptide3d_kwds = {'timeout': prompt_timeout('Peptide3D', 180)}
    if peptide3d_kwds['timeout'] >= 0:
        iadbs_kwds = {'timeout': prompt_timeout('iaDBs', 180)}
    else:
        iadbs_kwds = {'timeout': 0}
else:
    apex3d_kwds     = FP.kwds['apex3d']
    peptide3d_kwds  = FP.kwds['peptide3d']
    iadbs_kwds      = FP.kwds['iadbs']


fasta_file = ''
if iadbs_kwds['timeout'] >= 0:
    if prompt:
        fasta_file = fastas(*fastas_gui())
        parameters_file = parameters_gui(FP['iadbs']['parameters_file'].info['default'])
    else:
        fasta_file = fastas(fasta_file_tag, **FP.kwds['fastas'])
        parameters_file = iadbs_kwds['parameters_file']
        del iadbs_kwds['parameters_file']



<<<<<<< HEAD
###### translate fastas to NCBIgeneralFastas and store it on the server
###### if it exists and is compatible, do nothing.
fastas = fastas(**FP.kwds['fastas'])
=======
if on_windows and net_folder and not network_drive_exists(net_folder):
    log.warning(f"no network drive for {net_folder}: saving locally")
>>>>>>> c77f833267b6cb61c22f6b21acb30079742a2954


assert len(raw_folders), "No raw folders passed!!!"
raw_folders = list(find_folders(raw_folders))
assert len(raw_folders), "No raw folders found!!!"
log.info(f"analyzing folders: {dump2json(raw_folders)}")

for raw_folder in raw_folders:
    try:
        if not raw_folder.is_dir():
            log.error(f"missing: {raw_folder}")
            continue
        log.info(f"analyzing: {raw_folder}")

        sender.update_group(raw_folder) # wtf??? change name ....
        acquired_name = raw_folder.stem
        header_txt = parse_header_txt(raw_folder/'_HEADER.TXT')
        sample_set = header_txt['Sample Description'][:8]
        #                   C:/SYMPHONY_PIPELINE/2019-008/O191017-04
        local_folder = local_output_folder/sample_set/acquired_name
        a = apex3d(raw_folder, local_folder,**apex3d_kwds)
        if peptide3d_kwds['timeout'] >= 0:
            p = peptide3d(a.with_suffix('.bin'), local_folder,**peptide3d_kwds)
            if iadbs_kwds['timeout'] >= 0:
                i = iadbs(p, local_folder, fasta_file, parameters_file, **iadbs_kwds)
                if i is not None: 
                    params = create_params_file(a, p, i) # for projectizer2.0
                    with open(a.parent/"params.json", 'w') as f:
                        json.dump(params, f)
                    search_stats = get_search_stats(i)
                    rows2csv(i.parent/'stats.csv',
                             [list(search_stats), list(search_stats.values())])
        if net_folder:
            #                     Y:/RES/2019-008
            net_set_folder = Path(net_folder)/sample_set
            net_set_folder.mkdir(parents=True, exist_ok=True)
            # if reanalysing, the old folder is preserved, 
            # and a version number appended to the new one
            # e.g.              Y:/RES/2019-008/O191017-04
            # replaced with:    Y:/RES/2019-008/O191017-04__v1
            final_net_folder = find_free_path(net_set_folder/acquired_name)
            try: #replace that with the general save moving routine with check-sums
                move_folder(local_folder, final_net_folder)
                if local_folder.parent.exists() and not local_folder.parent.glob('*'):
                    local_folder.parent.rmdir()
                log.info(f"moved {raw_folder} to {final_net_folder}")
            except RuntimeError as e:
                log.warning(f"not copied '{raw_folder}': {repr(e)}")
        else:
            log.info(f"saved '{raw_folder}' locally") 
    except TimeoutExpired as e:
        log.error(f"Timeout: {repr(e)}")
    except Exception as e:
        log.error(f"error: {repr(e)}")

log.info('PLGS finished.')