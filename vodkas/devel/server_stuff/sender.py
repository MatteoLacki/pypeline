import json
from urllib.request import Request, urlopen

if _name_ == '_main_':
    host = '0.0.0.0'
    port = 8745
    url = f"http://{host}:{port}/log"

    request = Request(url)
    request.add_header('Content-Type',
                    'application/json; charset=utf-8')

    body_request = {'Message': 'trial'}

    body_request = json.dumps(body_request).encode('utf-8')

    with urlopen(request, body_request) as response:
        body_response = response.read()