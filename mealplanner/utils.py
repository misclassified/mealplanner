import datetime

import pandas as pd
import numpy as np

import sqlite3
import os


class SqliteUtils(object):
    
    def __init__(self, db_local_path):
        self.db_local_path = db_local_path
        
        
    def get_all_tables(self):
        "Get all tables in sqlite database"

        conn = sqlite3.connect(self.db_local_path)

        cursorObj = conn.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursorObj.fetchall()
        conn.close()

        return tables
    
    
    def sqlite_to_pandas(self, query):
        """Execute a query on Sqlite database
        and returns it to a Pandas Dataframe
        """

        conn = sqlite3.connect(self.db_local_path)

        cursorObj = conn.cursor()
        cursorObj.execute(query)

        # Fetch all rows and write to df
        df = pd.DataFrame(cursorObj.fetchall())
        
        if df.shape[0] > 0:
            names = list(map(lambda x: x[0], cursorObj.description))
            df.columns = names

        conn.close()
        return df
    

    def drop_sqlite_table(self, table):
        "Drop a specific table in sqlite database"

        conn = sqlite3.connect(self.db_local_path)
        cursorObj = conn.cursor()

        # Create table
        cursorObj.execute('''DELETE FROM {}'''.format(table))
        conn.commit()
        conn.close()
        
        return None
    
    def get_columns_order(self, table):
        """Column names order can be a 
        bit impredictable in sqlite, we use a 
        function to extract names order
        """
        
        conn = sqlite3.connect(self.db_local_path)
        cursorObj = conn.cursor()
        cursorObj.execute('''select * from {}'''.format(table))
        
        names = list(map(lambda x: x[0], cursorObj.description))
        
        return names