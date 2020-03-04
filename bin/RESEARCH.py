import argparse
from docstr2argparse.parse import foo2argparse
import json
import logging
from pathlib import Path
import platform
from pprint import pprint
from tqdm import tqdm

from fs_ops.paths import find_suffixed_files

from vodkas.fastas import get_fastas
from vodkas.iadbs import iadbs
from vodkas.research import research


ap = argparse.ArgumentParser(description='Rerun search with iaDBs.',
                             epilog="WARNING: PREVIOUS '*_IA_Workflow.xml' SHALL BE DELETED ",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# ap.add_argument('--prompt', action='store_true', help='Prompt users for input.')
ap.add_argument('--log_file', type=lambda p: Path(p).expanduser().resolve(),
                help='Path to temporary outcome folder.',
                default={"Windows": 'C:/SYMPHONY_VODKAS/temp_logs/research.log',
                         "Linux":   '~/SYMPHONY_VODKAS/research.log',
                         "Darwin":  '~/SYMPHONY_VODKAS/research.log'}[platform.system()])

ap.add_argument('--server_ip', type=str, help='IP of the server', default='0.0.0.0')

get_fastas_kwds = foo2argparse(get_fastas, args_prefix='fastas_', get_short=False)
for n,o,h in get_fastas_kwds:
    if o == 'fastas_prompt':
        h['action'] = "store_true"
    ap.add_argument(n, **h)

iadbs_kwds = foo2argparse(iadbs, args_prefix='iadbs_', positional=False, get_short=False)
for n,o,h in iadbs_kwds:
    ap.add_argument('--iadbs_'+o,**h)

ap.add_argument('Pep3D_Spectrum', type=Path, nargs='+',
    help="Path(s) to outputs of Peptide3D. \
          If provided with a folder instead, \
          a recursive search for files matching '*_Pep3D_Spectrum.xml' is performed.")


args = ap.parse_args()
pprint(args.__dict__)

iadbs_kwds = {o: args.__dict__[n.replace('--','')] for n,o,h in iadbs_kwds}
get_fastas_kwds = {o: args.__dict__[n.replace('--','')] for n,o,h in get_fastas_kwds}

try: # translate fastas to NCBIgeneralFastas and store it on the server.
    iadbs_kwds['fasta_file'] = get_fastas(**get_fastas_kwds)
except FileNotFoundError:
    log.error(f"Fastas unreachable: {fastas_path}")

logging.basicConfig(filename=args.log_file,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:', 
                    level=logging.INFO)
log = logging.getLogger('RESEARCH.py')

xmls = list(find_suffixed_files(args.Pep3D_Spectrum, ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
print("analyzing folders:")
pprint(xmls)

# server = Sender('RESEARCH', server_ip)

for xml in tqdm(xmls):
    log.info(f"researching: {str(xml)}")
    try:
        iadbs_kwds['input_file'] = xml
        iadbs_kwds['output_dir'] = xml.parent
        # server.send_pair('iadbs_args', dump2json(iadbs_kwds))
        iadbs_out, _, runtime = iadbs(**iadbs_kwds)
        apex_out = iadbs_out.parent/iadbs_out.name.replace('_IA_workflow.xml', '_Apex3D.xml')
        create_params_file(apex_out, xml, iadbs_out) # for projectizer2.0
        search_stats = iaDBsXMLparser(iadbs_out).info()
        # server.send_pair("stats", dump2json(search_stats))
        rows2csv(iadbs_out.parent/'stats.csv', [list(search_stats), list(search_stats.values())])
    except Exception as e:
        log.warning(repr(e))
log.info("Search redone.")
