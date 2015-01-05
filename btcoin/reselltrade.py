#coding:utf-8

import time, datetime

from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot

from fundc import config
from fundc.models.btcoin import CnBtCoinTransaction
import util

class TradeRule:

    def __init__(self):
        self.last_buy_price = 0.0

    def set_last_buy_price(self, last_buy_price):
        self.last_buy_price = last_buy_price

    def get_max_cny_amount(self):
        return 100.0

    def will_buy(self, bids, asks):
        x = 5
        return asks[-1][0] - bids[0][0] < 0.1 and bids[0][1] - asks[-1][1] > 0.2 and \
               asks[-1][0] - bids[0][0] < 0.01 * x and bids[0][1] / asks[-1][1] > 0.1 * x

    def get_buy_price_volumn(self, asks):
        return asks[-1][0], asks[-1][1]

    def will_sell(self, bids, asks):
        return bids[0][0] - self.last_buy_price > 0.02 or self.last_buy_price - bids[0][0] >= 0.1

    def get_sell_price(self, bids):
        return bids[0][0]


def run():
    okcoinSpot = OKCoinSpot(config.OkCoin.RESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = TradeRule()
    
    while True:
        time.sleep(0.1)

        data = util.try_depth(okcoinSpot, size=1)

        bids = data['bids']
        asks = data['asks']

        print '-' * 32
        print datetime.datetime.now()
        print 'ask:\t%2f\t%.3f' % (asks[0][0], asks[0][1])
        print 'bid:\t%2f\t%.3f' % (bids[0][0], bids[0][1])

        userinfo = util.try_userinfo(okcoinSpot)
        btc_amount = util.get_btc_amount(userinfo)
        if rule.will_buy(bids, asks):
            if btc_amount < 0.01: # btc最小交易单位为0.01
                buy_price, buy_amount = rule.get_buy_price_volumn(asks)
                max_buy_amount = rule.get_max_cny_amount() / buy_price
                buy_amount = min(buy_amount, max_buy_amount)
                print 'now buy', buy_price, buy_amount
                if util.get_freezed_cny(userinfo) > 0.1:
                    util.cancel_orders(okcoinSpot)
                util.try_trade(okcoinSpot, 'btc_cny', 'buy', buy_price, buy_amount)
                rule.set_last_buy_price(buy_price)
                time.sleep(0.5)
                print 'now sell', buy_price + 0.02, btc_amount
                util.try_trade(okcoinSpot, 'btc_cny', 'sell', buy_price + 0.02, btc_amount)
#                 CnBtCoinTransaction(Price=buy_price, Amount=btc_amount, TradeType='buy', TradeTime=datetime.datetime.now()).save()
        elif rule.will_sell(bids, asks):
            if btc_amount >= 0.01: # btc最小交易单位为0.01
                sell_price = rule.get_sell_price(bids)
                print 'now sell', sell_price, btc_amount
                util.try_trade(okcoinSpot, 'btc_cny', 'sell', sell_price, btc_amount)
#                 CnBtCoinTransaction(Price=sell_price, Amount=btc_amount, TradeType='sell', TradeTime=datetime.datetime.now()).save()


if __name__ == '__main__':
    run()
    