import argparse
import logging
from pprint import pprint
from pathlib import Path
import platform

from vodkas import plgs
from vodkas.fs import find_free_path, move_folder
from vodkas.logging import get_logger

DEBUG = True
net_folder = 'Y:/TESTRES' if DEBUG else 'Y:/RES'
log_folder = {
    "Windows": Path('C:/SYMPHONY_VODKAS/temp_logs/plgs.log'),
    "Linux":   Path('~/plgs.log').expanduser(),
    "Darwin":  Path('~/plgs.log').expanduser(),
}[platform.system()]

ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.')
ap.add_argument('raw_folders', type=Path, nargs='+',
                help='Path(s) to raw folder(s).')
ap.add_argument('--local_output_folder', type=Path,
                help='Path to temporary outcome folder.',
                default='C:/SYMPHONY_VODKAS/temp')
ap.add_argument('--log_file', type=Path,
                help='Path to temporary outcome folder.',
                default=log_folder)
ap.add_argument('--net_folder', type=Path,
                help=f"Network folder for results. Set to '' (empty word) if you want to skip copying [default = {net_folder}].",
                default=net_folder)
for arg_name, arg_desc in plgs.parsed.a2d:
    ap.add_argument(arg_name,**arg_desc)
args = ap.parse_args()
foo_args = plgs.parsed.parsed2kwds(args.__dict__)
if DEBUG:
    print(args.raw_folders)
    print(args.local_output_folder)
    pprint(foo_args)

# setting up loggers
log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=args.log_file,
                    format=log_format,
                    level=logging.INFO)
log = get_logger('PLGS', log_format)

# check network drives
net_drive = args.net_folder.parents[0]
if not net_drive.exists() and not str(net_drive) == '':
    log.warning(f"no network drive (proceeding locally): {net_drive}")

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
        plgs_ok = plgs(raw_folder, local_folder, **args)
        if plgs_ok and args.net_folder:
            #                     Y:/TESTRES/2019-008
            net_set_folder = args.net_folder/sample_set
            net_set_folder.mkdir(parents=True, exist_ok=True)
            # if the project is reanalyzed, the old one will not be replaced
            # but a version number will be appended to the acuired name
            # e.g. if we already have:          Y:/TESTRES/2019-008/O191017-04
            # then results will be copied to:   Y:/TESTRES/2019-008/O191017-04__v1
            net_folder = find_free_path(args.net_folder/sample_set/acquired_name)
            try:
                move_folder(local_folder, net_folder)
                if local_folder.parent.exists() and not local_folder.parent.glob('*'):
                    local_folder.parent.rmdir()
                log.info("moved results to the server.")
            except RuntimeError as e:
                log.warning(f"not copied '{raw_folder}': {repr(e)}")
        else:
            if not plgs_ok:
                log.error(f"plgs_ok == False")
            if not args.net_folder:
                log.warning(f"saved '{raw_folder}' locally") 
        log.info(f"Finished: '{raw_folder}'")
    except Exception as e:
        log.error(f"error: {repr(e)}")
log.info('PLGS finished.')



