import sqlite3
import pandas as pd

def getAll(conn, tName):
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT *
        FROM {tName}
        ''')
    
    return cursor.fetchall()

def load(df, dbname):
    if isinstance(df, list):
        querys = []
        for tName, df in df:
            conn = sqlite3.connect(dbname)
            df.to_sql(tName, conn, if_exists='replace')
            data = getAll(conn, tName)
            querys.append((f'{tName}', data))
            conn.close()
    return querys

