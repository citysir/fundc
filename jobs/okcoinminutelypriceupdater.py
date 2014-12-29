#coding:utf-8

import time
import datetime

from fundc import config
from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def run():
    okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国际账号需要 修改为 www.okcoin.com  国内站账号需要修改为www.okcoin.cn
    
    #现货API
    okcoinSpot = OKCoinSpot(okcoinRESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    
    now = datetime.datetime.now()
    end_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
    
    minutes = 30 
    since = time.mktime((end_time - datetime.timedelta(minutes=minutes)).timetuple())
    
    prices = try_kline(okcoinSpot, 'btc_cny', '1min', minutes, since * 1000)

    for price in prices:
        price_time = datetime.datetime.fromtimestamp(price[0] / 1000)
        open = price[1]
        high = price[2]
        low = price[3]
        close = price[4]
        volumn = price[5]
        if not CnBtCoinMinutelyPrice.objects.filter(PriceTime=price_time).exists():
            CnBtCoinMinutelyPrice(Open=open, Close=close, High=high, Low=low, Volumn=volumn, PriceTime=price_time, RecordTime=now).save()
            
def try_kline(okcoinSpot, symbol, type, size, since, times=5):
    while times > 0:
        try:
            return okcoinSpot.kline(symbol=symbol, type=type, size=size, since=since)
        except Exception, e:
            print e
            times -= 1
            time.sleep(1)

if __name__ == '__main__':
    run()