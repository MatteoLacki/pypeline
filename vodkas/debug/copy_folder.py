from pathlib import Path

from vodkas.fs import copy_folder, find_free_path

network_db_folder = Path(r"Y:/TESTRES")
# p = Path(r"O:\RAW\O1910\O191017_19.raw")
# r = Path(r'Y:/TESTRES/O191017_19')
# copy_folder(p, r)

acquired_name = "O191017_18"
##                              Y:\RES\         2019-008\   O191017-04
# net_folder = find_free_path(network_db_folder/sample_set/acquired_name)
##                              Y:\RES\         O191017-04
out_folder = Path("C:\\SYMPHONY_VODKAS\\temp\\2019-008\\O191017_18")
net_folder = find_free_path(network_db_folder/acquired_name)
s = copy_folder(out_folder, net_folder)
