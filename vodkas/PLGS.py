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


def get_paths(raw_folder, out_folder, network_out_folder):
    """Get proper names for the folders.

    Checks, if the folder already exists somewhere.
    Maybe it's stupid. Maybe it should check if it existed before?
    """
    raw = Path(raw_folder)
    out = Path(out_folder)
    net_out = Path(network_out_folder)
    proj_tag = raw.name[:5]
    if proj_tag[0] in ('O','I'):
        used = {p.name for x in (out, net_out) for p in x.glob(proj_tag+'*')}
        if used:
            used_No = {int(t.split('_')[1]) for t in used if "_" in t}
            if (out/proj_tag).exists() or (net_out/proj_tag).exists():
                used_No.add(0)
            proj_tag = "{}_{}".format(proj_tag, max(used_No) + 1)
        out /= proj_tag
        if net_out:
            net_out /= proj_tag
    return raw, out, net_out


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
    raw, out, net_out = get_paths(raw_folder, out_folder, network_out_folder)
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
        copy_folder(out, net_out)
        for f in out.glob('*'):
            f.unlink() # cleaning temp after use
        out.rmdir()
    #todo: it might be wiser not to base the naming convention only
    # upon the existing folders. There should be some depot with all 
    # used names and it should be searched for the current entry and
    # should be updated.

    xml_params['apex3d']['local_raw_folder'] = str(out)
    xml_params['apex3d']['server_raw_folder'] = str(net_out)
    xml_params['peptide3d']['fasta'] = str(fas)
    
    return xml_params, T