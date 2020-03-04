from pathlib import Path
from furious_fastas import fastas, Fastas

from .fs import move


def get_fastas(path_or_tag='none',
               db=r'X:/SYMPHONY_VODKAS/fastas/latest',
               add_contaminants=True,
               reverse=True,
               prompt=False):
    """Get proper fastas.

    Args:
        path_or_tag (str): path to fasta file or one of the standard proteomes used, e.g. 'human'.
        db (str): Path to fastas DB: used when supplying reduced fasta names, e.g. 'human'.
        add_contaminants (boolean): Should we add in contaminants.
        reverse (boolean):Should we reverse the fastas.
        prompt (boolean): Prompt users for input.

    Returns:
        Path: path to the fastas.
    """
    standard_fastas = {p.stem.split('_')[0]:p for p in Path(db).glob(f"*/PLGS/*.fasta")}
    if prompt:
        path_or_tag = input('fastas to use (human|wheat|..|custom path): ')
        if str(path_or_tag) in standard_fastas:
            print(f"Selected: {path_or_tag}, stored under {standard_fastas[path_or_tag]}")
        else:
            print(f"Selected: {path_or_tag}")
            add_contaminants = input('Adding contaminants: to stop me write "no": ')
            add_contaminants = add_contaminants.lower() != 'no'
            print(f'Contaminants: {add_contaminants}')
            reverse = input('Reversing fastas: to stop me write "no": ')
            reverse = reverse.lower() != 'no'
            print(f'Reversing fastas: {reverse}')
    else:
        if path_or_tag == 'none':
            raise FileNotFoundError('You did not specify a path for fastas.')

    if str(path_or_tag) in standard_fastas:
        outpath = standard_fastas[path_or_tag]
    else:
        path_or_tag = Path(path_or_tag)
        if not path_or_tag.exists():
            raise FileNotFoundError('Path does not exist.')
        # TODO: if path is there, don't do all that!
        final_name = path_or_tag.stem
        if add_contaminants:
            final_name += "_contaminated"
        if reverse:
            final_name += "_reversed"
        final_name += "_pipelineFriendly.fasta"
        outpath = path_or_tag.parent/final_name
        if not outpath.exists():
            fs = fastas(path_or_tag)
            if add_contaminants:
                from furious_fastas.contaminants import contaminants
                fs.extend(contaminants)
            fs_gnl = Fastas(f.to_ncbi_general() for f in fs)
            assert fs_gnl.same_fasta_types(), "Fastas are not in the same format."
            if reverse:
                fs_gnl.reverse()
            outpath = path_or_tag.parent/(path_or_tag.stem + '_contaminated_reversed_pipelineFriendly.fasta')
            fs_gnl.write(outpath)
    return outpath
