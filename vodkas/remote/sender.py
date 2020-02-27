from urllib.request import Request, urlopen
import json
from pathlib import Path
import pandas as pd


class Sender(object):
    def __init__(self, host='192.168.1.176', port=8745):
        self.host = host
        self.port = port

    def _establish_conn(self, where):
        url = f"http://{self.host}:{self.port}/{where}"
        request = Request(url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        return request

    def great(self, message):
        """Great the server.

        Args:
            message (str): The greating message.

        Returns:
            Projection index.
        """
        message = json.dumps(message).encode("cp1251")
        with urlopen(self._establish_conn('great'), message) as r:
            id_no = json.loads(r.read())
        return id_no

    def log(self, message):
        message = json.dumps(message).encode("cp1251") 
        with urlopen(self._establish_conn('log'), message) as r:
            ok = json.loads(r.read())
        return ok

    def df(self):
        message = json.dumps('').encode("cp1251") 
        with urlopen(self._establish_conn('df'), message) as r:
            df = pd.read_json(r.read())
        return df


if __name__ == '__main__':
    s = Sender(host='0.0.0.0')
    message = "Hello this is a test!"
    w = s.log(message)
    print(w)