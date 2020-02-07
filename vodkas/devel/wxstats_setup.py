from pathlib import Path
from filecmp import dircmp

from vodkas.fs import copy_folder, find_free_path, rm_tree

out_folder = source = Path(r"C:\SYMPHONY_VODKAS\temp\2019-008\O191017_10")
list(out_folder.glob('*'))
iaDBs_xml = list(out_folder.glob('*_IA_workflow.xml'))[0]

import subprocess

C:\Symphony\Utils\wxStat.jar
stats.csv
target = iaDBs_xml

def wxStats(iaDBs_xml,
            path_to_wxStat="C:/SYMPHONY_VODKAS/plgs/wxStat.jar",
            java_minimal_heap_size='1G'):
    path_to_wxStat, iaDBs_xml = Path(path_to_wxStat), Path(iaDBs_xml)
    cmd = f"java -Xmx{java_minimal_heap_size} -jar {path_to_wxStat} {iaDBs_xml} > {iaDBs_xml.parent/'stats.csv'}"
    return subprocess.run(cmd.split())

