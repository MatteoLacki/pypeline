import argparse
import logging
from pprint import pprint
from pathlib import Path
import platform

from vodkas import plgs
from vodkas.fs import find_free_path, move_folder, network_drive_exists
from vodkas.header_txt import parse_header_txt
from vodkas.logging import get_logger

DEBUG = True

ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('fastas', type=str,
                help="fastas (str): Fasta file to use, or a prefix to one of the standard proteomes used, e.g. 'human'.")
ap.add_argument('raw_folders', type=Path, nargs='+',
                help='Path(s) to raw folder(s).')
ap.add_argument('--local_output_folder', type=Path,
                help='Path to temporary outcome folder.',
                default=r'C:/SYMPHONY_VODKAS/temp')
ap.add_argument('--fastas_db', type=Path,
                help="Path to fastas DB: used when supplying reduced fasta names, e.g. 'human'",
                default=r'X:/SYMPHONY_VODKAS/fastas/latest')
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
if DEBUG:
    print(args.raw_folders)
    print(args.local_output_folder)
    pprint(kwds)


# setting up logger
log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=args.log_file,
                    format=log_format,
                    level=logging.INFO)
log = get_logger('PLGS', log_format)


# check network drive
if not args.net_folder == '' and not network_drive_exists(args.net_folder):
    log.warning(f"no network drive for {args.net_folder}: saving locally")
if not network_drive_exists(args.fastas_db):
    log.warning(f"network drive absent: {args.fastas_db}")



# check fastas: assumed to be kept only on the server, not locally
standard_fastas = {p.stem.split('_')[0]:p for p in args.fastas_db.glob(f"*/PLGS/*.fasta")}
if args.fastas in standard_fastas:
    fastas = standard_fastas[args.fastas]
else:
    fastas = Path(args.fastas)
    if not fastas.exists():
        log.error(f"Fastas unreachable: {fastas}")

# add automatic translation of fastas to proper format.
# can do it every time: super fast it is.
# then, dump locally?
# no, better aumatically add them to custom fastas.

 
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
        plgs_ok = plgs(fastas, raw_folder, local_folder, **kwds)
        if plgs_ok and args.net_folder:
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
            if not plgs_ok:
                log.error(f"plgs_ok == False")
            if not args.net_folder:
                log.warning(f"saved '{raw_folder}' locally") 
        log.info(f"Finished: '{raw_folder}'")
    except Exception as e:
        log.error(f"error: {repr(e)}")
log.info('PLGS finished.')
input("Press Enter to continue...")


