from itertools import chain
from pathlib import Path


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
    x = {'apex3d':dict(parse_xml_params(apex_xml)),
         'peptide3d':dict(parse_xml_params(pept_xml)),
         'iadbs':dict(parse_xml_params(work_xml))}
    flat = {p+k:v for p,w in 
            (('apex:','apex3d'),
             ('spec:','peptide3d'),
             ('work:','iadbs')) for k,v in x[w].items()}
    return x, flat
    

def extract_params_from_xmls(apex_xml, pept_xml, work_xml):
    params = {p+k:v for p,w in 
              (('apex:','apex3d'),
               ('spec:','peptide3d'),
               ('work:','iadbs')) for k,v in x[w].items()}
    with open() as f:
        json.dump(params)