from pathlib import Path
import pandas as pd
import sqlite3


class SimpleDB(object):
    def __init__(self, sqlite_path, tbl='logs'):
        self.conn = sqlite3.connect(str(sqlite_path))
        self.tbl = tbl

    def __del__(self):
        self.conn.close()

    def df(self):
        return pd.read_sql_query(f"SELECT * FROM {self.tbl}", self.conn)

    def append(self, df):
        try:
            df.to_sql(tbl, self.conn, if_exists='append')
        except sqlite3.OperationalError:
            db = pd.concat([self.df(), df.reset_index()], ignore_index=True)
            db.to_sql(self.tbl, self.conn, if_exists='replace', index=False)


# def test_db():
#     X = pd.DataFrame({'a':[1,2,3], 'b':['1','2','3'], 'd':[1, 434, 34]}).set_index('a')
#     X.to_sql('logs', conn, if_exists='replace')
#     db = SimpleDB(sqlite_path)
#     db.df()
#     db.append(df)
#     db.df()
#     for _ in range(100):
#         db.append(df)
#     db.df()
#     sqlite_path = Path('/home/matteo/Projects/vodkas/vodkas/devel/server_stuff/logs.db')
#     conn = sqlite3.connect(str(sqlite_path))
#     X = pd.DataFrame({'a':[1,2,3], 'b':['1','2','3'], 'd':[1, 434, 34]}).set_index('a')
#     X.to_sql('logs', conn, if_exists='replace')
#     df = pd.DataFrame({'a':[5,6,7], 'b':['1','2','3'], 'e':[1, 434, 34], 'c':['a','b','c']}).set_index('a')
#     df = X.copy()

