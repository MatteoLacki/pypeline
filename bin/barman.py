import sqlite3
from flask import g, Flask, jsonify, make_response, request, abort
from pathlib import Path
from platform import system as OS

if OS() == 'Windows':
    DBpath = Path(r'C:\SYMPHONY_VODKAS\simple.db')
else:
    DBpath = Path(r'/home/matteo/SYMPHONY_VODKAS/simple.db')

HOST = '0.0.0.0'
PORT = 8745
app  = Flask(__name__)

def DB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(str(DBpath))
    return db

@app.route('/')
def index():
    return 'Vodkas are up and running.'

@app.route('/getnumber', methods=['POST'])
def getnumber():
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
            host=HOST,
            port=PORT,
            threaded=False)