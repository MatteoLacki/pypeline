import pandas as pd
from flask import Flask, jsonify, make_response, request, abort

DEFAULT_APP_PORT = 8745

app = Flask(_name_)

@app.route('/log', methods=['POST'])
def receive_log():
    '''
    Receive logs send to that url

    Example:
    curl -i -H "Content-Type: application/json" -X PUT http://localhost:8744/log -d '{"force_recalculation_forecast_db":"True", "ssh_tunnel_production":"True"}'
    '''
#     print(request)
    if request.data:
        body = request.get_json()
        print(body)
        
    return jsonify({'status': 'done'})

if _name_ == '_main_':
    port = DEFAULT_APP_PORT

    app.run(debug=False,
            host='0.0.0.0',
            port=port,
            threaded=False)