#coding:utf-8

import time

def get_btc_amount(userinfo):
    '''
    {u'info': {u'funds': {u'freezed': {u'ltc': u'0', u'btc': u'0', u'cny': u'0'}, u'asset': {u'net': u'2000.85', u'total': u'2000.85'}, u'free': {u'ltc': u'0', u'btc': u'0.01', u'cny': u'1981.36'}}}, u'result': True}
    '''
    return float(userinfo['info']['funds']['free']['btc'])

def get_asset(userinfo):
    return userinfo['info']['funds']['asset']

def get_freezed_cny(userinfo):
    return float(userinfo['info']['funds']['freezed']['cny'])

def cancel_orders(okcoinSpot):
    orderinfo = okcoinSpot.orderinfo('btc_cny', -1)
    for order in orderinfo['orders']:
    #status:-1:已撤销  0:未成交  1:部分成交  2:完全成交
        if order['status'] in (0, 1):
            cancelresult = try_cancelOrder(okcoinSpot, 'btc_cny', order['order_id'])
            if cancelresult['result']:
                print 'cancelled order', order['order_id']

def try_cancelOrder(okcoinSpot, symbol, order_id, times=3):
    while times > 0:
        try:
            return okcoinSpot.cancelOrder(symbol, order_id)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)

def try_ticker(okcoinSpot, symbol='btc_cny', times=3):
    while times > 0:
        try:
            return okcoinSpot.ticker(symbol=symbol)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)

def try_depth(okcoinSpot, size=5, times=3):
    while times > 0:
        try:
            return okcoinSpot.depth(size=size)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)
            
def try_userinfo(okcoinSpot, times=3):
    while times > 0:
        try:
            return okcoinSpot.userinfo()
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)

def try_trade(okcoinSpot, symbol, tradeType, price, amount, times=3):
    while times > 0:
        try:
            return okcoinSpot.trade(symbol,tradeType,price,amount)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)
            
def try_trades(okcoinSpot, symbol='btc_cny', since=-60, times=3):
    while times > 0:
        try:
            return okcoinSpot.trades(symbol,since)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)
            
def try_kline(okcoinSpot, symbol, type, size, since, times=3):
    while times > 0:
        try:
            return okcoinSpot.kline(symbol=symbol, type=type, size=size, since=since)
        except Exception, e:
            print e
            times -= 1
            time.sleep(0.5)