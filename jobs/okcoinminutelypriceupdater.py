#coding:utf-8

import datetime

from fundc import config
from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def run():
    apikey = '250e4df5-a023-4017-82c5-676625e2b54b'
    secretkey = 'FE7B5462F294969CAF05FC2007F1539C'
    okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国际账号需要 修改为 www.okcoin.com  国内站账号需要修改为www.okcoin.cn
    
    #现货API
    okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)
    
    data = okcoinSpot.ticker('btc_cny')
    
    ticker = data['ticker']
    
    record_time = datetime.datetime.fromtimestamp(int(data['date']))
    price_time = datetime.datetime(record_time.year, record_time.month, record_time.day, record_time.hour, record_time.minute, 0)

    CnBtCoinMinutelyPrice(Price=ticker['last'], Volumn=ticker['vol'], PriceTime=price_time, RecordTime=record_time).save()
    

if __name__ == '__main__':
    run()