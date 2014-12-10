#coding:utf-8

import re
import urllib2
from BeautifulSoup import BeautifulSoup

from fundc import config, constant
from fundc.models.stock import StockBaseInfo

URL = "http://vip.stock.finance.sina.com.cn/usstock/ustotal.php"
RE = re.compile("http://stock.finance.sina.com.cn/usstock/quotes/\w+.html")

def run():
    count = 0
    for code, name, name2 in _find_code_names():
        if not StockBaseInfo.objects.filter(Code=code).exists():
            StockBaseInfo(Code=code, Name=name, Name2=name2, Region=constant.Region.US).save()
            print "saved %s,%s,%s" % (code, name, name2)
            count += 1

    if count == 0:
        print "no data to update"

def _find_code_names():
    for line in _find_all_stock_lines():
        code, name, name2 = line.strip().split(",", 2)
        yield code, name, name2

def _find_all_stock_lines():
    '''
<a href="http://stock.finance.sina.com.cn/usstock/quotes/GS.html"
    rel="suggest" title="GS,Goldman Sachs Group Inc.,高盛集团">高盛(GS)</a>
    '''
    response = urllib2.urlopen(URL)
    text = response.read()
    soup = BeautifulSoup(text.decode('gbk').encode('utf-8'))
    for e in soup.findAll('a',{'href': RE, 'rel': 'suggest'}):
        yield e['title']
    
def _test_match():
    r = re.compile(RE)
    print r.match("http://stock.finance.sina.com.cn/usstock/quotes/GS.html")
    print r.match("http://stock.finance.sina.com.cn/usstock/quotes/BAC.html")


if __name__ == '__main__':
    run()