#coding:utf-8

import time
import datetime

from fundc import config
from fundc.common.okcoin import OKCoin
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def run():
    api_key = '250e4df5-a023-4017-82c5-676625e2b54b'
    secret_key = 'FE7B5462F294969CAF05FC2007F1539C'
    api = OKCoin(api_key, secret_key)
    
    now = datetime.datetime.now()
    price_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
    ticker = api.get_ticker('btc_cny')

    CnBtCoinMinutelyPrice(Price=ticker['last'], PriceTime=price_time, RecordTime=now).save()
    

if __name__ == '__main__':
    run()