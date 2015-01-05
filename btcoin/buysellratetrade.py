#coding:utf-8

import time, datetime

from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot

from fundc import config
from fundc.models.btcoin import CnBtCoinTransaction
import util

class TradeRule:

    def get_max_cny_amount(self):
        return 200.0

    def will_buy(self, bids, asks):
        bid_sum = sum([bid[0] * bid[1] for bid in bids])
        ask_sum = sum([ask[0] * ask[1] for ask in asks])
        # (asks[-1][0] - bids[0][0] < 0.1) 逻辑是为了避免买一和卖一价差太大
        return (asks[-1][0] - bids[0][0] < 0.1) and bid_sum / ask_sum > 3.0

    def get_buy_price(self, asks):
        return asks[-1][0]

    def will_sell(self, bids, asks):
        bid_sum = sum([bid[0] * bid[1] for bid in bids])
        ask_sum = sum([ask[0] * ask[1] for ask in asks])
        return bid_sum / ask_sum < 1.0
    
    def get_sell_price(self, bids):
        return bids[0][0]

def run():
    okcoinSpot = OKCoinSpot(config.OkCoin.RESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = TradeRule()

    while True:
        time.sleep(0.2)

        data = util.try_depth(okcoinSpot, size=5)
        bids = data['bids']
        asks = data['asks']

        print '--', datetime.datetime.now(), '--------------'
        print 'asks:'
        for ask in asks:
            print '%2f\t%.3f' % (ask[0], ask[1])
        print 'bids:'
        for bid in bids:
            print '%2f\t%.3f' % (bid[0], bid[1])

        util.cancel_orders(okcoinSpot)

        userinfo = util.try_userinfo(okcoinSpot)
        btc_amount = util.get_btc_amount(userinfo)
        if rule.will_buy(bids, asks):
            if btc_amount < 0.01: # btc最小交易单位为0.01
                buy_price = rule.get_buy_price(asks)
                btc_amount = rule.get_max_cny_amount() / buy_price
                print 'now buy', buy_price, btc_amount
                util.try_trade(okcoinSpot, 'btc_cny', 'buy', buy_price, btc_amount)
                CnBtCoinTransaction(Price=buy_price, Amount=btc_amount, TradeType='buy', TradeTime=datetime.datetime.now()).save()
        elif rule.will_sell(bids, asks):
            if btc_amount >= 0.01: # btc最小交易单位为0.01
                sell_price = rule.get_sell_price(bids)
                print 'now sell', sell_price, btc_amount
                util.try_trade(okcoinSpot, 'btc_cny', 'sell', sell_price, btc_amount)
                CnBtCoinTransaction(Price=sell_price, Amount=btc_amount, TradeType='sell', TradeTime=datetime.datetime.now()).save()


if __name__ == '__main__':
    run()
    