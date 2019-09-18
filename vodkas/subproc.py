from pathlib import Path
from subprocess import Popen, TimeoutExpired, run, PIPE
from time import time


def run_win_proc(cmd,
                 timeout=10,
                 log = ""):
    """Run a subprocess on Windows.

    Args:
        cmd (list): the command to be executed.
        timeout (float): Minute timeout for the program execution.
        log (str): Path to where to write the log.
    """
    kill = Path(cmd[1]).name
    kill = "Taskkill /IM {} /F".format(kill)
    timeout *= 60 # seconds to minute
    try:
        if log:
            log = Path(log)
            log.parent.mkdir(parents=True, exist_ok=True)
            out = open(log, "w")
        else:
            out = None
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
    timeout *= 60 # seconds to minute
    try:
        T0 = time()
        pr = Popen(cmd, stdout=PIPE)
        out, err = pr.communicate(timeout=timeout)
        runtime = (time() - T0)*60
    except TimeoutExpired:
        kill = Path(cmd[1]).name
        kill = "Taskkill /IM {} /F".format(kill)
        _ = run(kill, capture_output=True)
        timeout_expired = True    

    if out_path:
        with open(out_path, 'wb') as f:
            _ = f.write(out)

    if timeout_expired:
        raise TimeoutExpired(' '.join(cmd),
                             timeout)

    return pr, runtime
