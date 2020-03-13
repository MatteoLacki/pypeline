import subprocess
from pathlib import Path
import pandas as pd

from .logging import get_logger
from .subproc import run_win_proc


logger = get_logger(__name__)


def wx2csv(input_file,
           output_file,
           path_to_wx2csv=r"C:/SYMPHONY_VODKAS/bin/wx2csv.jar",
           java_minimal_heap_size='1G',
           **kwds):
    """A wrapper around wx2csv.
    
    Args:
        input_file (Path or str): a path to *_IA_workflow.xml file containing outputs from the iaDBs search.
        output_file (Path or str): Path to where to place the output.
        path_to_wx2csv (Path or str): Path to the "wx2csv.jar" executable.
        java_minimal_heap_size (str): Minimal heap size for jave.
        **kwds: other parameters for 'subprocess.run'.
    Returns:
        pandas.Dataframe
    """
    logger.info('Running wx2csv.')

    algo = Path(path_to_wx2csv)
    assert algo.exists(), "Executable is missing! '{}' not found.".format(algo)
    input_file, output_file = Path(input_file), Path(output_file)

    wx2csv_stdout = output_file.parent/'wx2csv.log'

    cmd = [f"powershell.exe",
           "java",
           f"-Xmx{java_minimal_heap_size}",
           f"-jar {algo}",
           f"-b -o {output_file}",
           f"-i {input_file}"]
    run_win_proc(cmd, 60, wx2csv_stdout)

    if not output_file.exists():
        raise RuntimeError("wx2csv failed: output is missing")
    out = pd.read_csv(output_file)

    logger.info(f'wx2csv took {runtime} minutes.')

    return out

