import subprocess
from pathlib import Path
import platform


ls = lambda p: list(p.glob('*'))


def cp(source, target, **kwds):
    """Copy a file, or rather synchronize it.

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
    cmd = ['robocopy', str(source), str(target), "/E"]
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


def check_algo(path_to_algorithm):
    """Check if the algorithm's executable is there."""
    algo = Path(path_to_algorithm)
    assert algo.exists(), f"No '{algo}' found!"
    return str(algo)


def find_free_path(p):
    """Find the first free path for storing data by modifying the sample_set_no.

    Starting from: path/sample_set_no/acquired_name
    The procedure checks recursively if that path exists.
    If it does, append a free version number to sample_set_no.

    Args:
        p (str): Path to check and modify.
    """
    i = 0
    q = Path(p)
    while q.is_dir():
        i += 1
        q = Path(f"{p.parent}__v{i}")/p.name
    return q


def rm_tree(pth):
    """Removes recursively the folder and everything below in the file tree."""
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()