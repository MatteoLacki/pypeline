import pathlib


def path_check(path):
    """Check if the path exists."""
    path = pathlib.Path(path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f'File/Folder {path} does not exist.')
    return path