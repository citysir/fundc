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

    def get_buy_cny_amount(self, asks, btc_amount):
        return self.get_max_cny_amount() - asks[-1][0] * btc_amount

    def will_buy(self, bids, asks, kline):
        ''' 2分钟均线 > 5分钟均线 '''
        m2_0_avg_price = self.cal_avg_price(kline, 2)
        m5_0_avg_price = self.cal_avg_price(kline, 5)
        m2_1_avg_price = self.cal_avg_price(kline, 2, 1)
        m5_1_avg_price = self.cal_avg_price(kline, 5, 1)
        open, high, low, close = kline[-2][1:5] #取上一分钟的数据
        print 'avg:\t%.3f\t%.3f' % (m2_0_avg_price, m5_0_avg_price)
        print 'ochl:\t%.3f\t%.3f\t%.3f\t%.3f' % (open, close, high, low)
        return m2_0_avg_price > m5_0_avg_price and \
               m2_1_avg_price <= m5_1_avg_price and \
               ( (close < open and close - low >= 2 * (high - close) ) or (close > open and high - close < close - low ) ) and \
               asks[-1][0] - bids[0][0] < 0.5

    def cal_avg_price(self, kline, minutes, delta=0):
        '''
    1417536000000,    时间戳
    2370.16,    开
    2380,        高
    2352,        低
    2367.37,    收
    17259.83    交易量
        '''
        total = 0.0
        for i in range(minutes):
            total += kline[-(i+2+delta)][4]
        return total / minutes

    def get_buy_price(self, asks):
        return asks[-1][0]

    def will_sell(self, bids, asks, kline):
        m2_0_avg_price = self.cal_avg_price(kline, 2)
        m5_0_avg_price = self.cal_avg_price(kline, 5)
        open, high, low, close = kline[-2][1:5] #取上一分钟的数据
        return (close < open and close - low < 2 * (high - close) ) or \
               (open > close and high - close >= close - low ) or \
               m2_0_avg_price < m5_0_avg_price

    def get_sell_price(self, bids):
        return bids[0][0]


def run():
    okcoinSpot = OKCoinSpot(config.OkCoin.RESTURL, config.OkCoin.ApiKey, config.OkCoin.SecretKey)
    rule = TradeRule()
    
    while True:
        time.sleep(0.5)

        util.cancel_orders(okcoinSpot)

        userinfo = util.try_userinfo(okcoinSpot)

        data = util.try_depth(okcoinSpot, size=1)
        bids = data['bids']
        asks = data['asks']

        minutes = 10 
        since = int(time.time() - 60 * minutes) * 1000 
        kline = util.try_kline(okcoinSpot, 'btc_cny', '1min', minutes, since)

        btc_amount = util.get_btc_amount(userinfo)

        print '-' * 40
        print datetime.datetime.now(), util.get_asset(userinfo)['total'], btc_amount
        print 'ask:\t%.3f\t%.3f' % (asks[-1][0], asks[-1][1])
        print 'bid:\t%.3f\t%.3f' % (bids[0][0], bids[0][1])

        if rule.will_buy(bids, asks, kline):
            if btc_amount < 0.01: # btc最小交易单位为0.01
                buy_price = rule.get_buy_price(asks)
                buy_amount = rule.get_buy_cny_amount(asks, btc_amount) / buy_price
                rule.set_last_buy_price(buy_price)
                util.try_trade(okcoinSpot, 'btc_cny', 'buy', buy_price, buy_amount)
                print 'now buy', buy_price, buy_amount
        elif rule.will_sell(bids, asks, kline):
            if btc_amount >= 0.01: # btc最小交易单位为0.01
                sell_price = rule.get_sell_price(bids)
                util.try_trade(okcoinSpot, 'btc_cny', 'sell', sell_price, btc_amount)
                print 'now sell', sell_price, btc_amount


if __name__ == '__main__':
    run()
    