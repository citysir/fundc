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
        return 200.0

    def will_buy(self, bids, asks):
        # 买一和卖一价差很大的情况下购买
        return (asks[-1][0] - bids[0][0] >= 0.31 and bids[0][1] >= 0.2)

    def get_buy_price(self, bids):
        return bids[0][0] + 0.01

    def will_sell(self, bids, asks):
        return (bids[0][0] > self.last_buy_price or self.last_buy_price - bids[0][0] >= 0.15)

    def get_sell_price(self, bids):
        return bids[0][0]


def run():
    okcoinSpot = OKCoinSpot(config.OkCoin.RESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = TradeRule()
    
    while True:
        time.sleep(0.1)

        userinfo = util.try_userinfo(okcoinSpot)
        if util.get_freezed_cny(userinfo) > 0.1:
            util.cancel_orders(okcoinSpot)

        data = util.try_depth(okcoinSpot, size=1)
        bids = data['bids']
        asks = data['asks']

        print '-' * 40
        print datetime.datetime.now()
        print 'ask:\t%.3f\t%.3f' % (asks[-1][0], asks[-1][1])
        print 'bid:\t%.3f\t%.3f' % (bids[0][0], bids[0][1])

        btc_amount = util.get_btc_amount(userinfo)
        if rule.will_buy(bids, asks):
            if btc_amount < 0.01: # btc最小交易单位为0.01
                buy_price = rule.get_buy_price(bids)
                buy_amount = rule.get_max_cny_amount() / buy_price
                print 'now buy', buy_price, buy_amount
                util.try_trade(okcoinSpot, 'btc_cny', 'buy', buy_price, buy_amount)
                rule.set_last_buy_price(buy_price)
#                 CnBtCoinTransaction(Price=buy_price, Amount=btc_amount, TradeType='buy', TradeTime=datetime.datetime.now()).save()
        elif rule.will_sell(bids, asks):
            if btc_amount >= 0.01: # btc最小交易单位为0.01
                sell_price = rule.get_sell_price(bids)
                print 'now sell', sell_price, btc_amount
                util.try_trade(okcoinSpot, 'btc_cny', 'sell', sell_price, btc_amount)
#                 CnBtCoinTransaction(Price=sell_price, Amount=btc_amount, TradeType='sell', TradeTime=datetime.datetime.now()).save()


if __name__ == '__main__':
    run()
    