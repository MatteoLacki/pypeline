%load_ext autoreload
%autoreload 2
from urllib.request import Request, urlopen
from vodkas.remote.sender import Sender
from pathlib import Path
import pandas as pd
import json
from vodkas.simple_db import SimpleDB


s = Sender('Test', '192.168.1.191')
X = s.get_df()

X.columns
X.processing_computer_IP
X.project_idx

X.to_json()

Y = pd.DataFrame({'no':[1,2], 'path':[Path('~/ha'), Path('~/hi')]})
Y.to_json(default_handler=str)
Y.path = [str(p) for p in Y.path]

x = pd.DataFrame()
x.append({'a':1, 'b':'sdas'}, ignore_index=True)

s.send_df(Y)
s.get_df()

DB = SimpleDB('/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/simple.db')

DB.append(pd.DataFrame())
pd.DataFrame()
.to_sql(DB.conn, 'logs', if_exists='replace')
del DB

p = Path('/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/simple.db')



json.dumps({'dasa': p}, cls=ComplexEncoder)



import matplotlib.pyplot as plt

X.columns
plt.plot(X.xml, X.peptide_cnt)
X[X['value'].str.contains('"acquired_name"', na = False)]

from fs_ops.paths import find_suffixed_files

p = Path(r'T:\RES\2018-065\rerun new vials')
list(find_suffixed_files([p], ['**/*_Pep3D_Spectrum.xml'], ['.xml']))
