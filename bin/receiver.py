import pandas as pd
from flask import g, Flask, jsonify, make_response, request, abort
import pandas as pd
from pprint import pprint
import platform
import sqlite3

from vodkas.simple_db import SimpleDB

DEFAULT_APP_PORT = 8745

if platform.system() == "Windows":
    DBpath = r'C:\SYMPHONY_VODKAS\logs\simple.db'
elif platform.system() == "Linux":
    DBpath = r'/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/simple.db'
else:
    raise OSError()

app = Flask(__name__)


def DB():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(str(DBpath))
    return db


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, sTRANGER!'


@app.route('/greet', methods=['POST'])
def receive_greeting():
    """Receive greeting from the sender."""
    if request.data:
        greeting = request.get_json()
        conn = DB()
        idx = next(conn.execute("SELECT MAX(__project__) FROM logs"))[0] + 1
        return jsonify(idx)

@app.route('/updateDB', methods=['POST'])
def updateDB():
    """Receive a pd.DataFrame and append it to existing data base.
    
    Returns:
        boolean: was all successfull.
    """
    # pprint(request.__dict__)
    if request.data:
        try:
            df = pd.read_json(request.data)
            df['__remote_IP__'] = request.remote_addr
            conn = DB()
            try:
                df.to_sql("logs", conn, if_exists='append')
            except sqlite3.OperationalError:
                db = pd.concat([
                    pd.read_sql_query(f"SELECT * FROM logs", conn), 
                    df.reset_index()], 
                    ignore_index=True)
                db.to_sql("log", conn, if_exists='replace', index=False)
            return jsonify(True)
        except Exception as e:
            print(e)
    return jsonify(False)


@app.route('/df', methods=['POST'])
def df():
    """Send the entire DB back."""
    conn = DB()
    df = pd.read_sql_query(f"SELECT * FROM logs", conn)
    return df.to_json()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is None:
        db.close()


if __name__ == '__main__':
    port = DEFAULT_APP_PORT
    app.run(debug=True,
            host='192.168.1.191',
            port=port,
            threaded=False)
