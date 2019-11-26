from pathlib import Path
from subprocess import Popen, TimeoutExpired, run, PIPE
from time import time

from .logging import get_logger


logger = get_logger(__name__)



def run_win_proc(cmd,
                 timeout=10,
                 out_path=''):
    """Run a subprocess on Windows.

    Args:
        cmd (list): the command to be executed.
        timeout (float): Minute timeout for the command.
        out_path (str): Path to where to write stdout.
    """
    timeout_expired = False
    timeout *= 60 # minutes to seconds
    try:
        T0 = time()
        pr = Popen(cmd, stdout=PIPE)
        out, err = pr.communicate(timeout=timeout)
        runtime = (time() - T0)/60 # seconds to minutes
    except TimeoutExpired:
        kill = Path(cmd[1]).name
        kill = "Taskkill /IM {} /F".format(kill)
        _ = run(kill, capture_output=True)
        timeout_expired = True
        out = str.encode('Timeout Achieved.')
        logger.warning(f"Timeout achieved for P{kill}")

    if out_path:
        with open(out_path, 'wb') as f:
            _ = f.write(out)

    if timeout_expired:
        raise TimeoutExpired(' '.join(cmd),
                             timeout)

    return pr, runtime
