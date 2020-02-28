# from time import sleep
from collections import defaultdict

from docstr2argparse.parse import ParserDisambuigationEasy
from fs_ops.csv import rows2csv
from waters.parsers import iaDBsXMLparser

from . import apex3d, peptide3d, iadbs
from .xml_parser import create_params_file

MOCK = True


def plgs(fastas,
         raw_folder,
         out_folder,
         apex3d_kwds={},
         peptide3d_kwds={},
         iadbs_kwds={}):
    """Run PLGS.

    Run complete PLGS analysis.

    Args:
        fastas (str): Path to fasta file.
        raw_folder (str): Path to the raw folder acquired Waters data.
        out_folder (str): Path to folder for the output.
        apex3d_kwds (dict): Arguments for apex3d.
        peptide3d_kwds (dict): Arguments for peptide3d.
        iadbs_kwds (dict): Arguments for iadbs.

    Returns:
        dict: parsed parameters from the xml files.
    """   
    a,_ = apex3d(raw_folder, out_folder, **apex3d_kwds) # this will make .bin only
    p,_ = peptide3d(a.with_suffix('.bin'), out_folder,**peptide3d_kwds) # this will make .xml only
    i,_ = iadbs(p, out_folder, fastas, **iadbs_kwds)
    create_params_file(a, p, i) # for projectizer2.0
    search_stats = iaDBsXMLparser(i).info()
    rows2csv(i.parent/'stats.csv', [list(search_stats), list(search_stats.values())])


plgs.parsed = ParserDisambuigationEasy([apex3d, peptide3d, iadbs])