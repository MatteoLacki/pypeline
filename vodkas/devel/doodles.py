%load_ext autoreload
%autoreload 2
from docstr2argparse.parse import get_positional_or_keyword_params
from docstr2argparse.parse import defaults, parse_google, foo2argparse
from vodkas.fastas import get_fastas
from vodkas.plgs import plgs

from vodkas.fs import cp

defaults(plgs)
defaults(get_fastas)
get_positional_or_keyword_params(plgs)
parse_google(plgs.__doc__)
foo2argparse(plgs)

from vodkas.fastas import get_proteome
from pathlib import Path

fastas = 'human'
fastas_db = Path(r'X:/SYMPHONY_VODKAS/fastas/latest')

