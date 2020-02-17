from time import sleep
from collections import defaultdict

from docstr2argparse.parse import foo2argparse
from fs_ops.csv import rows2csv
from waters.parsers import iaDBsXMLparser

from . import apex3d, peptide3d, iadbs
from .fastas import get_fastas
from .xml_parser import create_params_file



def plgs(raw_folder,
         out_folder,
         get_fastas_kwds,
         apex3d_kwds,
         peptide3d_kwds,
         iadbs_kwds):
    """Run PLGS.

    Run complete PLGS analysis.

    Args:
        raw_folder (str): Path to the raw folder acquired Waters data.
        out_folder (str): Path to folder for the output.
        get_fastas_kwds (dict): Arguments for get_fastas
        apex3d_kwds (dict): Arguments for apex3d.
        peptide3d_kwds (dict): Arguments for peptide3d.
        iadbs_kwds (dict): Arguments for iadbs.

    Returns:
        dict: parsed parameters from the xml files.
    """
    fastas = get_fastas(**fastas_kwds)
    a, _ = apex3d(raw_folder, out_folder, **apex3d_kwds) # this will make .bin only
    p, _ = peptide3d(a.with_suffix('.bin'), out_folder,**kwds) # this will make .xml only
    i, _ = iadbs(p.with_suffix('.xml'), out_folder, fastas, **kwds)
    create_params_file(a, p, i) # for projectizer2.0
    search_stats = iaDBsXMLparser(i).info()
    rows2csv(i.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
    return True


def parse_optional_plgs_args():
    """Parse plgs' documentation.
    
    Returns:
        tuple: arg_parser with filled documents and dictionary with arguments desambuigation.
    """
    foos = [get_fastas, apex3d, peptide3d, iadbs]
    plgs_desc, plgs_args = foo2argparse(plgs)
    plgs_args = {n:h for n,o,h in plgs_args}
    out = []
    arg2foo = defaultdict(list)
    for f in foos:
        for n,o,h in foo2argparse(f)[1]:
            if n[0:2] == '--':
                arg2foo[o].append((f.__name__, o))
    repeating_args = {a for a, f_l in arg2foo.items() if len(f_l) > 1}
    for arg in repeating_args:
        del arg2foo[arg]
    for f in foos:
        for n,o,h in foo2argparse(f)[1]:
            if n[0:2] == '--':
                if o in repeating_args:
                    m = f"{f.__name__}_{o}"
                    n = "--" + m
                    arg2foo[m].append((f.__name__, o))
                out.append((n,h))
    arg2foo = {k: v[0] for k,v in arg2foo.items()}
    return plgs_desc, out, dict(arg2foo)
