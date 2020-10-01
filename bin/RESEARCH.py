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
import subprocess
import tqdm

from fs_ops.paths import find_suffixed_files
from fs_ops.csv import rows2csv

from waters.parsers import get_search_stats

from vodkas.config_parser import AdvConfigParser
from vodkas.iadbs import iadbs
from vodkas.logging_alco import get_log_sender_logFun
#TODO; move this to waters package
from vodkas.xml_parser import create_params_file


ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('config_path',
                help="Path to a config file with pipeline parameters.")
ap.add_argument('Pep3D_Spectrum_xml',
                type=lambda p: pathlib.Path(p).expanduser().resolve(),
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

peptide3d_xmls = list(find_suffixed_files(ap.Pep3D_Spectrum_xml, 
                                ['**/*_Pep3D_Spectrum.xml'],
                                ['.xml']))
if ap.DEBUG:
    print('peptide3d_xmls:')
    pprint.pprint(peptide3d_xmls)
    print()



config     = AdvConfigParser(ap.config_path)
ip, port   = config.get_ip_port()
log_file   = config.get_log_file()
fasta_path = config.get_fasta_path()
iadbs_kwds = config.get_foo_args(iadbs)

log, sender, logFun = get_log_sender_logFun(log_file,
                                            'RESEARCH.py',
                                            'RESEARCH' if not ap.DEBUG else 'RESEARCH_DEBUG',
                                            ip,
                                            port)

assert len(peptide3d_xmls), log.error('No Peptide3D spectra xmls found.')


# logging input-output of these functions:
iadbs, create_params_file, get_search_stats = \
    [logFun(f) for f in [iadbs, create_params_file, get_search_stats]]

log.info(f"Analyzing folders: {' '.join(str(x) for x in peptide3d_xmls)}")
for peptide3d_xml in tqdm.tqdm(peptide3d_xmls):
    sender.update_group(peptide3d_xml)
    log.info(f"researching: {str(peptide3d_xml)}")
    local_folder = peptide3d_xml.parent

    try:
        iadbs_xml = iadbs(peptide3d_xml,
                          local_folder,
                          fasta_path,
                          verbose=ap.DEBUG,
                          **iadbs_kwds)

        if iadbs_xml is not None:
            apex_xml = local_folder/iadbs_xml.name.replace('_IA_workflow.xml', '_Apex3D.xml')

            #TODO: all of the below code should be done by a function
            # in the 'waters' package that would parse only the headers of the
            # bloody 'xmls'.
            params = create_params_file(apex_xml, peptide3d_xml, iadbs_xml) # for projectizer2.0
            with open(local_folder/"params.json", 'w') as f:
                json.dump(params, f)
            search_stats = get_search_stats(iadbs_xml)
            rows2csv(local_folder/'stats.csv',
                     [list(search_stats), list(search_stats.values())])
            # UP TILL HERE!
            log.info(f'Analyzed {str(peptide3d_xml)}.')

    except subprocess.TimeoutExpired as e:
        log.error(f"Reached timeout: {repr(e)}") 

    except Exception as e:
        log.warning(repr(e))


log.info("Search redone.")
