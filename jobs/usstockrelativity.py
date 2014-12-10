#coding:utf-8

import datetime

import numpy

from fundc import config, constant

from django.db import transaction

from fundc.models.stock import StockBaseInfo, UsStockDailyPrice, UsStockGroup
from fundc.common import kmeans

def run(output_path):
    print 'load data from db'
    
    days = 90
    enddate = datetime.date.today() - datetime.timedelta(days=1)
    startdate = enddate - datetime.timedelta(days=days)
    base_infos = StockBaseInfo.objects.filter(Region=constant.Region.US)
    base_infos = dict([(base_info.Code, base_info.Name) for base_info in base_infos])
    prices = UsStockDailyPrice.objects.filter(Date__gte=startdate, Date__lte=enddate)
    
    print 'init stock_date_rise_prices'

    stock_date_rise_prices = {}
    stock_codes = set()
    for price in prices:
        if price.Open == 0:
            rise = 0
        else:
            rise = (price.Close - price.Open) / price.Open
            
        stock_date_rise_prices[(price.Date, price.Code)] = rise
        stock_codes.add(price.Code)

    print 'init stock_date_rise_data'
    
    stock_date_rise_data = {}
    for code in stock_codes:
        data = []
        date = startdate
        while date < enddate:
            data.append(stock_date_rise_prices.get((date, code), 0))
            date += datetime.timedelta(days=1)
        stock_date_rise_data[code] = data
      
    ## step 1: load data  
    print "step 1: load data..."
    codes = []
    datas = []   
    for code, data in stock_date_rise_data.iteritems():
        datas.append(data)
        codes.append(code)
    
    k = len(datas) / 10

    print "step 2: clustering...", k, len(datas)
    datas = numpy.mat(datas)

    centroids, clusterAssment = kmeans.kmeans(datas, k)
  
    ## step 3: show the result  
    print "step 3: output the result..."
    
    output(output_path, base_infos, codes, datas, clusterAssment)
            
    print "all finished."
    
@transaction.commit_on_success(config.FundcDatabase.ROUTERNAME)
def output(output_path, base_infos, codes, datas, clusterAssment):
    UsStockGroup.objects.all().delete()
    with open(output_path, 'wb') as f:
        numSamples, _ = datas.shape
        groups = {}
        for i in xrange(numSamples):  
            markIndex = int(clusterAssment[i, 0])
            groups.setdefault(markIndex, set()).add(codes[i])
            
        for markIndex, codes in groups.iteritems():
            for code in codes:
                f.write('%s,%s,%s\n' % (markIndex, code.encode('utf-8'), base_infos[code].encode('utf-8')))
                UsStockGroup(Code=code.encode('utf-8'), StockGroup=markIndex).save()
            f.write('\n')


if __name__ == '__main__':
    run("d://temp/usstockrelativity.txt")
#     update("000100")