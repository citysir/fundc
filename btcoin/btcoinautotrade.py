#coding:utf-8

import time, datetime

from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot

from fundc import config
from fundc.models.btcoin import CnBtCoinTransaction
from pricedifferencerule import PriceDifferenceRule

def cancel_orders(okcoinSpot):
    orderinfo = okcoinSpot.orderinfo('btc_cny', -1)
    for order in orderinfo['orders']:
    #status:-1:已撤销  0:未成交  1:部分成交  2:完全成交
        if order['status'] in (0, 1):
            cancelresult = try_cancelOrder(okcoinSpot, 'btc_cny', order['order_id'])
            if cancelresult['result']:
                print 'cancelled order', order['order_id']

def get_btc_amount(userinfo):
    '''
    {u'info': {u'funds': {u'freezed': {u'ltc': u'0', u'btc': u'0', u'cny': u'0'}, u'asset': {u'net': u'2000.85', u'total': u'2000.85'}, u'free': {u'ltc': u'0', u'btc': u'0.01', u'cny': u'1981.36'}}}, u'result': True}
    '''
    return float(userinfo['info']['funds']['free']['btc'])

def run():
    okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国际账号需要 修改为 www.okcoin.com  国内站账号需要修改为www.okcoin.cn
    
    #现货API
    okcoinSpot = OKCoinSpot(okcoinRESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = PriceDifferenceRule()
    
    while True:
        time.sleep(0.5)

        data = try_depth(okcoinSpot, size=5)
        bids = data['bids']
        asks = data['asks']

        context = {
            'bids': bids,
            'asks': asks,
        }

        print '--', datetime.datetime.now(), '--------------'
        print 'asks:'
        for ask in asks:
            print '%2f\t%.3f' % (ask[0], ask[1])
        print 'bids:'
        for bid in bids:
            print '%2f\t%.3f' % (bid[0], bid[1])

        rule.set_context(context)

        cancel_orders(okcoinSpot)

        userinfo = try_userinfo(okcoinSpot)
        btc_amount = get_btc_amount(userinfo)
        if rule.will_buy():
            if btc_amount < 0.01: # btc最小交易单位为0.01
                buy_price = rule.get_buy_price()
                btc_amount = rule.get_max_cny_amount() / buy_price
                print 'now buy', buy_price, btc_amount
                try_trade(okcoinSpot, 'btc_cny', 'buy', buy_price, btc_amount)
                rule.set_last_buy_price(buy_price)
                CnBtCoinTransaction(Price=buy_price, Amount=btc_amount, TradeType='buy', TradeTime=datetime.datetime.now()).save()
                time.sleep(0.5)
        elif rule.will_sell():
            if btc_amount >= 0.01: # btc最小交易单位为0.01
                sell_price = rule.get_sell_price()
                print 'now sell', sell_price, btc_amount
                try_trade(okcoinSpot, 'btc_cny', 'sell', sell_price, btc_amount)
                CnBtCoinTransaction(Price=sell_price, Amount=btc_amount, TradeType='sell', TradeTime=datetime.datetime.now()).save()

def try_cancelOrder(okcoinSpot, symbol, order_id, times=3):
    while times > 0:
        try:
            return okcoinSpot.cancelOrder(symbol, order_id)
        except Exception, e:
            print e
            times -= 1
            time.sleep(1)

def try_depth(okcoinSpot, size=5, times=3):
    while times > 0:
        try:
            return okcoinSpot.depth(size=size)
        except Exception, e:
            print e
            times -= 1
            time.sleep(1)
            
def try_userinfo(okcoinSpot, times=3):
    while times > 0:
        try:
            return okcoinSpot.userinfo()
        except Exception, e:
            print e
            times -= 1
            time.sleep(1)

def try_trade(okcoinSpot, symbol, tradeType, price, amount, times=3):
    while times > 0:
        try:
            return okcoinSpot.trade(symbol,tradeType,price,amount)
        except Exception, e:
            print e
            times -= 1
            time.sleep(1)


if __name__ == '__main__':
    run()
    