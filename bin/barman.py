import argparse
from flask import g, Flask, jsonify, request
from platform import system as OS
import socket

from vodkas.remote.db import DB
from vodkas.json import dump2json


DEBUG = True
currentIP = socket.gethostbyname(socket.gethostname())

############################################################### CLI 
ap = argparse.ArgumentParser(description='Let the barman take care of the symphony of vodkas.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('--host',
                help="Host's IP.",
                default=currentIP)
ap.add_argument('--port', 
                help='Port to listen to.', 
                default=8745, 
                type=int)
ap.add_argument('--DBpath',
                help='Port to listen to.',
                default=r'C:\SYMPHONY_VODKAS\simple.db' if OS() == 'Windows' else r'/home/matteo/SYMPHONY_VODKAS/simple.db')
args = ap.parse_args()
############################################################### Flask


app  = Flask(__name__)

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = DB(args.DBpath)
    return db

@app.route('/')
def index():
    return 'Vodkas: get ready to party.'

@app.route('/get_project_id', methods=['POST'])
def get_project_id():
    if request.data:
        if DEBUG:
            print(request.data)
        db = get_db()
        return jsonify(db.get_free_project_id())

@app.route('/log', methods=['POST'])
def log():
    if request.data:
        l = request.get_json()
        if DEBUG:
            print(l)
        db = get_db()
        db.log(*l)
        return jsonify(True)

@app.route('/get_all_logs', methods=['POST'])
def get_all_logs():
    if request.data:
        db = get_db()
        logs = list(db.iter_logs())
        return dump2json(logs)

@app.route('/query', methods=['POST'])
def query():
    if request.data:
        sql = request.get_json()
        out = queryDB(sql)
        return jsonify(out)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        del db


############################################################### MAIN
if __name__ == '__main__':
    app.run(debug=DEBUG,
            host=args.host,
            port=args.port,
            threaded=True)