#coding:utf-8

from fundc.btcoin.rule import Rule

class BuySellRateRule(Rule):
    
    def set_context(self, context):
        self.context = context


    def get_max_cny_amount(self):
        return 200.0


    def will_buy(self):
        bids = self.context['bids']
        asks = self.context['asks']
        
        bid_sum = sum([bid[0] * bid[1] for bid in bids])
        ask_sum = sum([ask[0] * ask[1] for ask in asks])

        # (asks[-1][0] - bids[0][0] < 0.1) 逻辑是为了避免买一和卖一价差太大
        return (asks[-1][0] - bids[0][0] < 0.1) and bid_sum / ask_sum > 3.0


    def will_sell(self):
        bids = self.context['bids']
        asks = self.context['asks']

        bid_sum = sum([bid[0] * bid[1] for bid in bids])
        ask_sum = sum([ask[0] * ask[1] for ask in asks])

        return bid_sum / ask_sum < 1.0
