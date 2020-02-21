
import sys
import logging
from pathlib import Path
import platform
from pprint import pprint

from fs_ops.paths import find_suffixed_files

from vodkas import iadbs
from vodkas.fastas import get_fastas
from vodkas.logging import get_logger
from vodkas.xml_parser import parse_parameters_file

paths = [Path(p).resolve().expanduser() for p in sys.argv[1:]]
xmls = list(find_suffixed_files(paths,
                                ['**/*_Pep3D_Spectrum.xml'],
                                ['.xml']))
print("Re-analyzing folders:")
pprint(xmls)

fastas_path = input('fastas to use: ')

parameters_file = Path(r"X:/SYMPHONY_VODKAS/search/215.xml")
print(f'Default search parameters (parameters_file):')
parse_parameters_file(parameters_file)
parameters_file = input(f'If OK hit ENTER, or provide better path: ') or parameters_file
print(parameters_file)


log_file = {"Windows": 'C:/SYMPHONY_VODKAS/temp_logs/research.log',
                          "Linux":  Path('~/research.log').expanduser(),
                          "Darwin": Path('~/research.log').expanduser(),}[platform.system()]
log_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:'
logging.basicConfig(filename=log_file, format=log_format, level=logging.INFO)
log = get_logger('RERUN_IADBS', log_format)


try: # translate fastas to NCBIgeneralFastas and store it on the server.
    fastas = get_fastas(fastas_path)
except FileNotFoundError:
    log.error(f"Fastas unreachable: {fastas}")
    exit()


for xml in xmls:
    log.info(f"researching: {str(xml)}")
    try:
        iadbs_out, _, runtime = iadbs(xml, xml.parent, fastas)
    except Exception as e:
        log.warning(repr(e))
log.info("Search redone.")

parameters_file = Path(r"X:/SYMPHONY_VODKAS/search/215.xml")
input('press ENTER')

