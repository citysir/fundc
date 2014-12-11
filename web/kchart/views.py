#coding=utf8

import sys
import datetime
import json

from django.shortcuts import render_to_response
from fundc import config, constant
from fundc.models.stock import StockBaseInfo, CnStockDailyPrice, UsStockDailyPrice

def kchart(request):
    stockCode = request.REQUEST.get("stockCode")
    if not stockCode:
        stockCode = '000100'

    enddate = datetime.date.today() - datetime.timedelta(days=1)
    startdate = enddate - datetime.timedelta(days=365)
    
    base_info = StockBaseInfo.objects.filter(Code=stockCode).get()
    if base_info.Region == constant.Region.CN:
        prices = list(CnStockDailyPrice.objects.filter(Date__gte=startdate, Date__lte=enddate, Code=base_info.Code).order_by("Date"))
    elif base_info.Region == constant.Region.US:
        prices = list(UsStockDailyPrice.objects.filter(Date__gte=startdate, Date__lte=enddate, Code=base_info.Code).order_by("Date"))
    else:
        prices = []
    
    if prices:
        min_x = prices[0].Date.strftime("%Y/%m/%d")
        max_x = prices[-1].Date.strftime("%Y/%m/%d")
    min_y = sys.maxint
    max_y = 0
    
    xAxis = [] #["2013/1/24", "2013/1/25", "2013/1/28", "2013/1/29", "2013/1/30"]
    series = [] # 开盘，收盘，最低，最高 [ [2320.26,2302.6,2287.3,2362.94], [2300,2291.3,2288.26,2308.38] ]
    for price in prices:
        datestr = price.Date.strftime("%Y-%m-%d")
        xAxis.append(datestr)
        series.append((price.Open, price.Close, price.Low, price.High))
        if price.High > max_y:
            max_y = price.High
        if price.Low < min_y:
            min_y = price.Low
    
    xAxis = json.dumps(xAxis)
    series = json.dumps(series)
    
    return render_to_response('kchart/kchart.html', locals())