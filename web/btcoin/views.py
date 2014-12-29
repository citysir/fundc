#coding=utf8

import sys
import json

from django.shortcuts import render_to_response
from fundc import config
from fundc.models.btcoin import CnBtCoinMinutelyPrice

def btchart(request):
    hours = request.REQUEST.get("h")
    refresh = int(request.REQUEST.get("r", '0'))

    hours = int(hours) if hours else 24  
    limit = 60 * hours
    prices = list(CnBtCoinMinutelyPrice.objects.all().order_by('-PriceTime')[:limit])
    prices.reverse()

    hours_desc = _get_hours_desc(hours)
    
    if prices:
        min_x = prices[0].PriceTime.strftime("%Y-%m-%d %H:%M")
        max_x = prices[-1].PriceTime.strftime("%Y-%m-%d %H:%M")
    min_y = sys.maxint
    max_y = 0
     
    xAxis = [] #["10-1", "10-2", "10-3", "10-4", "10-5", ...]
    series = [] # 开盘，收盘，最低，最高 [ [2320.26,2302.6,2287.3,2362.94], [2300,2291.3,2288.26,2308.38] ]
    volumns = []
    for price in prices:
        minute = price.PriceTime.strftime("%Y-%m-%d %H:%M")
        xAxis.append(minute)
        series.append((price.Open, price.Close, price.Low, price.High))
        volumns.append(price.Volumn)
        if price.High > max_y:
            max_y = price.High
        if price.Low < min_y:
            min_y = price.Low

    xAxis = json.dumps(xAxis)
    series = json.dumps(series)
    
    return render_to_response('btcoin/btchart.html', locals())


def _get_hours_desc(hours):
    if hours == 1:
        return '1小时'
    elif hours == 3:
        return '3小时'
    elif hours == 6:
        return '6小时'
    elif hours == 12:
        return '12小时'
    elif hours == 24:
        return '1天'
    elif hours == 72:
        return '3天'
    elif hours == 168:
        return '7天'
    else:
        raise Exception("不支持的 hours %s" % hours)
    