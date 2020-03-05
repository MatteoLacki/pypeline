from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from pathlib import Path
import pandas as pd
import socket


currentIP = socket.gethostbyname(socket.gethostname())


class Sender(object):
    def __init__(self,
                 name,
                 host=currentIP,
                 port=8745, 
                 encoding="cp1251"):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.name = name
        self.id = self.getnumber(self.name)
        # try:
        #     self.id = self.__greet(self.name)
        # except URLError:
        #     raise URLError('IP not OK.')

    def __socket(self, route, message):
        url = f"http://{self.host}:{self.port}/{route}"
        request = Request(url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        return urlopen(request, message)

    def getnumber(self, greeting):
        """Greet the receiver."""
        greeting = json.dumps(greeting).encode(self.encoding)
        with self.__socket('getnumber', greeting) as s:
            return json.loads(s.read())

    def query(self, sql):
        sql = json.dumps(sql).encode(self.encoding)
        with self.__socket('query', sql) as s:
            return json.loads(s.read())        

    def send_df(self, df):
        df['__project_id__'] = self.id
        df['__name__'] = self.name
        df_json = df.to_json(default_handler=str).encode(self.encoding) 
        with self.__socket('updateDB', df_json) as s:
            return json.loads(s.read())

    def send_dict(self, d):
        df = pd.DataFrame()
        df = df.append(d, ignore_index=True)
        self.send_df(df)

    def send_pair(self, key, value):
        self.send_dict({'key':key, 'value': json.dumps(value)})

    def get_df(self):
        with self.__socket('df', '""'.encode(self.encoding)) as s:
            return pd.read_json(s.read())



if __name__ == '__main__':
    s = Sender(host=currentIP)
    message = "Hello this is a test!"
    w = s.log(message)
    print(w)