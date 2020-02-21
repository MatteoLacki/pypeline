from pathlib import Path
import pandas as pd
import sqlite3



sqlite_path = Path('/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/logs.db')
conn = sqlite3.connect(str(sqlite_path))

X = pd.DataFrame({'a':[1,2,3], 'b':['1','2','3'], 'd':[1, 434, 34]}).set_index('a')
X.to_sql('logs', conn, index=True, index_label='a', if_exists='replace')
Y = pd.DataFrame({'a':[5,6,7], 'b':['1','2','3'], 'e':[1, 434, 34], 'c':['a','b','c']}).set_index('a')

try:
    Y.to_sql('logs', conn, if_exists='append')
except sqlite3.OperationalError:
    W = pd.read_sql_query(f"SELECT * FROM logs", conn, index_col='a')
    pd.concat([W,Y]).to_sql('logs', conn, if_exists='replace')
pd.read_sql_query(f"SELECT * FROM logs", conn, index_col='a')



# with sqlite.connect(str(sqlite_path)):
conn.close()