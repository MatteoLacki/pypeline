import pandas as pd
from flask import Flask, jsonify, make_response, request, abort
import pandas as pd

from vodkas.simple_db import SimpleDB

DEFAULT_APP_PORT = 8745
DB = SimpleDB('/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/logs.db')
app = Flask(__name__)


@app.route('/great', methods=['POST'])
def receive_greating():
    """Receive greating from the sender."""
    if request.data:
        body = request.get_json()
        print(body)
        print(request.remote_addr)
    return jsonify(len(DB))


@app.route('/log', methods=['POST'])
def receive_log():
    """Receive logs send to that url

    Example:
        curl -i -H "Content-Type: application/json" -X PUT http://localhost:8744/log -d '{"force_recalculation_forecast_db":"True", "ssh_tunnel_production":"True"}'
    """
    if request.data:
        log = request.get_json()
        log['processing_computer_IP'] = str(request.remote_addr)
        print(log)
        row = pd.DataFrame()
        row = row.append(log, ignore_index=True)
        DB.append(row)
    return jsonify(True)


@app.route('/df', methods=['POST'])
def df():
    """Receive logs send to that url

    Example:
        curl -i -H "Content-Type: application/json" -X PUT http://localhost:8744/log -d '{"force_recalculation_forecast_db":"True", "ssh_tunnel_production":"True"}'
    """
    return DB.df().to_json()



if __name__ == '__main__':
    port = DEFAULT_APP_PORT
    app.run(debug=False,
            host='0.0.0.0',
            port=port,
            threaded=False)
