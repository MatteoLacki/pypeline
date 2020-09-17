%load_ext autoreload
%autoreload 2
from urllib.request import Request, urlopen
from vodkas.remote.sender import Sender
from pathlib import Path
import pandas as pd
from pprint import pprint

s = Sender('Test', '192.168.1.214')
all_posts = s.list_logs()
len(all_posts)


pprint([p for p in all_posts if p.project_id == 18 and p.key=='iadbs:args'])
pd.DataFrame(all_posts)