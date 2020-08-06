from pathlib import Path
from pprint import pprint
import json
import logging

from vodkas import iadbs
from vodkas.fastas import get_fastas
from vodkas.logging_algo import get_logger

symphony_local = Path(r"C:/SYMPHONY_VODKAS")
logging.basicConfig(filename=symphony_local/"iadbs.log",
                    format='RERUN_IADBS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)

fold = Path(r"Y:\RES\2019-095")

def zeropad(x, k=2):
    if x < 10:
        x = f"0{x}"
    return str(x)

folders = [fold/f"O190920_{zeropad(i)}"
		   for i in range(2,9) if i not in (8,15,22,29)]
# folders = [fold/f"O190920_{zeropad(i)}"
#            for i in range(2,29) if i not in (8,15,22,29)]
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




