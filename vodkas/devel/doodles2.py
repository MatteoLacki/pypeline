%load_ext autoreload
%autoreload 2
from urllib.request import Request, urlopen
from vodkas.remote.sender import Sender
from pathlib import Path
import pandas as pd
import json
from vodkas.simple_db import SimpleDB
json.dumps()

s = Sender('Test', '0.0.0.0')

X = s.get_df()

X.columns
X.processing_computer_IP
X.project_idx

X.to_json()

Y = pd.DataFrame({'no':[1,2], 'path':[Path('~/ha'), Path('~/hi')]})
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