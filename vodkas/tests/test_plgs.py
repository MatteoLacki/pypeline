from vodkas.examples.PLGS import PLGS

# from vodkas.apex3d import apex3d
PLGS("C:/ms_soft/MasterOfPipelines/Data/O190302_01.raw", "human")


# from pathlib import Path
# raw_folder = Path("C:/ms_soft/MasterOfPipelines/Data/O190302_01.raw")
# proj_tag = raw_folder.name[:5]
# out_folder=Path("C:/SYMPHONY_VODKAS/temp")
# out_folder /= proj_tag


apex3d, peptide3d, iadbs, args = monitor(apex3d, peptide3d, iadbs)
args.json()


from vodkas.xml_parser import parse_xmls

x, flat =parse_xmls("C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_Apex3D.xml",
           "C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_Pep3D_Spectrum.xml",
           "C:/SYMPHONY_VODKAS/temp/O1903/O190302_01_IA_workflow.xml")
x
flat