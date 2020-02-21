from urllib.request import Request, urlopen
import json
from pathlib import Path


class Sender(object):
	def __init__(self, host='192.168.1.176', port=8745):
		self.host = host
		self.port = port
		self.url = f"http://{host}:{port}/log"
		self.request = Request(self.url)
		self.request.add_header('Content-Type',
			'application/json; charset=utf-8')

	def send(self, message):
		message = json.dumps(message).encode("cp1251") 
		with urlopen(self.request, message) as r:
			ok = json.loads(r.read())
		return ok


###########################

#s = Sender()


#message = "Hello this is a test!"

#s.send(message)