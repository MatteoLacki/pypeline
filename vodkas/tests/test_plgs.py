from vodkas.examples.PLGS import PLGS
from vodkas.xml_parser import parse_xmls
from pprint import pprint

PLGS("C:/ms_soft/MasterOfPipelines/Data/O190302_01.raw", "human")

xml_params, params = parse_xmls("C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_Apex3D.xml",
           "C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_Pep3D_Spectrum.xml",
           "C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_IA_workflow.xml")

pprint(xml_params['apex3d'])
pprint(xml_params['apex3d'])


