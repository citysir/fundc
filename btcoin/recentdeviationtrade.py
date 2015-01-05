#coding:utf-8

import time, datetime

from fundc.common.okcoin.OkcoinSpotAPI import OKCoinSpot

from fundc import config
import util

class TradeRule:

    def __init__(self):
        self.last_buy_price = 0.0

    def set_last_buy_price(self, last_buy_price):
        self.last_buy_price = last_buy_price

    def get_max_cny_amount(self):
        return 500.0

    def will_buy(self, bids, asks, trades):
        min_price, max_price = 1000000.0, 0.0
        total_amount, total_cny = 0.0, 0.0
        for trade in trades:
            price = float(trade['price'])
            amount = float(trade['amount'])
            if price < min_price:
                min_price = price
            if price > max_price:
                max_price = price
            total_amount += amount
            total_cny += price * amount

        avg_price = total_cny / total_amount
        buy_price = avg_price - (avg_price - min_price) * 0.33
        return asks[-1][0] < buy_price

    def get_buy_price(self, asks):
        return asks[-1][0]

    def will_sell(self, bids, asks, trades):
        min_price, max_price = 1000000.0, 0.0
        total_amount, total_cny = 0.0, 0.0
        for trade in trades:
            price = float(trade['price'])
            amount = float(trade['amount'])
            if price < min_price:
                min_price = price
            if price > max_price:
                max_price = price
            total_amount += amount
            total_cny += price * amount

        avg_price = total_cny / total_amount
        return (self.last_buy_price - bids[0][0] > 0.1 or bids[0][0] > avg_price or self.last_buy_price - bids[0][0] >= 0.45)

    def get_sell_price(self, bids):
        return bids[0][0]


def run():
    okcoinSpot = OKCoinSpot(config.OkCoin.RESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = TradeRule()
    
    while True:
        time.sleep(0.2)

        util.cancel_orders(okcoinSpot)

        userinfo = util.try_userinfo(okcoinSpot)

        data = util.try_depth(okcoinSpot, size=1)
        bids = data['bids']
        asks = data['asks']
        
        trades = util.try_trades(okcoinSpot, since=-60)

        print '-' * 40
        print datetime.datetime.now()
        print 'ask:\t%.3f\t%.3f' % (asks[-1][0], asks[-1][1])
        print 'bid:\t%.3f\t%.3f' % (bids[0][0], bids[0][1])

        btc_amount = util.get_btc_amount(userinfo)
        if rule.will_buy(bids, asks, trades):
            if btc_amount < 0.01: # btc最小交易单位为0.01
                buy_price = rule.get_buy_price(asks)
                buy_amount = rule.get_max_cny_amount() / buy_price
                rule.set_last_buy_price(buy_price)
                util.try_trade(okcoinSpot, 'btc_cny', 'buy', buy_price, buy_amount)
                print 'now buy', buy_price, buy_amount
        elif rule.will_sell(bids, asks, trades):
            if btc_amount >= 0.01: # btc最小交易单位为0.01
                sell_price = rule.get_sell_price(bids)
                util.try_trade(okcoinSpot, 'btc_cny', 'sell', sell_price, btc_amount)
                print 'now sell', sell_price, btc_amount


if __name__ == '__main__':
    run()
    