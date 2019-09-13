import logging
from time import sleep

from . import apex3d, peptide3d, iadbs
from .fastas import get_fastas
from .misc import call_info
from .xml_parser import extract_params_from_xmls


logger = logging.getLogger(__name__)


def plgs(raw_folder, out_folder, **kwds):
    """Run PLGS.

    A convenience wrapper around apex3d, peptide3d, and iaDBs.

    Args:
        raw_folder (str): Path to the raw folder acquired Waters data.
        out_folder (str): Path to folder for the output.
        kwds: named arguments for the apex3d, peptide3d, and iadbs.
    Returns:
        dict: parsed parameters from the xml files.
    """
    logger.info("Running plgs.")
    logger.info(call_info(locals()))
    fastas = get_fastas(**kwds)
    a, _ = apex3d(raw_folder, out_folder, **kwds)
    p, _ = peptide3d(a.with_suffix('bin'), out_folder,**kwds)
    i, _ = iadbs(p.with_suffix('xml'), out_folder, fastas, **kwds)
    extract_params_from_xmls(a, p, i)
    logger.info('PLGS finished.')
    # xml_params, params = parse_xmls(a, p, i)
    # with open(out/'params.json', 'w') as f:
    #     json.dump(params, f, indent=2) # for projectizer2.0

