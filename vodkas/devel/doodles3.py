%load_ext autoreload
%autoreload 2
from vodkas.remote.sender import Sender
from urllib.request import Request, urlopen
import json
from pathlib import Path
import sqlite3
import json

from vodkas.remote.db import DB
from vodkas.json import dump2json

Sender('test','0.0.0.0')

request = Request(f"http://0.0.0.0:8745/test")
request.add_header('Content-Type', 'application/json; charset=utf-8')
with urlopen(request, '""'.encode()) as s:
    print(json.loads(s.read()))

request = Request(f"http://0.0.0.0:8745/getnumber")
request.add_header('Content-Type', 'application/json; charset=utf-8')
with urlopen(request) as s:
    print(json.loads(s.read()))

%load_ext autoreload
%autoreload 2
from vodkas.remote.sender import Sender, currentIP

s = Sender('Test')
s.getnumber('Test')
s.query("SELECT name FROM sqlite_master WHERE type='table' AND name='{logs}';")




db = DB(r'/home/matteo/SYMPHONY_VODKAS/simple.db')
db.tables()
db.table_exist('logs')
list(db.iter_logs())
db.drop_logs()
db.tables()
db.create_logs_if_aint_there()
db.tables()
for i in range(100):
    db.log(i, 'test', 'input', dump2json({'haha':i, 'cipa':'tak'}))
list(db.iter_logs())

del db

db.get_free_project_id()