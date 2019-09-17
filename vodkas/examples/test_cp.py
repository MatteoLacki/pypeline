from vodkas.fs import copy_folder
from pathlib import Path

A = Path("C:/SYMPHONY_VODKAS/temp/dupa")
B = Path("J:/test_RES/aaa")
copy_folder(A, B)