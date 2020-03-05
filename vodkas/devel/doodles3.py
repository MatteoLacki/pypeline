%load_ext autoreload
%autoreload 2
import json
from pathlib import Path
import sqlite3
import pandas as pd

from vodkas.remote.db import DB
from vodkas.json import dump2json
from vodkas.remote.sender import Sender, currentIP

s = Sender('Test')
s.project_id
for i in range(100):
    s.log('test', {'haha':i, 'path':Path(f'{i}'), 'str': 'asdaa'})
logs = s.get_all_logs()
log = logs[-1]
log[:-1]

df = s.all_logs_df()


# s.query("SELECT name FROM sqlite_master WHERE type='table' AND name='{logs}';")


db = DB(r'/home/matteo/SYMPHONY_VODKAS/simple.db')
db.tables()
db.table_exist('logs')
list(db.iter_logs())
db.drop_logs()
db.tables()
db.create_logs_if_aint_there()
db.tables()

for i in range(100):
    db.log(currentIP, i, 'test', 'input', dump2json({'haha':i, 'cipa':'tak'}))
list(db.iter_logs())

del db

db.get_free_project_id()