#coding:utf8

class Router:
    def db_for_read(self, model, **hints):
        from fundc.config import FundcDatabase
        from fundc.models.stock import StockBaseInfo, CnStockDailyPrice, UsStockDailyPrice, CnStockGroup, UsStockGroup
        from fundc.models.btcoin import CnBtCoinMinutelyPrice, CnBtCoinTransaction
        if model in (StockBaseInfo, CnStockDailyPrice, UsStockDailyPrice, CnStockGroup, UsStockGroup,
                     CnBtCoinMinutelyPrice, CnBtCoinTransaction):
            return FundcDatabase.ROUTERNAME

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        return None
