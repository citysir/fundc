#coding utf-8

class Rule:
    
    def __init__(self):
        self.last_buy_price = 0
    
    def set_context(self, context):
        pass
    
    def set_last_buy_price(self, last_buy_price):
        self.last_buy_price = last_buy_price
    
    def get_max_cny_amount(self):
        return 0.0
    
    def will_buy(self):
        return False
    
    def get_buy_price(self):
        return 0
    
    def will_sell(self):
        return False
    
    def get_sell_price(self):
        return 10000
    