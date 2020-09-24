%load_ext autoreload
%autoreload 2
from collections import defaultdict
import configparser
import pathlib

from docstr2argparse.parse import parse_google
from furious_fastas.protogui import fasta_path_gui, get_pipeline_fasta_path, check_updated_fastas_folder

from vodkas.iadbs import iadbs
from vodkas.config_parser import get_config_values

p = pathlib.Path('/home/matteo/Projects/vodkas')
path = p/'tests/research_linux.ini'


# def parse_research_config(path):
config = configparser.ConfigParser()
out = config.read(path)
assert len(out) == 1, "Something is fishy about the config."

iadbs_kwds = get_config_values(iadbs, config)

log_file = pathlib.Path(config['logging']['log_file']).expanduser().resolve()
ip, port = config['logging']['log_server_ip_port'].split(':')
port = int(port)


fasta_path = config['fastas'].get('fastas',None)
updated_fastas_folder = config['fastas'].get('updated_fastas_folder', None)


fasta_path = fasta_path_gui(updated_fastas_folder)

check_updated_fastas_folder(updated_fastas_folder)


# write a test around that
get_pipeline_fasta_path('human', True,  False, updated_fastas_folder)
get_pipeline_fasta_path('human', False, False, updated_fastas_folder)
get_pipeline_fasta_path('human', False, True,  updated_fastas_folder)
get_pipeline_fasta_path('human', True,  True,  updated_fastas_folder)

get_pipeline_fasta_path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', False,  False, updated_fastas_folder,
    True)
get_pipeline_fasta_path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', True,  False, updated_fastas_folder,
    True)
get_pipeline_fasta_path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', True, True, updated_fastas_folder,
    True)
get_pipeline_fasta_path('~/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', True, True, updated_fastas_folder,
    True)


path_or_tag, updated_fastas_folder, add_contaminants, reverse = \
    fasta_path_gui(updated_fastas_folder)
fasta_path = get_pipeline_fasta_path(path_or_tag,
                                     add_contaminants,
                                     reverse,
                                     updated_fastas_folder)

# pathlib.Path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta').exists()