from pathlib import Path

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fs import cp
from vodkas.misc import monitor
from vodkas.xml_parser import parse_xmls


def PLGS(raw_folder,
         proteome,
         temp_folder="C:/Symphony/Temp/test",
         parameters_file="X:/SYMPHONY_VODKAS/search/251.xml",
         fastas_kwds={},
         apex_kwds={},
         pep3d_kwds={},
         iadbs_kwds={},
         json_args={},
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
        json_args (dict): Arguments for the FuncState.json: where to save the json logs?
        debug (boolean): Debug mode.

    Returns:
        Paths to folder with results.
    """
    raw_folder = Path(raw_folder)
    out_folder = Path(out_folder)
    fasta_file = fastas(proteome, **fastas_kwds)
    parameters_file = Path(parameters_file)
    if debug:
        print(raw_folder, out_folder, fasta_file, parameters_file)
    apex3d, peptide3d, iadbs, args = monitor(apex3d, peptide3d, iadbs)
    apexOut, _apex = apex3d(raw_folder, out_folder,**apex_kwds)
    pep3dOut, _pep = peptide3d(apexOut.with_suffix('.bin'), 
                               out_folder, **pep3d_kwds)
    iadbsOut, _iadbs = iadbs(pep3dOut.with_suffix('.xml'),
                             out_folder,
                             fasta_file=fasta_file,
                             parameters_file=parameters_file,
                             **iadbs_kwds)
    args.json(**json_args)
    # params for the bloody projectizer2.0
    params = dict(parse_xmls(apexOut.with_suffix('.xml'),
                             pep3dOut.with_suffix('.xml'),
                             iadbsOut.with_suffix('.xml')))
    with open(params_path, 'w') as f:
        json.dump(params, f, indent=2)
    