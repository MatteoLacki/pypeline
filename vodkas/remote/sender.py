from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from pathlib import Path
import pandas as pd


class Sender(object):
    def __init__(self,
                 name,
                 host='192.168.1.176',
                 port=8745, 
                 encoding="cp1251"):
        self.host = host
        self.port = port
        self._enc = encoding
        self.name = name
        try:
            self.id = self.__greet(self.name)
        except URLError:
            raise URLError('IP not OK.')

    def __socket(self, route, message):
        url = f"http://{self.host}:{self.port}/{route}"
        request = Request(url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        return urlopen(request, message)

    def __greet(self, greeting):
        """Greet the receiver."""
        greeting = json.dumps(greeting).encode(self._enc)
        with self.__socket('greet', greeting) as s:
            return json.loads(s.read())

    def send_df(self, df):
        df['__project_id__'] = self.id
        df['__name__'] = self.name
        print(df)
        df_json = df.to_json(default_handler=str).encode(self._enc) 
        with self.__socket('updateDB', df_json) as s:
            return json.loads(s.read())

    def send_dict(self, d):
        df = pd.DataFrame()
        df = df.append(d, ignore_index=True)
        self.send_df(df)

    def send_pair(self, key, value):
        self.send_dict({'key':key, 'value': json.dumps(value)})

    def get_df(self):
        with self.__socket('df', '""'.encode(self._enc)) as s:
            return pd.read_json(s.read())



if __name__ == '__main__':
    s = Sender(host='0.0.0.0')
    message = "Hello this is a test!"
    w = s.log(message)
    print(w)