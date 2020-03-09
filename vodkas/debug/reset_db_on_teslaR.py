%load_ext autoreload
%autoreload 2
from vodkas.remote.sender import Sender
from pathlib import Path
import pandas as pd
from vodkas.remote.db import DB
from platform import system

s = Sender('Test')


if system()=='Windows':
    dbpath = r'C:\SYMPHONY_VODKAS\simple.db'
else:
    dbpath = r'/home/matteo/SYMPHONY_VODKAS/simple.db'

db = DB(dbpath)
db.tables()
db.table_exist('logs')

X = pd.DataFrame(db.iter_logs())
X.columns



# db.drop_logs()
# db.tables()
# db.create_logs_if_aint_there()
# db.tables()