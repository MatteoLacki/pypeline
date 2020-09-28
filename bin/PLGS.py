import argparse
import json
import logging
from pathlib import Path
import pprint
import sys

from fs_ops.csv import rows2csv
from fs_ops.paths import find_folders

from waters.parsers import get_search_stats

from vodkas import apex3d, peptide3d, iadbs
from vodkas.config_parser import AdvConfigParser
from vodkas.header_txt import parse_header_txt
from vodkas.logging_alco import get_log_sender_logFun
from vodkas.xml_parser import create_params_file

ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)

ap.add_argument('config_path',
                help="Path to a config file with pipeline parameters.")

ap.add_argument('raw_folders',
                type=Path,
                nargs='+',
                help='Path(s) to raw folder(s), or paths that will be recursively searched for ".raw" folders.')

ap.add_argument('--verbose',
                help='Be verbose.',
                action='store_true')

ap.add_argument('--DEBUG',
                help='DEBUG',
                action='store_true')

ap = ap.parse_args()

if ap.DEBUG:
    print('Args:')
    pprint.pprint(ap.__dict__)
    print()

config     = AdvConfigParser(ap.config_path)
ip, port   = config.get_ip_port()
log_file   = config.get_log_file()
fasta_path = config.get_fasta_path()
iadbs_kwds = config.get_foo_args(iadbs)

log, sender, logFun = get_log_sender_logFun(log_file,
                                            'PLGS.py',
                                            'PLGS' if not ap.DEBUG else 'PLGS_DEBUG',
                                            ip, port)

# logging input-output of these functions:
apex3d, peptide3d, iadbs, create_params_file, get_search_stats = \
    [logFun(f) for f in [apex3d, peptide3d, iadbs, create_params_file, get_search_stats]]

raw_folders = list(find_folders(ap.raw_folders))
assert len(raw_folders), "No raw folders passed."
log.info(f"analyzing folders: {' '.join(str(x) for x in raw_folders)}")


for raw_folder in raw_folders:
    try:
        sender.update_group(raw_folder)
        
        acquired_name = raw_folder.stem
        header_txt = parse_header_txt(raw_folder/'_HEADER.TXT')
        sample_set = header_txt['Sample Description'][:8]
        #                   C:/SYMPHONY_PIPELINE/2019-008/O191017-04
        local_folder = local_output_folder/sample_set/acquired_name
        a = apex3d(raw_folder, local_folder,**apex3d_kwds)
        if peptide3d_kwds['timeout'] >= 0:
            p = peptide3d(a.with_suffix('.bin'), local_folder,**peptide3d_kwds)
            if iadbs_kwds['timeout'] >= 0:
                i = iadbs(p, local_folder, fasta_file, parameters_file, **iadbs_kwds)
                if i is not None: 
                    params = create_params_file(a, p, i) # for projectizer2.0
                    with open(a.parent/"params.json", 'w') as f:
                        json.dump(params, f)
                    search_stats = get_search_stats(i)
                    rows2csv(i.parent/'stats.csv',
                             [list(search_stats), list(search_stats.values())])
        if net_folder:
            #                     Y:/RES/2019-008
            net_set_folder = Path(net_folder)/sample_set
            net_set_folder.mkdir(parents=True, exist_ok=True)
            # if reanalysing, the old folder is preserved, 
            # and a version number appended to the new one
            # e.g.              Y:/RES/2019-008/O191017-04
            # replaced with:    Y:/RES/2019-008/O191017-04__v1
            final_net_folder = find_free_path(net_set_folder/acquired_name)
            try: #replace that with the general save moving routine with check-sums
                move_folder(local_folder, final_net_folder)
                if local_folder.parent.exists() and not local_folder.parent.glob('*'):
                    local_folder.parent.rmdir()
                log.info(f"moved {raw_folder} to {final_net_folder}")
            except RuntimeError as e:
                log.warning(f"not copied '{raw_folder}': {repr(e)}")
        else:
            log.info(f"saved '{raw_folder}' locally") 
    except subprocess.TimeoutExpired as e:
        log.error(f"Timeout: {repr(e)}")
    except Exception as e:
        log.error(f"error: {repr(e)}")

log.info('PLGS finished.')