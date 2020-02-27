import pandas as pd
from flask import Flask, jsonify, make_response, request, abort
import pandas as pd
from pprint import pprint

from vodkas.simple_db import SimpleDB

DEFAULT_APP_PORT = 8745
DB = SimpleDB('/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/simple.db')
app = Flask(__name__)


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
        boolean: was all successfull.
    """
    # pprint(request.__dict__)
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
    port = DEFAULT_APP_PORT
    app.run(debug=False,
            host='0.0.0.0',
            port=port,
            threaded=False)
