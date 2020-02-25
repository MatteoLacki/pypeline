from pathlib import Path
import pandas as pd
import sqlite3


class SimpleDB(object):
    """A trivial, extendible database used with pandas.DataFrames.

    The DB has only one table, that we want to extend."""
    
    def __init__(self, sqlite_path, tbl='logs'):
        """Instantiate the data base.

        Args:
            sqlite_path (str): Path to the database.
            tbl (str): Name of the main table in the DB.
        """
        self.conn = sqlite3.connect(str(sqlite_path))
        self.tbl = tbl

    def __del__(self):
        self.conn.close()

    def df(self):
        """Get the database as a pandas DataFrame.

        Returns:
            pd.DataFrame: Data Frame with all the entries from the database.
        """
        return pd.read_sql_query(f"SELECT * FROM {self.tbl}", self.conn)

    def append(self, df):
        """Append a data frame to the data base.

        Args:
            df (pd.DataFrame): DataFrame to append to the database's main table.
        """
        try:
            df.to_sql(tbl, self.conn, if_exists='append')
        except sqlite3.OperationalError:
            db = pd.concat([self.df(), df.reset_index()], ignore_index=True)
            db.to_sql(self.tbl, self.conn, if_exists='replace', index=False)

