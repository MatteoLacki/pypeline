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
         **kwds):
    """Run PLGS.

    A convenience wrapper around apex3d, peptide3d, and iaDBs.

    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        proteome (str): prefix to the standard fasta file, e.g. human.
        out_folder (str): Path to where to temporary storage.
        network_out_folder (str): Path to where to place the output on the server.
        parameters_file (str): Path to the search parameters used in iaDBs peptide search.
        kwds: other named arguments.
    Returns:
        dict: parsed parameters from the xml files.
    """
    raw_folder = Path(raw_folder)
    out_folder = Path(out_folder)
    network_out_folder = Path(network_out_folder)
    proj_tag = raw_folder.name[:5]
    if proj_tag[0] in ('O','I'):
        out_folder /= proj_tag
    fasta_file = fastas(proteome, **kwds)
    parameters_file = Path(parameters_file)
    apexOut, _apex = apex3d(raw_folder, out_folder,**kwds)
    pep3dOut, _pep = peptide3d(apexOut.with_suffix('.bin'), out_folder, **kwds)
    iadbsOut, _iadbs = iadbs(pep3dOut.with_suffix('.xml'),
                             out_folder,
                             fasta_file,
                             parameters_file,
                             **kwds)    
    # for projectizer2.0
    xml_params, params = parse_xmls(apexOut, pep3dOut, iadbsOut)
    with open(out_folder/'params.json', 'w') as f:
        json.dump(params, f, indent=2)
    # move the whole folder to the final location
    copy_folder(out_folder, network_out_folder/proj_tag)
    return xml_params