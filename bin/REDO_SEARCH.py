import argparse
from docstr2argparse import parse_arguments
import logging
from pathlib import Path
from pprint import pprint

from vodkas import iadbs
from vodkas.fastas import get_fastas
from vodkas.fs import copy_folder, find_free_path, rm_tree
from vodkas.header_txt import parse_header_txt
from vodkas.logging import get_logger

DEBUG = True

# if __name__ == '__main__':
get_args = lambda x: dict(parse_arguments(x))
A = {**get_args(iadbs), **get_args(get_fastas)}
default_log = 'C:/SYMPHONY_VODKAS/temp_logs/plgs.log'

parser = argparse.ArgumentParser(description='Rerun search with iaDBs: outcomes will be dumped in the same folders as the provided files are in. WARNING: it replaces the results of the previous analysis.')
A['peptide3d_results'] = {'type': Path, 'nargs': "+",
    'help': 'Path(s) to the peptide3d result files.'}
A["--log_file"] = {'type': Path, 'default': default_log,
    'help': f"Local log file [default = {default_log}]."}
del A['input_file'], A['output_dir'], A['fasta_file']

for name, kwds in sorted(A.items()):
    parser.add_argument(name, **kwds)

args = parser.parse_args().__dict__

log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=args['log_file'], format=log_format, level=logging.INFO)
logger = get_logger('RERUN_IADBS', log_format)
del args['log_file']

print()
print(f"Running analysis on folders:")
pprint(args['peptide3d_results'])
print()

fasta_file = get_fastas(**args)
for pep3d in args['peptide3d_results']:
    logger.info(f"Starting search on '{pep3d}'.")
    try:
        if not pep3d.exists():
            logger.info(f"File missing: {pep3d}")
            raise FileNotFoundError(f"Did not find {pep3d}")
        iadbs_out, _ = iadbs(pep3d, pep3d.parent, fasta_file, **args)
    except Exception as e:
        logger.warning(repr(e))

logger.info("Search redone.")

