from pathlib import Path
from subprocess import Popen, TimeoutExpired, run, PIPE
from time import time


def run_win_proc(cmd,
                 timeout=10,
                 log = ""):
    """Run a subprocess on Windows.

    Args:
        cmd (list): the command to be executed.
        timeout (float): Timeout for the program execution.
        log (str): Path to where to write the log.
    """
    kill = Path(cmd[1]).name
    kill = "Taskkill /IM {} /F".format(kill)
    try:
        out = open(log, "w") if log else None
        T0 = time()
        pr = Popen(cmd, stdout=out)
        pr.communicate(timeout=timeout)
        runtime = time() - T0
        if log:
            out.close()
    except TimeoutExpired:
        _ = run(kill, capture_output=True)
        raise TimeoutExpired(' '.join(cmd),
                             timeout)
    return pr, runtime