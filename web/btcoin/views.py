#coding=utf8

import json

from django.shortcuts import render_to_response
from fundc import config
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def btchart(request):
    limit = 60 * 24
    prices = list(CnBtCoinMinutelyPrice.objects.all().order_by('-id')[:limit])
    prices.reverse()
     
    xAxis = [] #["1", "2", "3", "4", "5", ...]
    series = [] #  [ 2312, 2313, ... ]
    for price in prices:
        minute = price.PriceTime.strftime("%M")
        xAxis.append(minute)
        series.append(price.Price)

    xAxis = json.dumps(xAxis)
    series = json.dumps(series)
    
    return render_to_response('btcoin/btchart.html', locals())