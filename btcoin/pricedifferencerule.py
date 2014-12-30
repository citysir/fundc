#coding:utf-8

from fundc.btcoin.rule import Rule

class PriceDifferenceRule(Rule):

    def set_context(self, context):
        self.context = context

    def get_max_cny_amount(self):
        return 200.0

    def will_buy(self):
        bids = self.context['bids']
        asks = self.context['asks']
        # 买一和卖一价差很大的情况下购买
        return (asks[-1][0] - bids[0][0] > 0.5)

    def get_buy_price(self):
        bids = self.context['bids']
        return bids[0][0] + 0.02

    def will_sell(self):
        bids = self.context['bids']
        asks = self.context['asks']
        return (asks[-1][0] - bids[0][0] < 0.2)

    def get_sell_price(self):
        bids = self.context['bids']
        return bids[0][0]