%load_ext autoreload
%autoreload 2
from pprint import pprint
from collections import OrderedDict, namedtuple
import logging

from docstr2argparse.parse import FooParser
from docstr2argparse.parse import defaults, parse_google, foo2argparse

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fastas import get_fastas
from vodkas.logging import store_parameters

foos = [get_fastas, apex3d, peptide3d, iadbs]
ARG = namedtuple('ARG', 'name o_name info')

FP = FooParser(foos)
pprint(FP)

FP['iadbs']['mock'].info['action'] = "store_true"
FP['iadbs']['mock'].info['action']
FP.parse_kwds({'iadbs_mock':True, 'apex3d_cuda':True, 'iadbs_path':'~/Symp'})
FP.kwds['iadbs']
FP['iadbs']

%load_ext autoreload
%autoreload 2
from fs_ops.paths import find_folders
from pathlib import Path

paths = [r'J:\collab_uni_Gutenberg']
p = paths[0]
p = p/'S1703/S170317_06.raw'


list(find_folders([r'J:\collab_uni_Gutenberg\S1703', r'J:\collab_uni_Gutenberg\T1405']))

from vodkas.fastas import fastas
from pathlib import Path
from platform import system

db_path = r'X:/SYMPHONY_VODKAS/fastas/latest' if system() == 'Windows' else r'/home/matteo/SYMPHONY_VODKAS/fastas/latest' 

def fastas_gui(db=db_path):
    standard_fastas = {p.stem.split('_')[0]:p for p in Path(db).glob(f"*/PLGS/*.fasta")}
    path = input('fastas to use (human|wheat|..|custom path): ')
    if str(path) in standard_fastas:
        print(f"Selected: {path}: {standard_fastas[path]}")
        out_path = standard_fastas[path]
        reverse = False
        add_contaminants = False
    else:
        if Path(path).exists():
            out_path = path
            print(f"Selected: {path}")
            add_contaminants = input('Adding contaminants: to stop me write "no": ')
            add_contaminants = add_contaminants.lower() != 'no'
            print(f'Contaminants: {add_contaminants}')
            reverse = input('Reversing fastas: to stop me write "no": ')
            reverse = reverse.lower() != 'no'
            print(f'Reversing fastas: {reverse}')
        else:
            raise FileNotFoundError('Fastas are not found')    
    return out_path, add_contaminants, reverse

def fastas(path,
           db=db_path,
           add_contaminants=True,
           reverse=True,
           prompt=False):
    """Get proper fastas.

    Args:
        path (str): path to fasta file or one of the standard proteomes used, e.g. 'human'.
        db (str): Path to fastas DB: used when supplying reduced fasta names, e.g. 'human'.
        add_contaminants (boolean): Should we add in contaminants.
        reverse (boolean):Should we reverse the fastas.
        prompt (boolean): Prompt users for input.

    Returns:
        Path: path to the fastas.
    """
    standard_fastas = {p.stem.split('_')[0]:p for p in Path(db).glob(f"*/PLGS/*.fasta")}
    

fastas_gui()
r"X:\SYMPHONY_VODKAS\fastas\latest\2020-3-2_2-0-11\PLGS\ecoli_4518_conts_172_2020-3-2_2-0-11.fasta"