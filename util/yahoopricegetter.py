#coding:utf-8

import time
import datetime
import urllib2
from StringIO import StringIO

def get_an_try(s, startdate, enddate, times=1):
    while times > 0:
        try:
            return get(s, startdate, enddate)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.2)

def get(s, startdate, enddate):
    '''
http://table.finance.yahoo.com/table.csv?s=cmcm&d=11&e=7&f=2014&g=d&a=11&b=1&c=2014&ignore=.csv
s — 股票名称 
a — 起始时间，月 
b — 起始时间，日 
c — 起始时间，年 
d — 结束时间，月 
e — 结束时间，日 
f — 结束时间，年 
g — 时间周期。
    '''
    a = startdate.month - 1
    b = startdate.day
    c = startdate.year
    d = enddate.month - 1
    e = enddate.day
    f = enddate.year
    
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept':'text/html;q=0.9,*/*;q=0.8',
              'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Connection':'close',
              'Referer':'http://finance.yahoo.com/',
              }
    url = 'http://table.finance.yahoo.com/table.csv?s=%s&d=%s&e=%s&f=%s&g=d&a=%s&b=%s&c=%s&ignore=.csv' % (s, d, e, f, a, b, c)
    print url
    request = urllib2.Request(url, None, header)
    response = urllib2.urlopen(request, None, 15)
    text = StringIO(response.read())
    results = {}
    text.readline() #skip head line
    line = text.readline()
    while line:
        line = line.strip()
        results.update(_parse_line(line))
        line = text.readline()
    return results

def _parse_line(line):
    '''
    Date    Open    High    Low    Close    Volume    Adj Close
    '''
    date, open_price, high, low, close, volumn, adj_close = line.split(',')
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return {
            date : {
                    'Open': float(open_price),
                    'High': float(high),
                    'Low': float(low),
                    'Close': float(close),
                    'Volumn': int(volumn),
                    'AdjClose': float(adj_close),
                    }
            }

    
if __name__ == '__main__':
#     print get('CMCM', datetime.date.today() - datetime.timedelta(days=3), datetime.date.today() - datetime.timedelta(days=1))
#     print get('3888.HK', datetime.date.today() - datetime.timedelta(days=3), datetime.date.today() - datetime.timedelta(days=1))
    print get('cmcm', datetime.date.today() - datetime.timedelta(days=3), datetime.date.today() - datetime.timedelta(days=1))