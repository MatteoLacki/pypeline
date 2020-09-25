"""
Run RESEARCH with the symphony pipeline.

Convention: for the AdvConfigParser to work properly, it must be the case that
the doc-string of the iadbs and fasta_file must contain any of the entries in the config file, under the proper section.

E.g. section 'fasta_file' has 'updated_fastas_folder'.
This means, that 'updated_fastas_folder' should also be and argument of the 'fastas_file' function.

If some parameter ain't mentioned in the config file, then the default is used or the user is prompted for input.
"""
import argparse
import json
import logging
import pathlib
import pprint
import tqdm

from fs_ops.paths import find_suffixed_files
from fs_ops.csv import rows2csv

from waters.parsers import get_search_stats

from vodkas.config_parser import AdvConfigParser
from vodkas.iadbs import iadbs
from vodkas.logging_alco import get_sender_n_log_Fun
#TODO; move this to waters package
from vodkas.xml_parser import create_params_file


ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('config_path',
                help="Path to a config file with pipeline parameters.")
ap.add_argument('Pep3D_Spectrum_xml',
                type=pathlib.Path,
                nargs='+',
                help="Path(s) to outputs of Peptide3D. \
          If provided with a folder instead, \
          a recursive search for files matching '*_Pep3D_Spectrum.xml' is performed.")
ap.add_argument('--verbose',
                help='Be verbose.',
                action='store_true')
ap.add_argument('--DEBUG',
                help='DEBUG.',
                action='store_true')
ap = ap.parse_args()

if ap.DEBUG:
    print('Args:')
    pprint.pprint(ap.__dict__)
    print()

if ap.verbose:
    print('WARNING: THIS SCRIPT WILL OVERWRITE PREVIOUS *_IA_workflow.xml FILES, params.json, AND stats.csv')
    print('IT IS YOUR RESPONSIBILITY TO SAVE THEM IF YOU NEED THEM.')
    print('In nomine proteomii, amen!\n')

assert len(ap.Pep3D_Spectrum_xml), "Missing Peptide3D spectra."
xmls = list(find_suffixed_files(ap.Pep3D_Spectrum_xml, 
                                ['**/*_Pep3D_Spectrum.xml'],
                                ['.xml']))
if ap.DEBUG:
    print('xmls:')
    pprint.pprint(xmls)
    print()

# p = pathlib.Path('/home/matteo/Projects/vodkas')
# path = p/'tests/research_linux2.ini'
# config     = AdvConfigParser(path)
config     = AdvConfigParser(ap.config_path)
ip, port   = config.get_ip_port()
log_file   = config.get_log_file()
fasta_path = config.get_fasta_path()
iadbs_kwds = config.get_foo_args(iadbs)

logging.basicConfig(filename = log_file,
                    level    = logging.INFO,
                    format   = '%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
log = logging.getLogger('RESEARCH.py')
sender, logFun = get_sender_n_log_Fun(log, 'RESEARCH', ip, port)

# logging input-output of these functions:
iadbs, create_params_file, get_search_stats = \
    [logFun(f) for f in [iadbs, create_params_file, get_search_stats]]

assert len(xmls), log.error('No Peptide3D spectra xmls found.')

log.info(f"Analyzing folders: {' '.join(str(x) for x in xmls)}")
for xml in tqdm.tqdm(xmls):
    sender.update_group(xml)
    log.info(f"researching: {str(xml)}")
    try:
        iadbs_xml = iadbs(xml, xml.parent, fasta_path, verbose=ap.DEBUG, **iadbs_kwds)
        if iadbs_xml is not None:
            apex_out = iadbs_xml.parent/iadbs_xml.name.replace('_IA_workflow.xml', '_Apex3D.xml')
            params = create_params_file(apex_out, xml, iadbs_xml) # for projectizer2.0
            with open(iadbs_xml.parent/"params.json", 'w') as f:
                json.dump(params, f)
            search_stats = get_search_stats(iadbs_xml)
            rows2csv(iadbs_xml.parent/'stats.csv',
                     [list(search_stats), list(search_stats.values())])
    except Exception as e:
        log.warning(repr(e))
        print(e)
    print()
log.info("Search redone.")
