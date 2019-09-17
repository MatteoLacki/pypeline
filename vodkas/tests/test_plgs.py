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


from vodkas import apex3d
from pathlib import Path
pr = apex3d('a','b')
pr.communicate()
pr.poll()
pr.stderr

