import argparse
from pprint import pprint
from pathlib import Path

from vodkas import plgs
from vodkas.fs import find_free_path, move_folder

DEBUG = True
net_folder = 'Y:/TESTRES' if DEBUG else 'Y:/RES'

ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.')
ap.add_argument('raw_folders', type=Path, nargs='+',
                help='Path(s) to raw folder(s).')
ap.add_argument('--temp_folder', type=Path,
                help='Path to temporary outcome folder.',
                default='C:/SYMPHONY_VODKAS/temp')
ap.add_argument('--log_file', type=Path,
                help='Path to temporary outcome folder.',
                default='C:/SYMPHONY_VODKAS/temp_logs/plgs.log')
ap.add_argument('--net_folder', type=Path,
                help=f"Network folder for results. Set to '' (empty word) if you want to skip copying [default = {net_folder}].",
                default=net_folder)

for arg_name, arg_desc in plgs.parsed.a2d:
    ap.add_argument(arg_name,**arg_desc)
args = ap.parse_args()
foo_args = plgs.parsed.parsed2kwds(args.__dict__)
if DEBUG:
    print(args.raw_folders)
    print(args.temp_folder)
    pprint(foo_args)

log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=args.log_file,
                    format=log_format,
                    level=logging.INFO)
log = get_logger('PLGS', log_format)

net_drive = args.net_folder.parents[0] 
if not net_drive.exists():
    log.error(f"no network drive {net_drive}")
    exit()

log.info("Analyzing folders:")
pprint(args.raw_folders)

for raw_folder in args.raw_folders:
    log.info(f"analyzing: {raw_folder}")
    try:

    except Exception as e:
        log.error(repr(e))

log.info('PLGS finished.')



