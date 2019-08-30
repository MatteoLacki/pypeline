from vodkas.examples.PLGS import PLGS
from vodkas.xml_parser import parse_xmls
from pprint import pprint
from pathlib import Path

PLGS("C:/ms_soft/MasterOfPipelines/Data/O190302_01.raw", "human")

xml_params, params = parse_xmls("C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_Apex3D.xml",
           "C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_Pep3D_Spectrum.xml",
           "C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_IA_workflow.xml")

pprint(xml_params['apex3d'])
pprint(xml_params['apex3d'])


proj_tag = "O1903"
p = Path()
len(list(p.parent.glob(proj_tag)))


# there is a problem

raw_folder = 'C:/SYMPHONY_VODKAS/temp/O1903'
out_folder = 'C:/SYMPHONY_VODKAS/temp'
network_out_folder = 'J:/test_RES'


raw_folder = 'C:/SYMPHONY_VODKAS/temp/O1904'
out_folder = 'C:/SYMPHONY_VODKAS/temp'
network_out_folder = 'J:/test_RES'

raw = Path(raw_folder)
out = Path(out_folder)
net_out = Path(network_out_folder)
proj_tag = raw.name[:5]


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