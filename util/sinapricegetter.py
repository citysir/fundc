#coding:utf-8

import re
import time
import datetime
import urllib2

from BeautifulSoup import BeautifulSoup

RE = re.compile('http://vip\.stock\.finance\.sina\.com\.cn/quotes_service/view/vMS_tradehistory\.php\?symbol=(sh|sz)[\d]+&date=[\d]+\-[\d]+\-[\d]+')

def get_an_try(s, startdate, enddate, times=1):
    while times > 0:
        try:
            return get(s, startdate, enddate)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)

def get(s, startdate, enddate):
    '''
http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000100.phtml
    '''
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept':'text/html;q=0.9,*/*;q=0.8',
              'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Connection':'close',
              'Referer':'http://finance.yahoo.com/',
              }
#     url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=2014&jidu=4' % s
    url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml' % s
    print url
    request = urllib2.Request(url, None, header)
    response = urllib2.urlopen(request, None, 15)
    text = response.read()
    
    results = {}
    soup = BeautifulSoup(text)
    for e in soup.findAll('a', {'href': RE, 'target': '_blank'}):
        tr = e.parent.parent.parent
        results.update(_parse_tr(tr))
    return results

def _parse_tr(tr):
    '''
    开盘价 最高价 收盘价 最低价 交易量(股) 交易金额(元)
    '''
    tds = tr.findAll('td')
    datestr = tds[0].find('a').text
    open_price = tds[1].contents[0].string
    high = tds[2].contents[0].string
    close = tds[3].contents[0].string
    low = tds[4].contents[0].string
    volumn = tds[5].contents[0].string
    amount = tds[6].contents[0].string
    
    date = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
    return {
            date : {
                    'Open': float(open_price),
                    'High': float(high),
                    'Low': float(low),
                    'Close': float(close),
                    'Volumn': int(volumn),
                    'AdjClose': float(close),
                    'Amount': float(amount),
                    }
            }

def _test_match():
    r = re.compile(RE)
    print r.match("http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz000100&date=2014-11-28")
    print r.match("http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sh600001&date=2014-11-28")

    
if __name__ == '__main__':
#     _test_match()
    print get('000100', datetime.date.today() - datetime.timedelta(days=3), datetime.date.today() - datetime.timedelta(days=1))