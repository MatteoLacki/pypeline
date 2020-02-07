from itertools import chain
import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def parse_xml_params(path, prefix=""):
    """A quicker XML parser.

    Args:
        path,
        prefix (str): prefix to the name of the parameter.
    Yields:
        tuples (parameter, value).
    """
    path = Path(path).with_suffix('.xml')
    with open(path, 'r') as f:
        for l in f:
            if "PARAM NAME" in l:
                w = l.split('"')
                k = w[1]
                v = w[3]
                try:
                    v = v.replace(',','.')
                    v = float(v)
                except ValueError:
                    pass
                yield "{}{}".format(prefix, k), v
            if "</PARAMS>" in l:
                break


def iter_xmls(apex_xml, pept_xml, work_xml):
    yield from parse_xml_params(apex_xml, 'apex:')
    yield from parse_xml_params(pept_xml, 'spec:')
    yield from parse_xml_params(work_xml, 'work:')


def parse_xmls(apex_xml, pept_xml, work_xml):
    d_parse = lambda p: dict(parse_xml_params(p))
    x = {'apex3d':    d_parse(apex_xml),
         'peptide3d': d_parse(pept_xml),
         'iadbs':     d_parse(work_xml)}

    flat = {p+k:v for p,w in 
            (('apex:','apex3d'),
             ('spec:','peptide3d'),
             ('work:','iadbs')) for k,v in x[w].items()}

    return x, flat
    

def create_params_file(apex_xml, pept_xml, work_xml):
    """Create a params.json file for Projectizer2.0.

    This facilitates the creation of proper input for the IsoQuant (and PysoQuant).
    """
    logger.info('Parsing xml files for Projectizer2.0.')
    
    d_parse = lambda p: dict(parse_xml_params(p))
    x = {'apex3d':    d_parse(apex_xml),
         'peptide3d': d_parse(pept_xml),
         'iadbs':     d_parse(work_xml)}

    params = {p+k:v for p,w in 
              (('apex:','apex3d'),
               ('spec:','peptide3d'),
               ('work:','iadbs')) for k,v in x[w].items()}
    
    p = Path(apex_xml).parent/"params.json"
    with open(p, 'w') as f:
        json.dump(params, f, indent=2)
    
    logger.info(json.dumps(params))


