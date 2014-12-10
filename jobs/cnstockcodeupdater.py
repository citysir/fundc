#coding:utf-8

import re
import urllib2
from BeautifulSoup import BeautifulSoup

from fundc import config, constant
from fundc.models.stock import StockBaseInfo

URL = "http://bbs.10jqka.com.cn/codelist.html"
RE = re.compile("http://bbs\.10jqka\.com\.cn/(sh|sz),[\d]+,1")

def run():
    count = 0
    for code, name in _find_code_names():
        if not StockBaseInfo.objects.filter(Code=code).exists():
            StockBaseInfo(Code=code, Name=name, Region=constant.Region.CN, Tag=constant.ChinaTag.get(code)).save()
            print "saved", code, name
            count += 1

    if count == 0:
        print "no data to update"

def _find_code_names():
    for line in _find_all_stock_lines():
        parts = line.strip().rsplit(" ", 1)
        name, code = parts[0].strip(), parts[1].strip()
        if not code.isdigit():
            raise Exception("error %s" % code)
        yield code, name

def _find_all_stock_lines():
    '''
<li><a href="http://bbs.10jqka.com.cn/sz,000407,1" target="_blank" title="胜利股份">胜利股份 000407</a></li>
    '''
    response = urllib2.urlopen(URL)
    text = response.read()
    soup = BeautifulSoup(text)
    for e in soup.findAll('a',{'href': RE, 'target': '_blank'}):
        yield e.text
    
def _test_match():
    r = re.compile(RE)
    print r.match("http://bbs.10jqka.com.cn/sh,600000,1")
    print r.match("http://bbs.10jqka.com.cn/sz,002275,1")
    

if __name__ == '__main__':
    run()