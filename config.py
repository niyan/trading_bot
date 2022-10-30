import mysql.connector
from mysql.connector.constants import ClientFlag
import pandas as pd
import csv

api_key = 'Bd6cQJVzf-WhB3Qpjhvb4PRCdzXCWovb'
api_secret = 'pIVPEultPdhzSuFQYiX6546FBqFRh_nJ'

configuration = {
    'database':'trading',
    'user':'root',
    'password': 'DzPrl9xeqL9v1e54',
    'host': '34.65.222.111'
}

conn = mysql.connector.connect(**configuration, buffered=True)
cursor = conn.cursor()
sql = """ USE trading """
cursor.execute(sql)
conn.commit

symbols = ['SUPERUSDT', 'GALAUSDT', 'TRXUSDT', 'WAVESUSDT', \
           'SHIBUSDT', 'YGGUSDT', 'CHZUSDT', 'OMGUSDT', 'GRTUSDT', 'DOGEUSDT']

posFrame = pd.DataFrame(symbols, columns=['symbol'])
posFrame['position'] = 0
posFrame['quantity'] = 0
posFrame.to_csv('positionCheck', index=False)
print(posFrame)



#for key, value in candles.items(): print(key, len(value), sep=" | ")
