from pathlib import Path
from pprint import pprint
import json
import logging

from vodkas import iadbs
from vodkas.fastas import get_fastas
from vodkas.logging import get_logger


symphony_local = Path(r"C:/SYMPHONY_VODKAS")
logging.basicConfig(filename=symphony_local/"iadbs.log",
                    format='RERUN_IADBS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)

fold = Path(r"Y:\RES\2019-095")
folders = [fold/f"O190920_{i}" 
		   for i in range(10,29) if i not in (15,22)]
fastas = get_fastas('human')

problems = []
# f = folders[0]
for f in folders[1:]:
	try:
		input = f/f"{f.stem}_Pep3D_Spectrum.xml"
		outfile, _ = iadbs(input, f, fastas)
	except Exception as e:
		problems.append((str(f), repr(e)))

if problems:
	with open(Path('C:/SYMPHONY_VODKAS/problems')) as h:
		json.dump(problems,h,indent=4)




