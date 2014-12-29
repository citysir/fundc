#coding utf-8

from fundc.btcoin.rule import Rule

class BuySellRateRule(Rule):
    
    def set_context(self, context):
        self.context = context


    def get_max_amount(self):
        return 100.0


    def will_buy(self):
        bids = self.context['bids']
        asks = self.context['asks']
        
        care_count = 10
        bid_sum = sum([bid[0] * bid[1] for bid in bids[:care_count]])
        ask_sum = sum([ask[0] * ask[1] for ask in asks[:care_count]])

        return bid_sum / ask_sum > 3.0


    def will_sell(self):
        bids = self.context['bids']
        asks = self.context['asks']
        
        care_count = 10
        bid_sum = sum([bid[0] * bid[1] for bid in bids[:care_count]])
        ask_sum = sum([ask[0] * ask[1] for ask in asks[:care_count]])

        return bid_sum / ask_sum < 1.0
        