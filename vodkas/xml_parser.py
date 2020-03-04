import xml.etree.cElementTree as ET
from itertools import chain
import json
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
    return params


def print_parameters_file(parameters_file):
    tree = ET.parse(parameters_file)
    root = tree.getroot()
    for h in root.iter('*'):
        if h.attrib:
            if 'VALUE' in h.attrib:
                print(h.tag, h.attrib['VALUE'])
    for digest in root.iter('DIGESTS'):
        for analysis_digestor in digest: 
            print(analysis_digestor.tag, analysis_digestor.attrib)
            for aa_seq_dig in analysis_digestor:
                print(aa_seq_dig.attrib['NAME'])
                for c in aa_seq_dig:
                    print(c.tag, c.attrib['AMINO_ACID'], c.attrib['POSITION'])        
    for modifier in root.iter('MODIFICATIONS'):
        for mod in modifier:
            print(mod.tag, mod.attrib['STATUS'])
            for l in mod:
                print(l.tag, l.attrib)

