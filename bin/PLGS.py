import argparse
import logging
from pprint import pprint
from pathlib import Path
import platform
import json

from docstr2argparse.parse import foo2argparse

from vodkas import plgs
from vodkas.fastas import get_fastas
from vodkas.fs import find_free_path, move_folder, network_drive_exists
from vodkas.header_txt import parse_header_txt
from vodkas.logging import get_logger
from vodkas.remote.sender import Sender

DEBUG = True

ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
for n,_,h in foo2argparse(get_fastas, get_short=False):
    ap.add_argument(n, **h)
ap.add_argument('raw_folders', type=Path, nargs='+',
                help='Path(s) to raw folder(s).')
ap.add_argument('--local_output_folder', type=Path,
                help='Path to temporary outcome folder.',
                default=r'C:/SYMPHONY_VODKAS/temp')
ap.add_argument('--log_file', type=Path,
                help='Path to temporary outcome folder.',
                default={"Windows": 'C:/SYMPHONY_VODKAS/temp_logs/plgs.log',
                          "Linux":  Path('~/plgs.log').expanduser(),
                          "Darwin": Path('~/plgs.log').expanduser(),}[platform.system()])
ap.add_argument('--net_folder', type=Path,
                help=f"Network folder for results. Set to '' (empty word) if you want to skip copying.",
                default='Y:/TESTRES2' if DEBUG else 'Y:/RES')
for arg_name, arg_desc in plgs.parsed.a2d:
    ap.add_argument(arg_name,**arg_desc)
args = ap.parse_args()
kwds = {k+"_kwds":v for k,v in plgs.parsed.parsed2kwds(args.__dict__).items()}


print(args.raw_folders)
print(args.local_output_folder)
pprint(kwds)


# setting up logger
log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=args.log_file,
                    format=log_format,
                    level=logging.INFO)
log = get_logger('PLGS', log_format)


if not args.net_folder == '' and not network_drive_exists(args.net_folder):
    log.warning(f"no network drive for {args.net_folder}: saving locally")
if not network_drive_exists(args.fastas_db):
    log.warning(f"network drive absent: {args.fastas_db}")


try: # translate fastas to NCBIgeneralFastas and store it on the server.
    fastas = get_fastas(args.fastas_path)
except FileNotFoundError:
    log.error(f"Fastas unreachable: {args.fastas_path}")
    exit()

# setting up connection with the server DB.
# server = Sender()
 
log.info("analyzing folders:")
pprint(args.raw_folders)
for raw_folder in args.raw_folders:
    try:
        log.info(f"analyzing: {raw_folder}")
        if not raw_folder.is_dir():
            log.error(f"missing: {raw_folder}")
            continue
        acquired_name = raw_folder.stem
        header_txt = parse_header_txt(raw_folder/'_HEADER.TXT')
        sample_set = header_txt['Sample Description'][:8]
        #                   C:/SYMPHONY_PIPELINE/2019-008/O191017-04
        local_folder = args.local_output_folder/sample_set/acquired_name
        # message = [str(fastas), str(raw_folder), str(local_folder), kwds]
        # server.send(message)
        
        plgs(fastas, raw_folder, local_folder, **kwds)
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
                log.info("moved results to the server.")
            except RuntimeError as e:
                log.warning(f"not copied '{raw_folder}': {repr(e)}")
        else:
            log.warning(f"saved '{raw_folder}' locally") 
        log.info(f"Finished: '{raw_folder}'")
    except Exception as e:
        log.error(f"error: {repr(e)}")
log.info('PLGS finished.')
