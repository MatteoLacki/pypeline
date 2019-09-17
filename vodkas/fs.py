import subprocess
from pathlib import Path
import platform


def cp(source, target, **kwds):
    """Copy a file, or rather synchornize it.

    On Windows, use robocopy.
    One would have to wrap the executables and use Wine on Linux.

    Args:
        source (Path or str): Path to the source.
        target (Path or str): Path to the target.
        kwds: named arguments for subprocess.run
    """
    s, t = Path(source), Path(target)
    assert platform.system() == 'Windows', "This command works only on Windows, as Symphony does."
    cmd = ['robocopy', str(s.parent), str(t), str(s.name)]
    return subprocess.run(cmd, **kwds)


def test_cp():
    if platform.system() == 'Windows':
        cp('C:/test_s/test.ref', 'C:/test_t')
        assert next(Path('C:/test_t').iterdir()) == Path('C:/test_t/test.ref')
        Path('C:/test_t/test.ref').unlink()


def copy_folder(source, target):
    cmd = ['robocopy', str(source), str(target),"/E"]
    return subprocess.run(cmd)



def random_folder_name(k=20):
    """Generate a random name for a folder.

    Args:
        k (int): The length of the out string.
    Returns:
        A folder names.
    """
    from random import choice
    from string import ascii_letters, digits
    return ''.join(choice(ascii_letters+digits) for n in range(int(k)))


def fastas(proteome, 
           fasta_db_server=r'X:/SYMPHONY_VODKAS/fastas/latest',
           fasta_db_local=r'C:/SYMPHONY_VODKAS/fastas',
           subprocess_run_kwds={},
           **kwds):
    """Get the path with the proper fastas.

    Args:
        proteome (str): the beginning of the fasta file.
        fasta_db_server (str): path to the fastas on the server.
        fasta_db_local (str): path to the local fastas.
        subprocess_run_kwds (dict): arguments for the subprocess.run.
        kwds: further arguments to subprocess.run used for copying.

    Returns:
        Path to the local fasta file.
    """
    f_loc = Path(fasta_db_local)
    f_ser = Path(fasta_db_server)
    try:
        f_ser = next(f_ser.glob(f"*/PLGS/{proteome}*.fasta"))
        if not (f_loc/f_ser.name).exists():
            # remove any older versions
            for f in f_loc.glob(f"{proteome}*.fasta"):
                f.unlink()
            # copy the newest version
            proc = cp(f_ser, f_loc, **subprocess_run_kwds)
        return f_loc/f_ser.name
    except StopIteration:
        raise FileNotFoundError(f'There is no file starting with "{proteome}" on the server under "{f_ser}".')


def check_algo(path_to_algorithm, 
               verbose=False):
    """Check if the algorithm's executable is there."""
    algo = Path(path_to_algorithm)
    assert algo.exists(), f"No '{algo}' found!"
    if verbose:
        print(f"Running {algo.name}")
    return algo
