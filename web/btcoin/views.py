#coding=utf8

import json

from django.shortcuts import render_to_response
from fundc import config
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def btchart(request):
    hours = request.REQUEST.get("h")
    refresh = int(request.REQUEST.get("r", '0'))

    hours = int(hours) if hours else 24  
    limit = 60 * hours
    prices = list(CnBtCoinMinutelyPrice.objects.all().order_by('-id')[:limit])
    prices.reverse()

    hours_desc = _get_hours_desc(hours)
     
    xAxis = [] #["1", "2", "3", "4", "5", ...]
    series = [] #  [ 2312, 2313, ... ]
    volumns = []
    for price in prices:
        minute = price.PriceTime.strftime("%H-%M")
        xAxis.append(minute)
        series.append(price.Price)
        volumns.append(price.Volumn)

    xAxis = json.dumps(xAxis)
    series = json.dumps(series)
    
    return render_to_response('btcoin/btchart.html', locals())


def _get_hours_desc(hours):
    if hours == 1:
        return '1小时内'
    elif hours == 3:
        return '3小时内'
    elif hours == 6:
        return '6小时内'
    elif hours == 12:
        return '12小时内'
    elif hours == 24:
        return '1天内'
    elif hours == 72:
        return '3天内'
    elif hours == 168:
        return '7天内'
    else:
        raise Exception("不支持的 hours %s" % hours)
    