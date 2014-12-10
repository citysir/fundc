#coding:utf-8

import time
import httplib
import urllib
import json
import hashlib

class OKCoin():
    HOST = "www.okcoin.cn" # 注意国际站 需要将 www.okcoin.cn 换成www.okcoin.com
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def __signature(self, params):
        s = ''
        for k in sorted(params.keys()):
            if len(s) > 0:
                s += '&'
        s += k + '=' + str(params[k])
        return hashlib.md5(s + '&secret_key='+self.api_secret).hexdigest().upper()

    def __tapi_call(self, method, params={}):
        params["api_key"] = self.api_key
        params["sign"] = self.__signature(params)
        headers = {
            "Content-type" : "application/x-www-form-urlencoded",
        }
        conn = httplib.HTTPSConnection(OKCoin.HOST, timeout=30) # 注意国际站 需要将 www.okcoin.cn 换成www.okcoin.com
        temp_params = urllib.urlencode(params)
        conn.request("POST", "/api/v1/%s.do" % method, temp_params, headers)
        response = conn.getresponse()
        data = json.load(response)
        params.clear()
        conn.close()
        #print data
        res = data.get("result")
        if res == "true" or res == True:
            return data
        else:
            raise Exception("error code %s" % data["error_code"])

    def __api_call(self, method, **params):
        query_string = '&'.join(['%s=%s' % (key, value) for (key, value) in params.iteritems()])
        conn = httplib.HTTPSConnection(OKCoin.HOST, timeout=15)
        conn.request("GET", "/api/v1/%s.do?%s" % (method, query_string))
        response = conn.getresponse()
        data = json.load(response)
        conn.close()
        return data

    def get_ticker(self, symbol):
        data = self.__api_call("ticker", symbol=symbol)
        if "ticker" in data:
            return {
                "last": data["ticker"]["last"],
                "buy": data["ticker"]["buy"],
                "sell": data["ticker"]["sell"],
                "vol": data["ticker"]["vol"]
            }
        else:
            raise Exception("Error when get ticker")

    def get_ticker_try(self, symbol, times=1):
        while times > 0:
            try:
                return self.get_ticker(symbol)
            except Exception, e:
                print e
                times -= 1
                time.sleep(0.5)

    def get_depth(self, symbol):
        return self.__api_call("depth", symbol=symbol)
    
    def get_trades(self, symbol, since):
        data = self.__api_call("trades", symbol=symbol, since=since)
        return data

    def get_funds(self):
        return self.__tapi_call('userinfo')

    def get_orders(self, pair, order_id=-1):
        params = { "symbol"   : pair, "order_id" : order_id }
        result = self.__tapi_call('order_info', params)
        return result["orders"]

    def trade(self, tpair, ttype, price, amount):
        params = {
            "symbol" : tpair, # 国际站：btc_usd/ltc_usd  国内站  btc_cny/ltc_cny
            "type"   : ttype,
            "price"  : price,
            "amount" : amount
        }
        result = self.__tapi_call('trade', params)
        return result["order_id"]

    def buy(self, pair, price, amount):
        result = self.trade(pair, "buy", price, amount)
        return result

    def sell(self, pair, price, amount):
        result = self.trade(pair, "sell", price, amount)
        return result

    def cancel(self, pair, order_id):
        params = { "symbol": pair, "order_id" : order_id }
        return type(self.__tapi_call('cancel_order', params)) == dict


if __name__ == '__main__':
    api_key = '250e4df5-a023-4017-82c5-676625e2b54b'
    secret_key = 'FE7B5462F294969CAF05FC2007F1539C'
    api = OKCoin(api_key, secret_key)
    
    ticker = api.get_ticker('btc_cny')