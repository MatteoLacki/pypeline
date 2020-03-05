import argparse
from docstr2argparse.parse import foo2argparse
import json
import logging
from pathlib import Path
from platform import system
from pprint import pprint
from tqdm import tqdm

from fs_ops.paths import find_suffixed_files
from fs_ops.csv import rows2csv
from waters.parsers import get_search_stats

from vodkas.fastas import get_fastas
from vodkas.iadbs import iadbs
from vodkas.json import dump2json
from vodkas.logging import store_parameters
from vodkas.remote.sender import Sender, currentIP
from vodkas.xml_parser import print_parameters_file, create_params_file



######################################## CLI
ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
get_fastas_kwds = foo2argparse(get_fastas, args_prefix='fastas_', get_short=False)
for n,o,h in get_fastas_kwds:
    if o == 'prompt':
        h['action'] = "store_true"
    ap.add_argument(n, **h)
iadbs_kwds = foo2argparse(iadbs, args_prefix='iadbs_', positional=False, get_short=False)
for n,o,h in iadbs_kwds:
    if o == 'mock':
        h['action'] = "store_true"
        del h['type']
    ap.add_argument('--iadbs_'+o,**h)

ap.add_argument('Pep3D_Spectrum', type=Path, nargs='+',
    help="Path(s) to outputs of Peptide3D. \
          If provided with a folder instead, \
          a recursive search for files matching '*_Pep3D_Spectrum.xml' is performed.")

ap.add_argument('--log_file',
    type=lambda p: Path(p).expanduser().resolve(),
    help='Path to temporary outcome folder.',
    default= 'C:/SYMPHONY_VODKAS/temp_logs/research.log' if system() == 'Windows' else '~/SYMPHONY_VODKAS/research.log')


ap.add_argument('--server_ip', 
                type=str, 
                help='IP of the server',
                default=currentIP)

args = ap.parse_args()

######################################## Logging
logging.basicConfig(filename=args.log_file, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
log = logging.getLogger('RESEARCH.py')
sender = Sender('RESEARCH', args.server_ip) # what to do, if server is down???
print(sender.project_id)
# from vodkas.logging import MockSender
# sender = MockSender()
logFun = store_parameters(log, sender)
iadbs = logFun(iadbs)
create_params_file = logFun(create_params_file)
get_search_stats = logFun(get_search_stats)


# ######################################## PROTO GUI
parse_out_kwds = lambda p: {o: args.__dict__[n.replace('--','')] for n,o,h in p}
iadbs_kwds = parse_out_kwds(iadbs_kwds)
get_fastas_kwds = parse_out_kwds(get_fastas_kwds)

try: # translate fastas to NCBIgeneralFastas and store it on the server.
    iadbs_kwds['fasta_file'] = get_fastas(**get_fastas_kwds)
except FileNotFoundError:
    log.error(f"Fastas unreachable: {fastas_path}")
    error()

if args.fastas_prompt: # search file.
    search_params = iadbs_kwds['parameters_file']
    print(f'Default search parameters {search_params}:')
    print_parameters_file(search_params)
    iadbs_kwds['parameters_file'] = input(f'OK? ENTER. Not OK? Provide path here and hit ENTER: ') or search_params


######################################## RESEARCH 
xmls = list(find_suffixed_files(args.Pep3D_Spectrum, ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
print("analyzing folders:")
pprint(xmls)

for xml in tqdm(xmls):
    log.info(f"researching: {str(xml)}")
    try:
        iadbs_kwds['input_file'] = xml
        iadbs_kwds['output_dir'] = xml.parent
        iadbs_out,_ = iadbs(**iadbs_kwds)
        apex_out = iadbs_out.parent/iadbs_out.name.replace('_IA_workflow.xml', '_Apex3D.xml')
        params = create_params_file(apex_out, xml, iadbs_out) # for projectizer2.0
        search_stats = get_search_stats(iadbs_out)
        rows2csv(iadbs_out.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
    except Exception as e:
        log.warning(repr(e))
        print(e)
log.info("Search redone.")
