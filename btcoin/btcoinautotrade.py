#coding:utf-8

import time, datetime

from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot

from fundc import config
from fundc.models.btcoin import CnBtCoinTransaction
from buysellraterule import BuySellRateRule

def cancel_orders(okcoinSpot):
    orderinfo = okcoinSpot.orderinfo('btc_cny', -1)
    for order in orderinfo['orders']:
    #status:-1:已撤销  0:未成交  1:部分成交  2:完全成交
        if order['status'] in (0, 1):
            cancelresult = okcoinSpot.cancelOrder('btc_cny', order['order_id'])
            if cancelresult['result']:
                print 'canceled order', order['order_id']
                
def get_btc_amount(userinfo):
    '''
    {u'info': {u'funds': {u'freezed': {u'ltc': u'0', u'btc': u'0', u'cny': u'0'}, u'asset': {u'net': u'2000.85', u'total': u'2000.85'}, u'free': {u'ltc': u'0', u'btc': u'0.01', u'cny': u'1981.36'}}}, u'result': True}
    '''
    return float(userinfo['info']['funds']['free']['btc'])

def run():
    okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国际账号需要 修改为 www.okcoin.com  国内站账号需要修改为www.okcoin.cn
    
    #现货API
    okcoinSpot = OKCoinSpot(okcoinRESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = BuySellRateRule()
    
    while True:
        time.sleep(5)
        
        data = okcoinSpot.depth(size=10)
        bids = data['bids']
        asks = data['asks']
        
        context = {
            'bids': bids,
            'asks': asks,
        }
        
        print '--', datetime.datetime.now(), '--------------'
        print 'asks:'
        for ask in asks[:10]:
            print '%2f\t%.3f' % (ask[0], ask[1])
        print 'bids:'
        for bid in bids[:10]:
            print '%2f\t%.3f' % (bid[0], bid[1])

        rule.set_context(context)

        cancel_orders(okcoinSpot)

        userinfo = okcoinSpot.userinfo()
        btc_amount = get_btc_amount(userinfo)
        if rule.will_buy():
            if btc_amount == 0:
                print 'now buy'
                btc_amount = rule.get_max_cny_amount() / asks[-1][0]
                okcoinSpot.trade('btc_cny', 'buy', asks[-1][0], btc_amount)
                CnBtCoinTransaction(Price=asks[-1][0], Amount=btc_amount, TradeType='buy', TradeTime=datetime.datetime.now()).save()
        elif rule.will_sell():
            if btc_amount > 0:
                print 'now sell'
                okcoinSpot.trade('btc_cny', 'sell', bids[0][0], btc_amount)
                CnBtCoinTransaction(Price=bids[0][0], Amount=btc_amount, TradeType='sell', TradeTime=datetime.datetime.now()).save()

run()
    