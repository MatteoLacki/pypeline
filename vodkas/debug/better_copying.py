from pathlib import Path

from vodkas.fs import copy_folder

s = Path('C:/temp/A')
t = Path('J:/test_RES')
proc = copy_folder(s, t)
proc = copy_folder(s, Path('D:/test_RES'))

type(proc.returncode)