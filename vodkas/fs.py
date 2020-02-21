import subprocess
from pathlib import Path
import platform
from filecmp import dircmp


ls = lambda p: list(p.glob('*'))

def __cp(source, target, fcmd):
    """robocopy wrapper

    Args:
        source (Path or str): Path to the source.
        target (Path or str): Path to the target.
        fcmd (lambda): function returning a string with command for the subprocess.
    """
    s, t = Path(source), Path(target)
    assert platform.system() == 'Windows', "This command works only on Windows, as Symphony does."
    if not s:
        raise FileNotFoundError("Source folder missing.")
    if not t.parents[0].exists():
        raise FileNotFoundError(f"Network drive missing: mount '{t.parents[0]}'.")
    cmd = fcmd(s,t)
    completed_proc = subprocess.run(cmd.split())
    # if completed_proc.returncode != 0:
    #     raise RuntimeError("The copy process did not succeed. Consult your local handsomely paid coder.")
    return completed_proc

def cp(source, target):
    """Copy a file, or rather synchronize it.

    On Windows, use robocopy.
    One would have to wrap the executables and use Wine on Linux.

    Args:
        source (Path or str): Path to the source.
        target (Path or str): Path to the target.
    """
    return __cp(source, target, lambda s,t: f"robocopy {str(s.parent)} {str(t)} {str(s.name)}")


def move(source, target):
    """Move a file, or rather synchronize it.

    On Windows, use robocopy.
    One would have to wrap the executables and use Wine on Linux.

    Args:
        source (Path or str): Path to the source.
        target (Path or str): Path to the target.
    """
    if platform.system() == 'Windows':
        return __cp(source, target, lambda s,t: f"robocopy {str(s.parent)} {str(t)} {str(s.name)} /move")
    else:
        import shutil
        shutil.move(str(source), str(target))


def test_cp():
    if platform.system() == 'Windows':
        cp('C:/test_s/test.ref', 'C:/test_t')
        assert next(Path('C:/test_t').iterdir()) == Path('C:/test_t/test.ref')
        Path('C:/test_t/test.ref').unlink()


def copy_folder(source, target):
    return __cp(source, target, lambda s,t: f"robocopy {str(s)} {str(t)} /E")


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
        q = p.parent/f"{p.name}__v{i}"
        # q = Path(f"{p.parent}__v{i}")/p.name
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


# def move_folder(source, target):
#     copying_finished = copy_folder(source, target)
#     comp = dircmp(source, target)
#     if copying_finished and not comp.diff_files: # no differences: delete!
#         rm_tree(source)

def move_folder(source, target):
    return __cp(source, target, lambda s,t: f"robocopy {str(s)} {str(t)} /e /move")


def network_drive_exists(path):
    """Check if network folder exists."""
    return Path(Path(path).parts[0]).exists()
