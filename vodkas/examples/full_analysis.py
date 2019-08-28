from pathlib import Path

from vodkas import apex3d, peptide3d, iadbs


def run_waters_pipeline(raw_folder,
                        fasta_file,
                        out_folder="C:/Symphony/Temp/test",
                        parameters_file="C:/Symphony/Search/251.xml",
                        apex_kwds={},
                        pep3d_kwds={},
                        iadbs_kwds={}):
    """Run Waters pipeline.

    A convenience wrapper around apex3d, peptide3d, and iaDBs.

    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        fasta_file (str): Path to the fasta file used in iaDBs peptide search.
        out_folder (str): Path to where to place the output.
        parameters_file (str): Path to the search parameters used in iaDBs peptide search.
        apex_kwds (dict): Other named arguments to apex3d.
        pep3d_kwds (dict): Other named arguments to peptide3d.
        iadbs_kwds (dict): Other named arguments to iaDBs.
    Returns:
        Paths to Apex3D, Peptide3D and iaDBs output files.
    """
    raw_folder = Path(raw_folder)
    out_folder = Path(out_folder)
    apexOutPath, apex_proc = apex3d(raw_folder, out_folder,
                                    write_binary=True,
                                    capture_output=True,
                                    **apex_kwds)
    apexOutBIN = apexOutPath.with_suffix('.bin')
    pep3dOutPath, pep_proc = peptide3d(apexOutBIN, out_folder,
                                       write_binary=True,
                                       min_LEMHPlus=350.0,
                                       capture_output=True,
                                       **pep3d_kwds)
    pep3dOutXML = pep3dOutPath.with_suffix('.xml')
    iadbsOutXML, iadbs_proc = iadbs(pep3dOutXML, out_folder, 
                                     fasta_file=Path(fasta_file),
                                     parameters_file=Path(parameters_file),
                                     capture_output=True,
                                     **iadbs_kwds)
    return apexOutBIN, pep3dOutXML, iadbsOutXML