import argparse
import sqlite3
from flask import g, Flask, jsonify, make_response, request, abort
from pathlib import Path
from platform import system as OS
import socket

ap = argparse.ArgumentParser(description='Let the barman take care of the symphony of vodkas.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
currentIP = socket.gethostbyname(socket.gethostname())
ap.add_argument('--host', help='IP of the host.', default=currentIP)
ap.add_argument('--port', help='Port to listen to.', default=8745, type=int)
args = ap.parse_args()

def create_logs(conn):
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS logs (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

if OS() == 'Windows':
    DBpath = Path(r'C:\SYMPHONY_VODKAS\simple.db')
else:
    DBpath = Path(r'/home/matteo/SYMPHONY_VODKAS/simple.db')

app  = Flask(__name__)

def DB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(str(DBpath))
    return db

def query(q, args=(), one=False):
    with DB() as db:
        cur = db.execute(q, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return 'Vodkas are up and running.'

@app.route('/getnumber', methods=['POST'])
def getnumber():
    x = query('SELECT MAX(__project_id__) FROM logs')
    print(x)
    return jsonify(1)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/test', methods=['POST'])
def receive_greeting():
    """Receive greeting from the sender."""
    if request.data:
        print(DB())
        greeting = request.get_json()
        return jsonify('test')


if __name__ == '__main__':
    app.run(debug=True,
            host=args.host,
            port=args.port,
            threaded=False)