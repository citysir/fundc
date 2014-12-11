#coding:utf-8

import time
import datetime
import json

from fundc import config
from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def run():
    apikey = '250e4df5-a023-4017-82c5-676625e2b54b'
    secretkey = 'FE7B5462F294969CAF05FC2007F1539C'
    okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国际账号需要 修改为 www.okcoin.com  国内站账号需要修改为www.okcoin.cn
    
    #现货API
    okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)
    
    now = datetime.datetime.now()
    end_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
    
    minutes = 60 
    since = time.mktime((end_time - datetime.timedelta(minutes=minutes)).timetuple())
    
    prices = okcoinSpot.kline(symbol = 'btc_cny', type = '1min', size = minutes, since = since * 1000)

    for price in prices:
        price_time = datetime.datetime.fromtimestamp(price[0] / 1000)
        open = price[1]
        high = price[2]
        low = price[3]
        close = price[4]
        volumn = price[5]
        if not CnBtCoinMinutelyPrice.objects.filter(PriceTime=price_time).exists():
            CnBtCoinMinutelyPrice(Price=close, Volumn=volumn, PriceTime=price_time, RecordTime=now).save()


if __name__ == '__main__':
    run()