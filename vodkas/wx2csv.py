import subprocess
from pathlib import Path
import pandas as pd

import vodkas.default_paths as default


def wx2csv(input_file,
           output_file,
           path_to_wx2csv=default.wx2csvpath,
           debug=False,
           **kwds):
    """A wrapper around wx2csv.
    
    Args:
        input_file (Path or str): a path to *_IA_workflow.xml file containing outputs from the iaDBs search.
        output_file (Path or str): Path to where to place the output.
        path_to_wx2csv (Path or str): Path to the "wx2csv.jar" executable.
        debug (boolean): Debug mode.
        **kwds: other parameters for 'subprocess.run'.
    Returns:
        pandas.Dataframe
    """
    algo = str(Path(path_to_wx2csv))
    input_file, output_file = Path(input_file), Path(output_file)
    if input_file.suffix != '.xml':
        raise RuntimeError("Peptide3D failed: it accepts 'bin' input files only.")
    cmd = ["powershell.exe",
           "java -jar",
            algo,
            "-b -o {}".format(output_file),
            "-i {}".format(input_file)]
    if debug:
        print('wx2csv debug:')
        print(cmd)
    process = subprocess.run(cmd, **kwds)
    if kwds.get('capture_output', False):# otherwise no input was caught.
        log = output_file.parent/"wx2csv.log"
        log.write_bytes(process.stdout)
    if not output_file.exists():
        raise RuntimeError("wx2csv failed: output is missing")
    if process.stderr:
        print(process.stderr)
        raise RuntimeError("wx2csv failed: WTF")
    out = pd.read_csv(output_file)
    return out, process


def test_wx2csv():
    pd.set_option('display.max_rows', 4)
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_colwidth', -1)
    report, proc = wx2csv("C:/Symphony/Temp/proteome_tools/T1707/T170722_03/215/T170722_03_IA_workflow.xml",
        "C:/Symphony/Temp/proteome_tools/T1707/T170722_03/215/T170722_03.csv")
