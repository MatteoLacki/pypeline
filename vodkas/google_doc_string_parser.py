import re


def _parse_google_argument_name(arg):
    """Parse google arguments."""
    try:
        arg_type = next(re.finditer(r'\(.*?\)', arg)).group(0)
        arg = arg.replace(arg_type, '')
        arg_type = arg_type[1:-1]
    except StopIteration:
        arg_type = None
    arg = arg.strip()
    return arg, arg_type


def parse_google(docstring, trim=True):
    """Parse google style of doctring.

    This is defined as by Sphinx.Napoleon package.

    Args:
        docstring (str): Docstring to parse.
        trim (boolean): Should only existing entries be returned?

    Returns:
        dict: All parameters parsed.
    """
    o = {}
    o['Args'] = o['Arguments'] = []
    o['Attributes'] = []
    o['Example'] = []
    o['Examples'] = []
    o['Keyword Args'] = o['Keyword Arguments'] = []
    o['Methods'] = []
    o['Note'] = []
    o['Notes'] = []
    o['Other Parameters'] = []
    o['Return'] = o['Returns'] = []
    o['Raises'] = []
    o['References'] = []
    o['See Also'] = []
    o['Todo'] = []
    o['Warning'] = o['Warnings'] = []
    o['Warns'] = []
    o['Yield'] = o['Yields'] = []
    # pat = r"\n\s*({}):\s*\n".format("|".join(o))
    pat = r"\n\s*(\S+):\s*\n"
    if docstring:
        split = re.split(pat, docstring)
        desc = split[0].split('\n')
        o['short_description'] = desc[0]
        o['long_description'] = " ".join(x for l in desc[1:] for x in l.split())
        for tag, args in zip(split[1::2], split[2::2]):
            assert tag in o, f"Group not specified in Splinx.Napoleon google-doc-style: '{tag}'"
            args = args.rstrip('\n ')
            for arg in args.split('\n'):
                arg_name, arg_desc = arg.split(':', 1)
                arg_desc = " ".join(arg_desc.split())
                arg_name, arg_type = _parse_google_argument_name(arg_name)
                o[tag].append((arg_name, arg_type, arg_desc))
    for k in list(o.keys()):
        if not o[k]:
            del o[k] 
    return o


def test_parse_google():
    docstring = """Little function.

    That does not help.
    Anybody. Anywhere.
    Is useless.

    Args:
        sadness (boolean): no nothing.
        pain (float): stay afloat.

    Returns:
        shit: specific one.
    """
    x = parse_google(docstring)
    y = {'Args': [('sadness', 'boolean', 'no nothing.'), ('pain', 'float', 'stay afloat.')], 'Arguments': [('sadness', 'boolean', 'no nothing.'),('pain', 'float', 'stay afloat.')],'Return': [('shit', None, 'specific one.')],'Returns': [('shit', None, 'specific one.')],'short_description': 'Little function.','long_description': 'That does not help. Anybody. Anywhere. Is useless.'}
    assert x == y, 'Parsing is wrong.'
