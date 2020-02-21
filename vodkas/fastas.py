from pathlib import Path
from furious_fastas import fastas, Fastas

from .fs import move


def get_fastas(fastas_path,
               fastas_db=r'X:/SYMPHONY_VODKAS/fastas/latest',
               add_contaminants=True,
               reverse_fastas=True):
    """Get proper fastas.

    Args:
        fastas_path (str): path to fasta file or one of the standard proteomes used, e.g. 'human'.
        fastas_db (str): Path to fastas DB: used when supplying reduced fasta names, e.g. 'human'.
        add_contaminants (boolean): Should we add in contaminants.
        reverse_fastas (boolean):Should we reverse the fastas.

    Returns:
        Path: path to the fastas.
    """
    standard_fastas = {p.stem.split('_')[0]:p for p in Path(fastas_db).glob(f"*/PLGS/*.fasta")}
    if str(fastas_path) in standard_fastas:
        outpath = standard_fastas[fastas_path]
    else:
        fastas_path = Path(fastas_path)
        if not fastas_path.exists():
            raise FileNotFoundError
        # TODO: if path is there, don't do all that!
        final_name = fastas_path.stem
        if add_contaminants:
            final_name += "_contaminated"
        if reverse_fastas:
            final_name += "_reversed"
        final_name += "_pipelineFriendly.fasta"
        outpath = fastas_path.parent/final_name
        if not outpath.exists():
            fs = fastas(fastas_path)
            if add_contaminants:
                from furious_fastas.contaminants import contaminants
                fs.extend(contaminants)
            fs_gnl = Fastas(f.to_ncbi_general() for f in fs)
            assert fs_gnl.same_fasta_types(), "Fastas are not in the same format."
            if reverse_fastas:
                fs_gnl.reverse()
            outpath = fastas_path.parent/(fastas_path.stem + '_contaminated_reversed_pipelineFriendly.fasta')
            fs_gnl.write(outpath)
    return outpath
