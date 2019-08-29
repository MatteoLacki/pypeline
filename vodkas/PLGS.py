import json
from pathlib import Path

from vodkas.apex3d import apex3d
from vodkas.peptide3d import peptide3d
from vodkas.iadbs import iadbs
from vodkas.fs import copy_folder, fastas
from vodkas.xml_parser import parse_xmls


def PLGS(raw_folder,
         proteome,
         out_folder="C:/SYMPHONY_VODKAS/temp",
         network_out_folder="J:/test_RES",
         parameters_file="X:/SYMPHONY_VODKAS/search/215.xml",
         fastas_kwds={},
         apex_kwds={},
         pep3d_kwds={},
         iadbs_kwds={},
         json_args={},
         debug=False,
         **kwds):
    """Run PLGS.

    A convenience wrapper around apex3d, peptide3d, and iaDBs.

    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        proteome (str): prefix to the standard fasta file, e.g. human.
        out_folder (str): Path to where to temporary storage.
        network_out_folder (str): Path to where to place the output on the server.
        parameters_file (str): Path to the search parameters used in iaDBs peptide search.
        fastas_kwds (dict): Other named arguments to fastas. 
        apex_kwds (dict): Other named arguments to apex3d.
        pep3d_kwds (dict): Other named arguments to peptide3d.
        iadbs_kwds (dict): Other named arguments to iaDBs.
        json_args (dict): Arguments for the FuncState.json: where to save the json logs?
        debug (boolean): Debug mode.
        kwds: other named arguments.
    Returns:
        dict: parsed parameters from the xml files.
    """
    raw_folder = Path(raw_folder)
    out_folder = Path(out_folder)
    network_folder = Path(network_folder)
    proj_tag = raw_folder.name[:5]
    if proj_tag[0] in ('O','I'):
        out_folder /= proj_tag
    fasta_file = fastas(proteome, **fastas_kwds)
    parameters_file = Path(parameters_file)

    if debug:
        print(raw_folder, out_folder, fasta_file, parameters_file)
    apexOut, _apex = apex3d(raw_folder, out_folder,**apex_kwds)

    pep3dOut, _pep = peptide3d(apexOut.with_suffix('.bin'), out_folder, **pep3d_kwds)

    iadbsOut, _iadbs = iadbs(pep3dOut.with_suffix('.xml'),
                             out_folder,
                             fasta_file=fasta_file,
                             parameters_file=parameters_file,
                             **iadbs_kwds)    
    # for projectizer2.0
    xml_params, params = parse_xmls(apexOut, pep3dOut, iadbsOut)
    with open(out_folder/'params.json', 'w') as f:
        json.dump(params, f, indent=2)

    # move the whole folder to the final location
    copy_folder(out_folder, network_out_folder/proj_tag)

    return xml_params