import requests, json
import datetime, time
import config
from config import api_key, api_secret
from config import conn, cursor
from pprint import pprint

class Client():
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_api = "https://api.fmfw.io/api/3"

    def authenticate(self):
        session = requests.session()
        session.auth = (config.api_key, config.api_secret)
        headers = {
            'apiKey' : config.api_key,
            'secretKey' : config.api_secret
        }
        return session

    def get_balance(self, symbol):
        url = self.base_api + "/spot/balance/" + symbol
        session = self.authenticate()
        response = session.get(url)
        balance = response.json()
        return balance

    def get_ticker(self):
        url = self.base_api + "/public/ticker"
        session = self.authenticate()
        response = session.get(url)
        ticker = response.json()
        return ticker

    def get_candles(self, symbol, period):
        url = self.base_api + "/public/candles/" + symbol + "?period=" + period
        session = self.authenticate()
        response = session.get(url)
        candles = response.json()
        return candles

    def send_order(self, symbol, side, quantity, type):
        url = self.base_api + "/spot/order/"
        #timestamp = str(int(time.time() * 1000))
        session = self.authenticate()
        order = {'symbol':symbol, 'side':side, 'quantity':quantity, 'type':type}
        response = session.post(url, data = order)
        resp = response.json()

        return resp

    def send_to_db(self, symbol, order_id, trade_id, side, quantity, price, amount, fee, trade_date):
        cursor.execute("INSERT INTO trades (symbol, order_id, trade_id, side, quantity, price, amount, fee, trade_date)"
                       "VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                       (symbol, order_id, trade_id, side, quantity, price, amount, fee, trade_date))
        conn.commit()
        return symbol

    def get_trade_history(self, symbol):
        url = self.base_api + "/spot/history/trade?symbol=" + symbol
        session = self.authenticate()
        response = session.get(url)
        history = response.json()
        return history

    def get_fee_history(self, symbol):
        "https://api.fmfw.io/api/3/spot/fee/" + symbol
        url = self.base_api + "/spot/fee/" + symbol
        session = self.authenticate()
        response = session.get(url)
        fee = response.json()
        return fee

client = Client(api_key, api_secret)
# symbol, side, quantity, type
# order = client.send_order('MELDUSDT',  'sell', '990', 'market')


#print(balance['available'])
# df = pd.DataFrame(client.get_candles('ETHBTC'))
