from pathlib import Path

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fs import cp
from vodkas.misc import monitor


def PLGS(raw_folder,
         proteome,
         temp_folder="C:/Symphony/Temp/test",
         parameters_file="X:/SYMPHONY_VODKAS/search/251.xml",
         fastas_kwds={},
         apex_kwds={},
         pep3d_kwds={},
         iadbs_kwds={},
         debug=False,
         kwds):
    """Run PLGS.

    A convenience wrapper around apex3d, peptide3d, and iaDBs.

    Args:
        raw_folder (Path or str): a path to the input folder with raw Waters data.
        fasta_file (Path or str): Path to the fasta file used in iaDBs peptide search.
        out_folder (Path or str): Path to where to place the output.
        parameters_file (Path or str): Path to the search parameters used in iaDBs peptide search.
        apex_kwds (dict): Other named arguments to apex3d.
        pep3d_kwds (dict): Other named arguments to peptide3d.
        iadbs_kwds (dict): Other named arguments to iaDBs.
        subprocess_run_kwds (dict): arguments for the subprocess.run.
        debug (boolean): Debug mode.

    Returns:
        Paths to folder with results.
    """
    raw_folder = Path(raw_folder)
    out_folder = Path(out_folder)
    fasta_file = fastas(proteome, **fastas_kwds)
    parameters_file = Path(parameters_file)

    if debug:
        print(raw_folder)
        print(out_folder)
        print(fasta_file)
        print(parameters_file)

    apex3d, peptide3d, iadbs, args = monitor(apex3d, peptide3d, iadbs)

    apexOutPath, apex_proc = apex3d(raw_folder, 
                                    out_folder,
                                    write_binary=True,
                                    capture_output=True,
                                    **apex_kwds)

    apexOutBIN = apexOutPath.with_suffix('.bin')
    pep3dOutPath, pep_proc = peptide3d(apexOutBIN,
                                       out_folder,
                                       write_binary=True,
                                       min_LEMHPlus=350.0,
                                       capture_output=True,
                                       **pep3d_kwds)

    pep3dOutXML = pep3dOutPath.with_suffix('.xml')
    iadbsOutXML, iadbs_proc = iadbs(pep3dOutXML,
                                    out_folder, 
                                    fasta_file=fasta_file,
                                    parameters_file=parameters_file,
                                    capture_output=True,
                                    **iadbs_kwds)

    args.json()

    return apexOutBIN, pep3dOutXML, iadbsOutXML

    