%load_ext autoreload
%autoreload 2
from collections import defaultdict
import configparser
import pathlib

from docstr2argparse.parse import parse_google
from furious_fastas.protogui import fasta_file
from vodkas.iadbs import iadbs, write_params_xml_file
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

write_params_xml_file('/home/matteo/SYMPHONY_PIPELINE/215.xml')