from itertools import chain


def parse_xml_params(path, prefix=""):
    """A quicker XML parser.

    Args:
        path,
        prefix (str): prefix to the name of the parameter.
    Yields:
        tuples (parameter, value).
    """
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


def parse_xmls(apex_xml, pept_xml, work_xml):
    yield from parse_xml_params(apex_xml, 'apex')
    yield from parse_xml_params(pept_xml, 'spec')
    yield from parse_xml_params(work_xml, 'work')