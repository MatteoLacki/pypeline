from pathlib import Path
from filecmp import dircmp

from vodkas.fs import copy_folder, find_free_path, rm_tree

out_folder = source = Path(r"C:\SYMPHONY_VODKAS\temp\2019-008\O191017_10")
net_folder = target = find_free_path(Path(r"Y:\TESTRES\2019-008\O191017_10"))
comparison = dircmp(source, target)
move_folder(source, target)

