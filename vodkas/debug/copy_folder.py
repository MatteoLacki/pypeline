from pathlib import Path

from vodkas.fs import copy_folder


p = Path(r"O:\RAW\O1910\O191017_19.raw")
r = Path(r'Y:/TESTRES/O191017_19')
copy_folder(p, r)
