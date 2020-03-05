from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from pathlib import Path
import pandas as pd
import socket

from vodkas.json import dump2json
from vodkas.remote.db import LOG

currentIP = socket.gethostbyname(socket.gethostname())


class Sender(object):
    def __init__(self,
                 name,
                 host,
                 port=8745, 
                 encoding="cp1251"):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.name = name
        self.ip = socket.gethostbyname(socket.gethostname())
        self.project_id = self.__get_project_id()

    def __sock(self, route, message=None):
        url = f"http://{self.host}:{self.port}/{route}"
        request = Request(url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        if message is None:
            message = json.dumps(self.name).encode(self.encoding)
        return urlopen(request, message)

    def __get_project_id(self):
        with self.__sock('get_project_id') as s:
            return json.loads(s.read())

    def log(self, key, value):
        """Log key-value.
        
        Args:
            key (str): Parameter name.
            value (obj): Any serializable object.

        Returns:
            boolean: success?
        """
        _log = json.dumps((self.ip, 
                           self.project_id,
                           self.name, 
                           key, 
                           dump2json(value))).encode(self.encoding)
        with self.__sock('log', _log) as s:
            return json.loads(s.read())            

    def get_all_logs(self):
        with self.__sock('get_all_logs') as s:
            logs = []
            for date,ip,project_id,process_name,k,v in json.loads(s.read()):
                log = LOG(date,ip,project_id,process_name,k,json.loads(v))
                logs.append(log)
            return logs

    def all_logs_df(self):
        logs = self.get_all_logs()
        info = pd.DataFrame((log[:-1] for log in logs))
        log = logs[0]
        info.columns = log._fields[:-1]
        rest = pd.DataFrame((log.value) for log in logs)
        return pd.concat([info, rest], axis=1)


if __name__ == '__main__':
    s = Sender('Test', host=currentIP)
    print(s.project_id)
    print(s.all_logs_df())