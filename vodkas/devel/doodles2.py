%load_ext autoreload
%autoreload 2
from urllib.request import Request, urlopen
from vodkas.remote.sender import Sender
import pandas as pd

s = Sender('0.0.0.0')
s.great('Test')
X = s.df()

X.columns
X.processing_computer_IP
X.project_idx