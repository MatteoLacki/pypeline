import logging
from pathlib import Path

from .misc import get_coresNo, call_info


logger = logging.getLogger(__name__)


def get_fastas(proteome, 
               fasta_db_server=r'X:/SYMPHONY_VODKAS/fastas/latest',
               fasta_db_local=r'C:/SYMPHONY_VODKAS/fastas',
               **kwds):
    """Get the path to file with protein fastas.

    Args:
        proteome (str): Organism name = prefix of the fasta file.
        fasta_db_server (str): Path to server fastas.
        fasta_db_local (str): Path to local fastas.
        kwds: further arguments to subprocess.run used for copying.

    Returns:
        Path to the local fasta file.
    """
    logger.info('Running get_fastas.')
    logger.info(call_info(locals()))

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