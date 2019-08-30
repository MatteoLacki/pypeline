import json
from pathlib import Path

from vodkas.apex3d import apex3d
from vodkas.peptide3d import peptide3d
from vodkas.iadbs import iadbs
from vodkas.fs import copy_folder, fastas
from vodkas.xml_parser import parse_xmls


def _2xml(p):
    return p.with_suffix('.xml')

def _2bin(p):
    return p.with_suffix('.bin')


def plgs(raw_folder,
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
    raw = Path(raw_folder)
    out = Path(out_folder)
    net_out = Path(network_out_folder)
    proj_tag = raw.name[:5] # I1907, O1908, ...
    if proj_tag[0] in ('O','I'):
        out /= proj_tag
        if net_out:
            net_out /= proj_tag
    fas = fastas(proteome, **kwds)
    par_f = Path(parameters_file) # 215.xml, ...
    T = {}
    a_p, _, T['apex3d'] = apex3d(raw, out, **kwds)
    p_p, _, T['pep3d'] = peptide3d(_2bin(a_p), out, **kwds)
    i_p, _, T['iadbs'] = iadbs(_2xml(p_p), out, fas, par_f,**kwds)

    xml_params, params = parse_xmls(a_p, p_p, i_p)
    with open(out/'params.json', 'w') as f:
        json.dump(params, f, indent=2) # for projectizer2.0

    if net_out:
        copy_folder(out, net_out/proj_tag)

    xml_params['pep3d']['fasta'] = fas
    return xml_params, T