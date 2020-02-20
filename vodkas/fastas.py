from pathlib import Path
from furious_fastas import fastas, Fastas

from .fs import move


def get_fastas(fastas,
               fastas_db=r'X:/SYMPHONY_VODKAS/fastas/latest',
               add_contaminants=True,
               reverse_fastas=True):
    """Get proper fastas.

    Args:
        fastas (str): Fasta file to use, or a prefix to one of the standard proteomes used, e.g. 'human'.
        fastas_db (str): Path to fastas DB: used when supplying reduced fasta names, e.g. 'human'.
        add_contaminants (boolean): Should we add in contaminants.
        reverse_fastas (boolean):Should we reverse the fastas.

    Returns:
        Path: path to the fastas.
    """
    standard_fastas = {p.stem.split('_')[0]:p for p in Path(fastas_db).glob(f"*/PLGS/*.fasta")}
    if str(fastas) in standard_fastas:
        fastas = standard_fastas[args.fastas]
    else:
        fastas = Path(fastas)
        if not fastas.exists():
            raise FileNotFoundError
        fs = fastas(p)
        if add_contaminants:
            from furious_fastas.contaminants import contaminants
            fs.extend(contaminants)
        fs_gnl = Fastas(f.to_ncbi_general() for f in fs)
        assert fs_gnl.same_fasta_types(), "Fastas are not in the same format."
        if reverse_fastas:
            fs_gnl.reverse()
        outpath = p.parent/(p.stem + '_contaminated_reversed_pipelineFriendly.fasta')
        fs_gnl.write(outpath)
        # local_tmp = Path('~').expanduser()
        # fs_gnl.write(local_tmp/outpath.name)
        # move(local_tmp/outpath.name, outpath)
        return outpath