#coding:utf-8

import time
import datetime

from fundc import config, constant
from fundc.util import sinapricegetter
from django.db import transaction
from fundc.models.stock import StockBaseInfo, CnStockDailyPrice

def run():
    enddate = datetime.date.today()
    startdate = enddate - datetime.timedelta(days=7)
    for base_info in StockBaseInfo.objects.filter(Region=constant.Region.CN):
        update_prices(base_info, startdate, enddate)
        time.sleep(0.2)

def update_prices(base_info, startdate, enddate):
    daily_prices = sinapricegetter.get_an_try(base_info.Code, startdate, enddate, 3)
    if daily_prices:
        save_daily_prices(base_info.Code, daily_prices)

@transaction.commit_on_success(using=config.FundcDatabase.ROUTERNAME)
def save_daily_prices(code, daily_prices):
    for date, price in daily_prices.iteritems():
        if not CnStockDailyPrice.objects.filter(Date=date, Code=code).exists():
            CnStockDailyPrice(Date=date, Code=code, High=price['High'], Low=price['Low'], Open=price['Open'], Close=price['Close'], AdjClose=price['AdjClose']).save()
    if daily_prices:
        print 'saved %s daily prices' % code

def update(code):
    enddate = datetime.date.today() - datetime.timedelta(days=1)
    startdate = enddate - datetime.timedelta(days=365)
    base_info = StockBaseInfo.objects.filter(Code=code).get()
    update_prices(base_info, startdate, enddate)


if __name__ == '__main__':
    run()
#     update("000100")