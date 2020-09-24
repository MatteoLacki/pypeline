%load_ext autoreload
%autoreload 2
from collections import defaultdict
import configparser
import pathlib

from docstr2argparse.parse import parse_google
from furious_fastas.protogui import fasta_file
from vodkas.iadbs import iadbs
from vodkas.config_parser import AdvConfigParser

from vodkas.google_doc_string_parser import parse_google

p = pathlib.Path('/home/matteo/Projects/vodkas')
path = p/'tests/research_linux.ini'

config     = AdvConfigParser(path)
# config     = AdvConfigParser(ap.config_path)
iadbs_kwds = config.get_foo_args(iadbs)
ip, port   = config.get_ip_port()
log_file   = config.get_log_file()
# fasta_path = config.get_fasta_path(True)

config.get_foo_args(fasta_file)


dict(config['fasta_file'])

config['fastas']['add_contaminants']



# def parse_research_config(path):
config = configparser.ConfigParser()
out = config.read(path)
assert len(out) == 1, "Something is fishy about the config."

iadbs_kwds = get_config_values(iadbs, config)
log_file   = pathlib.Path(config['logging']['log_file']).expanduser().resolve()
ip, port   = config['logging']['log_server_ip_port'].split(':')
port       = int(port)
fasta_path_or_tag     = config['fastas'].get('fastas',None)
updated_fastas_folder = config['fastas'].get('updated_fastas_folder', None)

fasta_path = get_fasta_file(fasta_path_or_tag, updated_fastas_folder, True, True)



fasta_path = fasta_path_gui(updated_fastas_folder)
check_updated_fastas_folder(updated_fastas_folder)

get_fasta_file(fasta_path_or_tag, updated_fastas_folder, True, True)
get_fasta_file(fasta_path_or_tag, updated_fastas_folder, True, False)
get_fasta_file(fasta_path_or_tag, updated_fastas_folder, False, False)
# get_fasta_file(fasta_path_or_tag, updated_fastas_folder, False, True)


get_fasta_file('~/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', updated_fastas_folder, True, False)

# # write a test around that
# get_pipeline_fasta_path('human', True,  False, updated_fastas_folder)
# get_pipeline_fasta_path('human', False, False, updated_fastas_folder)
# get_pipeline_fasta_path('human', False, True,  updated_fastas_folder)
# get_pipeline_fasta_path('human', True,  True,  updated_fastas_folder)

# get_pipeline_fasta_path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', False,  False, updated_fastas_folder,
#     True)
# get_pipeline_fasta_path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', True,  False, updated_fastas_folder,
#     True)
# get_pipeline_fasta_path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', True, True, updated_fastas_folder,
#     True)
# get_pipeline_fasta_path('~/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta', True, True, updated_fastas_folder,
#     True)


# path_or_tag, updated_fastas_folder, add_contaminants, reverse = \
#     fasta_path_gui(updated_fastas_folder)
# fasta_path = get_pipeline_fasta_path(path_or_tag,
#                                      add_contaminants,
#                                      reverse,
#                                      updated_fastas_folder)

# # pathlib.Path('/home/matteo/Projects/vodkas/tests/ecoli_4518_2020-09-22_17-17-31.fasta').exists()