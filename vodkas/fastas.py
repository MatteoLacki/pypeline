import logging
from pathlib import Path

from .misc import get_coresNo, call_info
from .fs import cp

logger = logging.getLogger(__name__)


def get_proteome(proteome, 
                 fasta_db_server=r'X:/SYMPHONY_VODKAS/fastas/latest',
                 fasta_db_local=r'C:/SYMPHONY_VODKAS/fastas',
                 **kwds):
    """Get the path to file with standard proteome fastas.

    Args:
        proteome (str): Organism name = prefix of the fasta file.
        fasta_db_server (str): Path to server fastas.
        fasta_db_local (str): Path to local fastas.
        kwds: further arguments to subprocess.run used for copying.

    Returns:
        Path to the local fasta file.
    """
    f_loc = Path(fasta_db_local)
    f_ser = Path(fasta_db_server)
    try:
        f_ser = next(f_ser.glob(f"*/PLGS/{proteome}*.fasta"))
        if not (f_loc/f_ser.name).exists():# remove old
            for f in f_loc.glob(f"{proteome}*.fasta"):
                f.unlink()
            proc = cp(f_ser, f_loc)# copy newest
        return f_loc/f_ser.name
    except StopIteration:
        raise FileNotFoundError(f'There is no file starting with "{proteome}" on the server under "{f_ser}".')


def get_fastas(fastas, 
               fasta_db_server=r'X:/SYMPHONY_VODKAS/fastas/latest',
               fasta_db_local=r'C:/SYMPHONY_VODKAS/fastas',
               **kwds):
    """Get the path to file with standard proteome fastas.

    Args:
        fastas (str): Fasta file to use, or a prefix to one of the standard proteomes used, e.g. 'human'.
        fasta_db_server (str): Path to server fastas.
        fasta_db_local (str): Path to local fastas.
        kwds: further arguments to subprocess.run used for copying.

    Returns:
        Path to the local fasta file.
    """
    if Path(fastas).is_file():
        logger.info('Custom fastas used.')
        logger.info(str(fastas))
        return Path(fastas)
    else:
        logger.info('Checking standard proteomes.')
        logger.info(call_info(locals()))
        return get_proteome(fastas,
                            fasta_db_server, 
                            fasta_db_local)

