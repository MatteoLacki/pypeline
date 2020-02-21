"""
Prepare a csv input for ISOQuant.
It is a projectizer v. 2.0

Author: MatteoLacki
"""

import argparse
import json
from pathlib import Path

from vodkas.projectizer import dump_to_csv, parse_raw_folder, MissingInfoForIsoquant


p = argparse.ArgumentParser(description="Prepare a csv input file for an ISOQuant project. The files should include the necessary 'params.json' file.")
p.add_argument("folders",
    help="Raw files to be processed with ISOQuant.",
    nargs="+")
p.add_argument("-t", "--target",
               default=Path("./project.csv"),
               help="Path to the output csv file [default ./project.csv]")
p.add_argument( "-v", "--verbose",
                action='store_const',
                const=True,
                default=False,
                help="Show all verbosely.")
a = p.parse_args()
if a.verbose:
    print(a.__dict__)

try:
    csv_rows = []
    for f in a.folders:
        csv_rows.append(parse_raw_folder(f))
    dump_to_csv(a.target,
                csv_rows,
                ("acquired_name", "peptide3d_xml", "iaDBs_xml", "sample_description"))
    if a.verbose:
        print("Thank you for using our services. Have a good day!")
except MissingInfoForIsoquant:
    print("Insufficient info in file {}".format(str(f)))
    print("Omit this file and reprocess the other ones, naturally.")
