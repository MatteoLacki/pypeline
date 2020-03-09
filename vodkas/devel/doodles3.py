%load_ext autoreload
%autoreload 2
import json
from pathlib import Path
import sqlite3
import pandas as pd

from platform import system

from vodkas.remote.db import DB
from vodkas.json import dump2json
from vodkas.remote.sender import Sender, currentIP

s = Sender('Test', currentIP)
s.project_id
for i in range(100):
    s.log('test', {'haha':i, 'path':Path(f'{i}'), 'str': 'asdaa'})

for i in range(100):
    s = Sender('Test', currentIP)
    s.log('test', {'haha':i, 'path':Path(f'{i}'), 'str': 'asdaa'})

s = Sender('Test', currentIP)
for i in range(100):
    s.update_group(i)
    s.log('test', {'haha':i, 'path':Path(f'{i}'), 'str': 'asdaa'})


logs = s.list_logs()
l = logs[0]
l.date
l.group
pd.DataFrame((tuple(l) for l in logs), columns=logs[0]._fields)

info = pd.DataFrame((log[:-1] for log in logs))
log = logs[0]
log.value
info.columns = log._fields[:-1]
[type(l.value) for l in logs]
logs[-2]


pd.DataFrame([{'a':1}, {'a':2, 'b':{'asd':213}}])

rest = pd.DataFrame([log.value for log in logs])
return pd.concat([info, rest], axis=1)

log = logs[-1]
log[:-1]

df = s.all_logs_df()


from collections import namedtuple

X = namedtuple('X', 'x y')
a = X(1,2)
X(*json.loads(json.dumps(a)))


# s.query("SELECT name FROM sqlite_master WHERE type='table' AND name='{logs}';")

if system()=='Windows':
    dbpath = r'C:\SYMPHONY_VODKAS\simple.db'
else:
    dbpath = r'/home/matteo/SYMPHONY_VODKAS/simple.db'

db = DB(dbpath)
db.tables()
db.table_exist('logs')
list(db.iter_logs())
db.drop_logs()
db.tables()
db.create_logs_if_aint_there()
db.tables()
db.

for i in range(100):
    db.log(currentIP, i, 'test', 'input', dump2json({'haha':i, 'cipa':'tak'}))
list(db.iter_logs())

del db

db.get_free_project_id()