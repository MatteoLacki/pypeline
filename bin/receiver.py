import pandas as pd
from flask import Flask, jsonify, request
import pandas as pd
from pprint import pprint
import platform

from vodkas.simple_db import SimpleDB


HOST = '0.0.0.0'
PORT = 8745
app  = Flask(__name__)

if platform.system() == 'Windows':
    DB = SimpleDB('C:/SYMPHONY_VODKAS/simple.db')
else:
    DB = SimpleDB('/home/matteo/SYMPHONY_VODKAS/simple.db')


@app.route('/greet', methods=['POST'])
def receive_greeting():
    """Receive greeting from the sender."""
    if request.data:
        greeting = request.get_json()
        return jsonify(DB.get_new_index())


@app.route('/updateDB', methods=['POST'])
def updateDB():
    """Receive a pd.DataFrame and append it to existing data base.
    
    Returns:
        boolean: success
    """
    if request.data:
        try:
            df = pd.read_json(request.data)
            df['__remote_IP__'] = request.remote_addr
            print(df)
            DB.append(df)
            return jsonify(True)
        except Exception as e:
            print(e)
    return jsonify(False)


@app.route('/df', methods=['POST'])
def df():
    """Send the entire DB back."""
    return DB.df().to_json()


if __name__ == '__main__':
    app.run(debug=True,
            host=HOST,
            port=PORT,
            threaded=False)
